"""
Master script to load all vector collections
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.docs_to_embed_service import DocsToEmbedService
from src.services.intent_to_embed_service import IntentToEmbedService

def load_all_collections():
    """Load all vector collections: docs and intents"""
    
    print("🚀 Starting to load all vector collections...\n")
    
    # 1. Load documents
    print("📄 Processing documents...")
    docs_service = DocsToEmbedService()
    docs_service.process_pdfs()
    
    print("\n" + "="*50 + "\n")
    
    # 2. Load intents
    print("🎯 Processing intents...")
    intent_service = IntentToEmbedService()
    intent_service.process_intents()
    
    print("\n" + "="*50)
    print("✅ All collections loaded successfully!")
    print("Available collections: docs, sql, intent")
    print("ℹ️  'ambiguo' classification will be determined by distance thresholds during query time")

if __name__ == "__main__":
    load_all_collections()
