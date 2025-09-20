import os
import json
from tqdm import tqdm
import chromadb
from chromadb.config import Settings

from app.book_preprocess import clean_gutenberg_text, chunk_text_by_paragraph
from app.bedrock_converse import get_nova_pro_metadata
from app.bedrock_embed import get_bedrock_embedding

def flatten_metadata(meta: dict) -> dict:
    """
    Convert any list values in metadata to comma-separated strings.
    """
    flat = {}
    for k, v in meta.items():
        if isinstance(v, list):
            flat[k] = ", ".join(str(x) for x in v)
        else:
            flat[k] = str(v)  # Ensure all values are strings
    return flat

def main(
    ebook_path=None,
    chroma_dir=None,
    collection_name="innocents_abroad",
    batch_size=10
):
    # Set robust paths
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if ebook_path is None:
        ebook_path = os.path.join(PROJECT_ROOT, "data", "ebook.txt")
    if chroma_dir is None:
        chroma_dir = os.path.join(PROJECT_ROOT, "chroma_data")
    
    print(f"Current working directory: {os.getcwd()}")
    print(f"ChromaDB directory will be: {os.path.abspath(chroma_dir)}")
    print(f"Ebook path: {os.path.abspath(ebook_path)}")
    
    # Check if ebook file exists
    if not os.path.exists(ebook_path):
        print(f"ERROR: Ebook file not found at {ebook_path}")
        return
    
    # Create the directory if it doesn't exist
    os.makedirs(chroma_dir, exist_ok=True)
    print(f"Created/ensured directory exists: {chroma_dir}")
    
    try:
        # 1. Start ChromaDB client with persistence
        print("Initializing ChromaDB client...")
        client = chromadb.PersistentClient(path=chroma_dir)  # Use PersistentClient instead
        print("ChromaDB client created successfully")
        
        # 2. Create/get collection (will create if not exists)
        print(f"Creating/getting collection: {collection_name}")
        collection = client.get_or_create_collection(collection_name)
        print(f"Collection created/retrieved: {collection.name}")
        
        # 3. Load and preprocess the book
        print("Loading and preprocessing book...")
        with open(ebook_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        
        clean_text = clean_gutenberg_text(raw_text)
        chunks = chunk_text_by_paragraph(clean_text)
        
        print(f"Processing {len(chunks)} chunks...")
        
        # 4. Process and insert in small batches
        batch_ids, batch_docs, batch_embs, batch_metas = [], [], [], []
        
        for i, chunk in enumerate(tqdm(chunks, desc="Embedding and metadata")):
            try:
                # Get metadata and embedding
                meta = get_nova_pro_metadata(chunk)
                meta["chunk_id"] = i
                meta["text_preview"] = chunk[:60]
                embedding = get_bedrock_embedding(chunk)
                
                batch_ids.append(str(i))
                batch_docs.append(chunk)
                batch_embs.append(embedding)
                batch_metas.append(flatten_metadata(meta))
                
                # Insert batch when full or at the end
                if len(batch_ids) == batch_size or i == len(chunks) - 1:
                    print(f"Inserting batch of {len(batch_ids)} items...")
                    collection.add(
                        ids=batch_ids,
                        documents=batch_docs,
                        embeddings=batch_embs,
                        metadatas=batch_metas
                    )
                    print(f"Stored batch up to chunk {i+1}/{len(chunks)}")
                    
                    # Clear batches
                    batch_ids, batch_docs, batch_embs, batch_metas = [], [], [], []
                    
                    # Verify data is being stored
                    count = collection.count()
                    print(f"Total documents in collection: {count}")
                    
            except Exception as e:
                print(f"Error processing chunk {i}: {str(e)}")
                continue
        
        # Final count
        final_count = collection.count()
        print(f"Final count: {final_count} chunks stored in ChromaDB")
        
        # Check if directory was created and has content
        if os.path.exists(chroma_dir):
            print(f"✓ ChromaDB directory exists at: {os.path.abspath(chroma_dir)}")
            files = os.listdir(chroma_dir)
            print(f"Files in ChromaDB directory: {files}")
        else:
            print(f"✗ ChromaDB directory NOT found at: {os.path.abspath(chroma_dir)}")
        
        # 5. Test a query
        if final_count > 0:
            test_query = "What did Mark Twain think about the Sphinx?"
            print(f"\nTesting retrieval for: '{test_query}'")
            try:
                results = collection.query(
                    query_texts=[test_query],
                    n_results=min(3, final_count)
                )
                for idx, doc in enumerate(results["documents"][0]):
                    print(f"\nResult {idx+1}:\n{doc[:200]}...")
                    print(f"Metadata: {results['metadatas'][0][idx]}")
            except Exception as e:
                print(f"Error during query: {str(e)}")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()