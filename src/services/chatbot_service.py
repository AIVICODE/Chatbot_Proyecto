"""
Chatbot service
Contiene la lógica principal del chatbot
"""
from typing import Dict, Any
from persistence.db_start import db_start
from sentence_transformers import SentenceTransformer
from llm import llm


class ChatbotService:

    def __init__(self):
        """Inicializa el servicio del chatbot."""
        self.db_start = db_start() # Conecta con la base de datos de embeddings e intenciones.
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        self.ambiguous_threshold = 0.1  # Umbral de distancia para marcar ambigüedad
    
    def prerouting(self, message: str) -> str:
        """
        Determina la intención del mensaje usando embeddings y análisis de distancias.

        Retorna:
        - "sql"  -> si el mensaje es una consulta a base de datos
        - "docs" -> si el mensaje está relacionado a documentación
        - "ambiguo" -> si no se puede determinar con confianza
        """
        try:
            # Generar embedding para el mensaje del usuario
            message_embedding = self.model.encode([message], normalize_embeddings=True)
            
            # Buscar las intenciones más parecidas en la colección vectorial
            results = self.db_start.intent_collection.query(
                query_embeddings=message_embedding.tolist(),
                n_results=3,  # Se buscan las 3 más cercanas para analizar ambigüedad
                include=["metadatas", "distances"]
            )
            
            # Si no hay resultados válidos, se marca como ambiguo
            if not results['distances'] or not results['distances'][0]:
                return "ambiguo"
            
            distances = results['distances'][0]  # Lista de distancias obtenidas
            metadatas = results['metadatas'][0]  # Metadatos (ej. intenciones asociadas)
            
            # Primer resultado (el más cercano)
            best_distance = distances[0]
            best_intent = metadatas[0]['intent']
            
            # Si la distancia es muy grande, la coincidencia no es confiable
            if best_distance > self.ambiguous_threshold:
                return "ambiguo"
            
            # Si hay más de un resultado, compara el segundo
            if len(distances) > 1:
                second_distance = distances[1]
                second_intent = metadatas[1]['intent']
                
                # Si la diferencia entre ambos es poca pero las intenciones son diferentes → ambiguo
                distance_diff = second_distance - best_distance
                if distance_diff < 0.1 and best_intent != second_intent:
                    return "ambiguo"
            
             # Si pasó todas las validaciones, se devuelve la más confiable
            return best_intent
            
        except Exception as e:
            print(f"Error en prerouting: {str(e)}")
            return "ambiguo"
    
    def generate_context(self, message: str, intent: str) -> Dict[str, Any]:
        """Genera el contexto relevante según la intención detectada."""
        try:
            if intent == "ambiguo":
                # Caso en el que el sistema no entiende bien la intención
                return {
                    "context_type": "general",
                    "instructions": "La intención del usuario no está clara. Vuelve a preguntar de forma amable para clarificar su intención.",
                    "relevant_docs": [],
                    "examples": []
                }
            
            # Se genera embedding del mensaje para buscar contexto más específico
            message_embedding = self.model.encode([message], normalize_embeddings=True)
            
            # Según la intención se elige la estrategia de contexto
            if intent == "sql":
                return self._get_sql_context(message_embedding)
            elif intent == "docs":
                return self._get_docs_context(message_embedding)
            else:
                return self._get_general_context(message_embedding, intent)
                
        except Exception as e:
            print(f"Error generando contexto: {str(e)}")
            return {
                "context_type": "error",
                "instructions": "Hubo un error generando el contexto. Da una respuesta general y útil.",
                "relevant_docs": [],
                "examples": [],
                "error": str(e)
            }
    
    def _get_sql_context(self, message_embedding) -> Dict[str, Any]:
        """Contexto específico para consultas SQL."""
        # Busca ejemplos en la base de datos de intenciones que tengan 'intent=sql'.
        sql_results = self.db_start.intent_collection.query(
            query_embeddings=message_embedding.tolist(),
            n_results=3, # Top 3 para tener variedad
            where={"intent": "sql"},
            include=["documents", "metadatas"]
        )
        
        examples = []
        if sql_results['documents'] and sql_results['documents'][0]:
            examples = sql_results['documents'][0][:2]  # Toma los 2 ejemplos mas cercanos
        
        return {
            "context_type": "sql",
            "instructions": "Ayuda al usuario con consultas SQL. Proporciona código SQL claro y ejecutable con explicaciones sencillas. Considera la estructura de la base de datos y buenas prácticas.",
            "relevant_docs": [],
            "examples": examples,
            "specific_guidance": "Enfócate en la sintaxis SQL, optimización de consultas y ejemplos prácticos."
        }
    
    def _get_docs_context(self, message_embedding) -> Dict[str, Any]:
        """Contexto específico para documentación."""
        # Busca fragmentos relevantes en la colección de documentos.
        docs_results = self.db_start.docs_collection.query(
            query_embeddings=message_embedding.tolist(),
            n_results=15,
            include=["documents", "metadatas"]
        )
        
        relevant_docs = []
        if docs_results['documents'] and docs_results['documents'][0]:
             # Se recorren documentos y metadatos y se formatea la salida
            for doc, meta in zip(docs_results['documents'][0], docs_results['metadatas'][0]):
                relevant_docs.append({
                    "content": doc[:500],  # Limita el contenido para no desbordar tokens
                    "source": meta.get('source', 'Unknown'),
                    "page": meta.get('page', 'N/A')
                })
        
        return {
            "context_type": "docs",
            "instructions": "Responde basándote en la documentación provista. Sé específico y referencia la fuente si es posible.",
            "relevant_docs": relevant_docs,
            "examples": [],
            "specific_guidance": "Utiliza la documentación para dar respuestas precisas y detalladas."
        }
    
    def generate_prompt(self, message: str, intent: str, context: Dict[str, Any]) -> str:
        """
        Construye el prompt final para enviar al LLM.
        Este prompt incluye:
        - Instrucciones del sistema
        - Intención detectada
        - Contexto (docs, ejemplos)
        - Mensaje del usuario
        """
        prompt_parts = []
        
        # Instrucciones principales del sistema
        prompt_parts.append("Eres el asistente chatbot de la empresa WIS, encargada de logistica y te creamos para ayudarlos en sus consultas.")
        prompt_parts.append(f"Intención: {intent}")
        prompt_parts.append(f"Instrucciones: {context['instructions']}")
        
        # Agrega guía específica si existe
        if context.get('specific_guidance'):
            prompt_parts.append(f"Orientación específica: {context['specific_guidance']}")
        
        # Agrega documentación relevante si la hay
        if context.get('relevant_docs'):
            prompt_parts.append("\nDocumentación relevante:")
            for i, doc in enumerate(context['relevant_docs'], 1):
                prompt_parts.append(f"Doc {i} (Source: {doc['source']}, Page: {doc['page']}):")
                prompt_parts.append(doc['content'])
                prompt_parts.append("---")
        
        # Agrega ejemplos si existen
        if context.get('examples'):
            prompt_parts.append("\nEjemplos relevantes:")
            for i, example in enumerate(context['examples'], 1):
                prompt_parts.append(f"Example {i}: {example}")
        
        # Agrega mensaje original del usuario
        prompt_parts.append(f"\nMensaje del usuario: {message}")
        prompt_parts.append("\nPor favor, proporciona una respuesta útil y clara basándote en el contexto anterior.")
        
        return "\n".join(prompt_parts)
    
    def process_message(self, message: str, prompt: str = None) -> str:
        """Procesa el mensaje y genera la respuesta usando el LLM."""
        #   - Si se recibe un prompt generado → se pasa al modelo.
        #   - Si no → se usan respuestas simples por defecto (fallback).
        try:
            if prompt:
                # Llama al LLM con el prompt generado
                response = llm.complete(prompt)
                return str(response)
            else:
                 # Respuestas simples predefinidas cuando no hay contexto
                message_lower = message.lower()
                
                if "hola" in message_lower:
                    return "¡Hola! ¿En qué puedo ayudarte hoy?"
                elif "como estas" in message_lower:
                    return "¡Estoy muy bien, gracias por preguntar! ¿Y tú?"
                elif "adios" in message_lower:
                    return "¡Adiós! Que tengas un excelente día."
                elif "?" in message:
                    return f"Buena pregunta sobre '{message}'. Déjame ayudarte con eso."
                else:
                    return f"Recibí tu mensaje: '{message}'. ¿Podrías contarme un poco más para poder ayudarte mejor?"
        except Exception as e:
            print(f"Error en el procesamiento del LLM {str(e)}")
            return "Lo siento, ocurrió un error al procesar tu solicitud. Intenta nuevamente."

