"""
Script to process intent data and convert them to embeddings
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.intent_to_embed_service import IntentToEmbedService

if __name__ == "__main__":
    
    # Initialize the service
    intent_service = IntentToEmbedService()
    
    # Process all intent training data
    intent_service.process_intents()
