"""
Service for processing PDF documents and converting them to embeddings
"""
import os
import re
import uuid
from typing import List, Dict
import PyPDF2
from sentence_transformers import SentenceTransformer


class DocsToEmbedService:
    """Service for processing PDF documents and storing them as embeddings"""
    
    def __init__(self):
        """Initialize the document embedding service"""
        self.model = SentenceTransformer('all-mpnet-base-v2')
        self.docs_path = "./docs"
        self.chunk_counter = 0
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
        return text
    
    def chunk_text(self, text: str, max_length: int = 500) -> List[str]:
        """Split text into chunks based on sentences, avoiding cutting ideas"""
        text = text.replace("\n", " ").strip()
        sentences = re.split(r'(?<=[.!?]) +', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > max_length:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def process_pdfs(self):
        """Process all PDF files in the docs folder"""
        if not os.path.exists(self.docs_path):
            print(f"Docs folder not found: {self.docs_path}")
            return
        
        from .vector_service import VectorService
        vector_service = VectorService()
        
        pdf_files = [f for f in os.listdir(self.docs_path) if f.endswith('.pdf')]
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.docs_path, pdf_file)
            print(f"Processing: {pdf_file}")
            
            text = self.extract_text_from_pdf(pdf_path)
            if text:
                chunks = self.chunk_text(text, max_length=500)
                
                # Generate embeddings in batch for efficiency
                embeddings = self.model.encode(
                    chunks, 
                    show_progress_bar=True, 
                    convert_to_numpy=True, 
                    normalize_embeddings=True
                )
                
                for i, chunk in enumerate(chunks):
                    vector_service.docs_collection.add(
                        ids=[f"chunk_{self.chunk_counter}"],
                        documents=[chunk],
                        embeddings=[embeddings[i].tolist()],
                        metadatas=[{
                            "source": pdf_file,
                            "chunk": i,
                            "total_chunks": len(chunks)
                        }]
                    )
                    self.chunk_counter += 1
                
                print(f"✅ Added {len(chunks)} chunks from {pdf_file}")
        
        print("✅ All embeddings generated and stored in ChromaDB")
