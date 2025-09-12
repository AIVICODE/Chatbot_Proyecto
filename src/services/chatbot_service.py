"""
Chatbot service
Contains the main business logic
"""
from typing import Dict, Any
from .vector_service import VectorService
from sentence_transformers import SentenceTransformer
from ..models import llm
import numpy as np


class ChatbotService:
    """Service that encapsulates the chatbot business logic"""
    
    def __init__(self):
        """Initialize the chatbot service"""
        self.vector_service = VectorService()
        self.model = SentenceTransformer('all-mpnet-base-v2')
        self.ambiguous_threshold = 0.3  # Threshold for determining ambiguous intent
    
    def prerouting(self, message: str) -> str:
        """Determine intent using vector database and distance analysis"""
        try:
            # Generate embedding for the input message
            message_embedding = self.model.encode([message], normalize_embeddings=True)
            
            # Search for similar intents in the vector database
            results = self.vector_service.intent_collection.query(
                query_embeddings=message_embedding.tolist(),
                n_results=3,  # Get top 3 matches to check for ambiguity
                include=["metadatas", "distances"]
            )
            
            if not results['distances'] or not results['distances'][0]:
                return "ambiguo"
            
            distances = results['distances'][0]
            metadatas = results['metadatas'][0]
            
            # Get the best match
            best_distance = distances[0]
            best_intent = metadatas[0]['intent']
            
            # Check if the best match is too far (low confidence)
            if best_distance > self.ambiguous_threshold:
                return "ambiguo"
            
            # Check for ambiguity between top results
            if len(distances) > 1:
                second_distance = distances[1]
                second_intent = metadatas[1]['intent']
                
                # If distances are very close but intents are different, it's ambiguous
                distance_diff = second_distance - best_distance
                if distance_diff < 0.1 and best_intent != second_intent:
                    return "ambiguo"
            
            return best_intent
            
        except Exception as e:
            print(f"Error in prerouting: {str(e)}")
            return "ambiguo"
    
    def generate_context(self, message: str, intent: str) -> Dict[str, Any]:
        """Generate relevant context based on intent and message"""
        try:
            if intent == "ambiguo":
                return {
                    "context_type": "general",
                    "instructions": "Provide a helpful general response. Ask clarifying questions to better understand the user's needs.",
                    "relevant_docs": [],
                    "examples": []
                }
            
            # Generate embedding for the message to find relevant context
            message_embedding = self.model.encode([message], normalize_embeddings=True)
            
            # Strategy based on intent type
            if intent == "sql":
                return self._get_sql_context(message_embedding)
            elif intent == "docs":
                return self._get_docs_context(message_embedding)
            else:
                return self._get_general_context(message_embedding, intent)
                
        except Exception as e:
            print(f"Error generating context: {str(e)}")
            return {
                "context_type": "error",
                "instructions": "Provide a general helpful response.",
                "relevant_docs": [],
                "examples": [],
                "error": str(e)
            }
    
    def _get_sql_context(self, message_embedding) -> Dict[str, Any]:
        """Get SQL-specific context and examples"""
        # Search for relevant SQL examples/patterns
        sql_results = self.vector_service.intent_collection.query(
            query_embeddings=message_embedding.tolist(),
            n_results=3,
            where={"intent": "sql"},
            include=["documents", "metadatas"]
        )
        
        examples = []
        if sql_results['documents'] and sql_results['documents'][0]:
            examples = sql_results['documents'][0][:2]  # Top 2 SQL examples
        
        return {
            "context_type": "sql",
            "instructions": "Help the user with SQL queries. Provide clear, executable SQL code with explanations. Consider database structure and best practices.",
            "relevant_docs": [],
            "examples": examples,
            "specific_guidance": "Focus on SQL syntax, query optimization, and practical examples."
        }
    
    def _get_docs_context(self, message: str, message_embedding) -> Dict[str, Any]:
        """Get documentation-specific context"""
        # Search for relevant documentation chunks
        docs_results = self.vector_service.docs_collection.query(
            query_embeddings=message_embedding.tolist(),
            n_results=3,
            include=["documents", "metadatas"]
        )
        
        relevant_docs = []
        if docs_results['documents'] and docs_results['documents'][0]:
            for doc, meta in zip(docs_results['documents'][0], docs_results['metadatas'][0]):
                relevant_docs.append({
                    "content": doc[:500],  # Limit content to avoid token overflow
                    "source": meta.get('source', 'Unknown'),
                    "page": meta.get('page', 'N/A')
                })
        
        return {
            "context_type": "docs",
            "instructions": "Answer based on the provided documentation. Be specific and reference the source documents when possible.",
            "relevant_docs": relevant_docs,
            "examples": [],
            "specific_guidance": "Use the documentation context to provide accurate, detailed answers."
        }
    
    def generate_prompt(self, message: str, intent: str, context: Dict[str, Any]) -> str:
        """Generate final prompt for the LLM with all context"""
        prompt_parts = []
        
        # System instructions
        prompt_parts.append("You are a helpful AI assistant.")
        prompt_parts.append(f"Intent detected: {intent}")
        prompt_parts.append(f"Instructions: {context['instructions']}")
        
        # Add specific guidance if available
        if context.get('specific_guidance'):
            prompt_parts.append(f"Specific guidance: {context['specific_guidance']}")
        
        # Add relevant documentation if available
        if context.get('relevant_docs'):
            prompt_parts.append("\nRelevant documentation:")
            for i, doc in enumerate(context['relevant_docs'], 1):
                prompt_parts.append(f"Doc {i} (Source: {doc['source']}, Page: {doc['page']}):")
                prompt_parts.append(doc['content'])
                prompt_parts.append("---")
        
        # Add examples if available
        if context.get('examples'):
            prompt_parts.append("\nRelevant examples:")
            for i, example in enumerate(context['examples'], 1):
                prompt_parts.append(f"Example {i}: {example}")
        
        # Add user message
        prompt_parts.append(f"\nUser message: {message}")
        prompt_parts.append("\nPlease provide a helpful response based on the context above.")
        
        return "\n".join(prompt_parts)
    
    def process_message(self, message: str, prompt: str = None) -> str:
        """Process message and generate response using LLM"""
        try:
            if prompt:
                # Use the generated prompt for LLM
                response = llm.complete(prompt)
                return str(response)
            else:
                # Fallback to simple responses if no prompt provided
                message_lower = message.lower()
                
                if "hello" in message_lower or "hi" in message_lower or "hola" in message_lower:
                    return "Hello! How can I help you today?"
                elif "how are you" in message_lower or "como estas" in message_lower:
                    return "I'm doing great, thank you for asking! How are you?"
                elif "bye" in message_lower or "goodbye" in message_lower or "adios" in message_lower:
                    return "Goodbye! Have a great day!"
                elif "?" in message:
                    return f"Interesting question about '{message}'. Let me help you think about that."
                else:
                    return f"I received your message: '{message}'. Is there something specific I can help you with?"
        except Exception as e:
            print(f"Error in LLM processing: {str(e)}")
            return "I'm sorry, I encountered an error while processing your request. Please try again."

