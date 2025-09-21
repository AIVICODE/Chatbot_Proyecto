"""
Start script to initialize ChromaDB with embeddings
"""
import os
from pathlib import Path
import chromadb
from .db_setup.docs_to_embed_service import DocsToEmbedService
from .db_setup.intent_to_embed_service import IntentToEmbedService
from llm import embed_model

class db_start:
    """Service for managing vector embeddings with ChromaDB"""

    def __init__(self, setup_mode: bool = True):
        self.model = embed_model

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DB_DIR = os.path.join(BASE_DIR, "chroma_db")

        self.client = chromadb.PersistentClient(path=DB_DIR)

        if setup_mode:
            self.docs_collection = self.client.get_or_create_collection("docs")
            self.sql_collection = self.client.get_or_create_collection("sql")
            self.intent_collection = self.client.get_or_create_collection("intent")
        else:
            self.docs_collection = self.client.get_collection("docs")
            self.sql_collection = self.client.get_collection("sql")
            self.intent_collection = self.client.get_collection("intent")

    def export_chunks(self, collection_name: str, limit: int = 100, output_file: str = None):
        """Export chunks from a collection to a txt file"""
        collection = getattr(self, f"{collection_name}_collection", None)
        if collection is None:
            print(f"Collection '{collection_name}' not found.")
            return
        results = collection.get(limit=limit, include=["documents", "metadatas"])
        if not output_file:
            output_file = f"{collection_name}_chunks.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"=== CHUNKS EXPORT - Collection: {collection_name} ===\n")
            f.write(f"Total chunks retrieved: {len(results['documents'])}\n")
            f.write("="*60 + "\n\n")
            for i, (doc, metadata) in enumerate(zip(results['documents'], results['metadatas'])):
                f.write(f"CHUNK #{i+1}\n")
                f.write(f"Source: {metadata.get('source', 'Unknown')}\n")
                f.write(f"Chunk ID: {metadata.get('chunk', 'Unknown')}\n")
                f.write(f"Length: {len(doc)} characters\n")
                f.write("-" * 40 + "\n")
                f.write(f"{doc}\n")
                f.write("-" * 40 + "\n\n")
        print(f"✅ {len(results['documents'])} chunks exported to {output_file}")