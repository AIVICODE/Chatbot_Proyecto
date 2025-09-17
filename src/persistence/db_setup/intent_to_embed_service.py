"""
Service for processing intent data and converting them to embeddings
"""
import os
import sys
from sentence_transformers import SentenceTransformer

# Add the project root to the path to import from chroma_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from .data.intents_data import INTENT_TRAINING_DATA


class IntentToEmbedService:
    """Service for processing intent data and storing them as embeddings"""
    
    def __init__(self):
        """Initialize the intent embedding service"""
        self.model = SentenceTransformer('all-mpnet-base-v2')
        self.chunk_counter = 0
    
    def process_intents(self):
        """Process all intent training data (only sql and docs, ambiguo is determined by distance)"""
        from persistence.db_start import db_start
        vector_service = db_start()

        print("Processing intent training data...")
        
        # Extract texts for batch embedding generation
        texts = [item["text"] for item in INTENT_TRAINING_DATA]
        
        # Generate embeddings in batch for efficiency
        embeddings = self.model.encode(
            texts, 
            show_progress_bar=True, 
            convert_to_numpy=True, 
            normalize_embeddings=True
        )
        
        # Store each intent with its embedding
        for i, item in enumerate(INTENT_TRAINING_DATA):
            vector_service.intent_collection.add(
                ids=[f"intent_{self.chunk_counter}"],
                documents=[item["text"]],
                embeddings=[embeddings[i].tolist()],
                metadatas=[{
                    "intent": item["intent"],
                    "example_id": i,
                    "total_examples": len(INTENT_TRAINING_DATA)
                }]
            )
            self.chunk_counter += 1
        
        print(f"✅ Added {len(INTENT_TRAINING_DATA)} intent examples to ChromaDB")
        
        # Show summary by intent type
        intent_counts = {}
        for item in INTENT_TRAINING_DATA:
            intent = item["intent"]
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        print("\n📊 Intent distribution:")
        for intent, count in intent_counts.items():
            print(f"  - {intent}: {count} examples")
        
        print("✅ Intent embeddings generated and stored in ChromaDB")
        print("ℹ️  Note: 'ambiguo' intent will be determined automatically based on distance thresholds")
