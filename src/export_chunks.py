"""
Export all chunks from docs, sql, and intent collections to txt files.
Run: py src/export_chunks.py
"""
from persistence.db_start import db_start

if __name__ == "__main__":
    service = db_start(setup_mode=False)
    service.export_chunks("docs")
    service.export_chunks("sql")
    service.export_chunks("intent")
