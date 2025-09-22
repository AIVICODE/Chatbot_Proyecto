"""
Initialization script for ChromaDB collections and embeddings
Run this from the project root: py src/init_db.py
"""
from persistence.db_start import db_start
from persistence.db_setup.docs_to_embed_service import DocsToEmbedService
from persistence.db_setup.intent_to_embed_service import IntentToEmbedService

if __name__ == "__main__":
    service = db_start(setup_mode=True)

    docs_service = DocsToEmbedService()
    docs_service.process_docs()
    
    intent_service = IntentToEmbedService()
    intent_service.process_intents()

    print("✅ ChromaDB initialized")
