"""
Vector service for storing and retrieving embeddings using ChromaDB
"""
import chromadb
import os
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import uuid


class VectorService:
    """Service for managing vector embeddings with ChromaDB"""
    
    def __init__(self):
        """Initialize the vector service"""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # Create the 3 collections
        self.docs_collection = self.client.get_or_create_collection("docs")
        self.sql_collection = self.client.get_or_create_collection("sql")
        self.intent_collection = self.client.get_or_create_collection("intent")
    
    def view_chunks(self, collection_name: str = "docs", limit: int = 5, output_file: str = "chunks_review.txt"):
        """View some chunks from the specified collection and save to txt file"""
        collection = getattr(self, f"{collection_name}_collection")
        
        # Get some chunks from the collection
        results = collection.get(limit=limit, include=["documents", "metadatas"])
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"=== CHUNKS REVIEW - Collection: {collection_name} ===\n")
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
        
        print(f"✅ {len(results['documents'])} chunks saved to {output_file}")
        return results
