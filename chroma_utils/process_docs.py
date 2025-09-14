"""
Script to process PDF documents and convert them to embeddings
"""
from src.services.docs_to_embed_service import DocsToEmbedService

if __name__ == "__main__":
    
    # Initialize the service
    docs_service = DocsToEmbedService()
    
    # Process all PDFs in the docs folder
    docs_service.process_pdfs()
