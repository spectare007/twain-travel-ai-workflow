import os
from app.chroma_utils import connect_to_chromadb
from app.bedrock_embed import get_bedrock_embedding

COLLECTION_NAME = "innocents_abroad"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DIR = os.path.join(PROJECT_ROOT, "chroma_data")
client = connect_to_chromadb(CHROMA_DIR)

def search_book(query: str,
                chroma_dir: str = CHROMA_DIR,
                collection_name: str = COLLECTION_NAME,
                n_results: int = 3,
                preview_length: int = 300) -> str:
    """
    Search the book collection in ChromaDB for the most relevant chunks to the query.
    Returns a formatted string with the top results.
    """
    
    client = connect_to_chromadb(chroma_dir)
    collection = client.get_collection(collection_name)

    
    query_embedding = get_bedrock_embedding(query)

    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=['documents', 'metadatas']
    )

    
    if not results["documents"][0]:
        return "No relevant passages found in 'The Innocents Abroad.'"

    output = []
    for idx, doc in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][idx]
        summary = meta.get("summary", "")
        preview = doc[:preview_length] + ("..." if len(doc) > preview_length else "")
        output.append(
            f"Result {idx+1}:\n"
            f"Summary: {summary}\n"
            f"Passage: {preview}\n"
        )
    return "\n".join(output)

