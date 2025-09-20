import chromadb
from chromadb.config import Settings
import os

def connect_to_chromadb(chroma_dir: str = None) -> chromadb.PersistentClient:
    if chroma_dir is None:
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        chroma_dir = os.path.join(PROJECT_ROOT, "chroma_data")
    return chromadb.PersistentClient(path=chroma_dir)

def get_collection_stats(collection):
    """Get collection statistics efficiently."""
    count = collection.count()
    sample_data = None
    if count > 0:
        sample_data = collection.get(limit=1, include=['documents', 'metadatas'])
    return {
        'count': count,
        'sample_metadata_keys': list(sample_data['metadatas'][0].keys()) if sample_data and sample_data['metadatas'] else [],
        'sample_doc_length': len(sample_data['documents'][0]) if sample_data and sample_data['documents'] else 0
    }