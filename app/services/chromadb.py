import chromadb
from app.core.config import settings
import uuid

# ChromaDB client initialization
client = chromadb.Client()
COLLECTION_NAME = "vector_data"
collection = client.get_or_create_collection(COLLECTION_NAME)

# Insert data into ChromaDB
def insert_into_chromadb(text: str, metadata: dict) -> str:
    doc_id = str(uuid.uuid4())
    collection.add(documents=[text], ids=[doc_id], metadatas=[metadata])
    return doc_id

# Search in ChromaDB
def search_chromadb(query: str, top_k: int) -> list:
    results = collection.query(query_texts=[query], n_results=top_k)
    return [{"id": res, "metadata": md} for res, md in zip(results["ids"][0], results["metadatas"][0])]