# models.py
from llama_index.llms.google_genai import GoogleGenAI
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("❌ GOOGLE_API_KEY no encontrada en el archivo .env")

# Instancia global de embeddings
embed_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

# Instancia global de LLM
llm = GoogleGenAI(
    model="gemini-2.0-flash",
    api_key=google_api_key
)
