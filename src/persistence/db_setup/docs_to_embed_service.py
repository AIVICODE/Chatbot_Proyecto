"""
Service for processing PDF documents and converting them to embeddings
"""
import os
import re
from typing import List
import PyPDF2
from pathlib import Path
from llm import embed_model


class DocsToEmbedService:
    """Service for processing PDF documents and storing them as embeddings"""
    
    def __init__(self):
        """Initialize the document embedding service"""
        self.model = embed_model

        BASE_DIR = Path(__file__).parent # src/persistence/db_setup
        self.docs_path = BASE_DIR / "data" / "docs"
        self.chunk_counter = 0
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
        return text
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from a TXT file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading TXT {file_path}: {e}")
            return ""
    
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
    
    def process_docs(self):
        """Process all PDF and TXT files in the docs folder"""
        if not os.path.exists(self.docs_path):
            print(f"Docs folder not found: {self.docs_path}")
            return

        from persistence.db_start import db_start
        vector_service = db_start()

        # Buscar archivos PDF y TXT (corregido con tupla)
        files = [f for f in os.listdir(self.docs_path) if f.endswith(('.pdf', '.txt'))]
        print("Files found:", files)

        for file in files:
            file_path = os.path.join(self.docs_path, file)
            print(f"Processing: {file}")

            if file.endswith('.pdf'):
                text = self.extract_text_from_pdf(file_path)
            elif file.endswith('.txt'):
                text = self.extract_text_from_txt(file_path)
            else:
                continue

            print(f"Extracted {len(text)} characters from {file}")

            if text:
                chunks = self.chunk_text(text, max_length=500)

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
                            "source": file,
                            "chunk": i,
                            "total_chunks": len(chunks)
                        }]
                    )
                    self.chunk_counter += 1

                print(f"✅ Added {len(chunks)} chunks from {file}")

        print("✅ All embeddings generated and stored in ChromaDB")
