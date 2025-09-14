"""
Script to view chunks from the vector database
"""
from src.services.vector_service import VectorService

if __name__ == "__main__":
    print("🔍 Reviewing chunks from vector database...")
    
    # Initialize the service
    vector_service = VectorService()
    
    # View 10 chunks from docs collection
    vector_service.view_chunks(collection_name="docs", limit=10, output_file="chunks_review.txt")
    
    print("📝 Check 'chunks_review.txt' to see how the chunking worked!")
