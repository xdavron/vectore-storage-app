import chromadb
from datetime import datetime
from app.core.config import settings
from app.services.embedding import generate_embeddings
import uuid
from typing import List, Dict
import os
from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction
DEFAULT_COLLECTION = settings.DEFAULT_COLLECTION

# embedding_function = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-ada-002")

# ChromaDB client initialization
client = chromadb.PersistentClient(path='./chroma_db')

# Use the generate_embeddings function from embedding.py as our embedding_function.
embedding_function = generate_embeddings


def create_or_get_collection(collection_name: str = DEFAULT_COLLECTION):
    return client.get_or_create_collection(
        name=collection_name,
        # embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"}
    )


def save_to_chroma(chat_id: str, messages: list, collection_name: str = DEFAULT_COLLECTION):
    """Сохранение сообщений в ChromaDB с уникальными идентификаторами для каждого сообщения"""
    # Should be passed 'chat_history' as name of collection
    collection = create_or_get_collection(collection_name)

    documents = []
    metadatas = []
    ids = []

    for i, msg in enumerate(messages):
        # Извлекаем контент сообщения напрямую из словаря
        if isinstance(msg, dict):
            content = msg.get("content", "")
            role = msg.get("role", "unknown")
        else:
            content = str(msg)
            role = "unknown"

        documents.append(content)
        metadatas.append({
            "chat_id": chat_id,
            "role": role,
            "timestamp": datetime.now().isoformat()
        })
        # Формируем уникальный идентификатор, добавляя индекс
        ids.append(f"{chat_id}_{i}")

    try:
        collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    except Exception as e:
        print(f"Error saving to ChromaDB: {str(e)}")
        raise


def load_history_from_chroma(chat_id: str, top_k: int = 100, collection_name: str = DEFAULT_COLLECTION) -> list:
    """
    Load chat history from Chromadb for a given chat_id.
    Returns a list of dicts with 'role' and 'content' keys.
    """
    collection = create_or_get_collection(collection_name)

    try:
        results = collection.get(
            where={"chat_id": chat_id},
            limit=top_k
        )
    except Exception as e:
        print(f"Error loading history: {str(e)}")
        return []
    return [{"doc": doc, "metadata": meta} for doc, meta in zip(results['documents'], results['metadatas'])]


# Insert data into ChromaDB
# def insert_into_chromadb(text: str, metadata: dict, collection_name: str = DEFAULT_COLLECTION) -> str:
#     collection = create_or_get_collection(collection_name)
#
#     doc_id = str(uuid.uuid4())
#     collection.add(documents=[text], ids=[doc_id], metadatas=[metadata])
#     return doc_id


# Search in ChromaDB
# def search_chromadb(query: str, top_k: int, collection_name: str = DEFAULT_COLLECTION) -> list:
#     collection = create_or_get_collection(collection_name)
#
#     results = collection.query(query_texts=[query], n_results=top_k)
#     return [{"id": res, "metadata": md} for res, md in zip(results["ids"][0], results["metadatas"][0])]


def insert_bulk_data(self, items: List[Dict]) -> None:
    # For demonstration, iterate over items individually.
    # In a real implementation, you might use a bulk API if available.
    for idx, item in enumerate(items):
        text = item.get("text")
        if not text:
            continue
        metadata = item.get("metadata", {})
        if not metadata:
            metadata = {"source": f"line_{idx}"}
        self.insert_data(text, metadata)


def insert_into_chromadb(text: str, metadata: dict, collection_name: str = DEFAULT_COLLECTION) -> str:
    """
    Insert a single document (text) into Chromadb with its associated metadata.
    Returns a generated document ID.
    """
    collection = create_or_get_collection(collection_name)
    doc_id = str(uuid.uuid4())
    try:
        collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
    except Exception as e:
        raise Exception(f"Error inserting into Chromadb: {str(e)}")
    return doc_id


def insert_into_chromadb_bulk(texts: list, payloads: list, collection_name: str = DEFAULT_COLLECTION,
                              batch_size: int = 256):
    """
    Bulk insert a list of documents (texts) with corresponding metadata (payloads) into Chromadb.
    The client automatically generates IDs.
    """
    collection = create_or_get_collection(collection_name)
    # (Chromadb's add method supports adding many documents at once.)
    try:
        collection.add(
            documents=texts,
            metadatas=payloads,
            ids=[str(uuid.uuid4()) for _ in texts]
        )
    except Exception as e:
        raise Exception(f"Error during bulk insertion into Chromadb: {str(e)}")


def search_chromadb(query: str, top_k: int, collection_name: str = DEFAULT_COLLECTION) -> list:
    """
    Search the collection for documents similar to the query text.
    Returns a list of results, each containing an 'id', 'score', and 'metadata'.
    """
    collection = create_or_get_collection(collection_name)
    try:
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
    except Exception as e:
        raise Exception(f"Error during search in Chromadb: {str(e)}")

    # Format the results (Chromadb returns a dict with lists for each field)
    res_list = []
    # Assuming results have keys: "ids", "documents", "metadatas", "distances"
    ids = results.get("ids", [[]])[0]
    distances = results.get("distances", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    for idx, _ in enumerate(ids):
        res_list.append({
            "id": ids[idx],
            "score": distances[idx],
            "metadata": metadatas[idx]
        })
    return res_list