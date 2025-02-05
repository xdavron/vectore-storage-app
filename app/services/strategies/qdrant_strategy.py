from app.services.qdrant import insert_into_qdrant, search_qdrant, insert_into_qdrant_bulk
from app.services.embedding import generate_embedding
from app.services.strategies.base import VectorDBStrategy
from typing import List, Dict


class QdrantStrategy(VectorDBStrategy):
    def insert_data(self, text: str, metadata: dict) -> str:
        vector = generate_embedding(text)
        return insert_into_qdrant(vector, metadata)

    def search_data(self, query: str, top_k: int) -> list:
        vector = generate_embedding(query)
        return search_qdrant(vector, top_k)

    def insert_bulk_data(self, items: List[Dict]) -> None:
        vectors = []
        payloads = []
        for idx, item in enumerate(items):
            text = item.get("text")
            if not text:
                continue
            metadata = item.get("metadata", {})
            # Provide default metadata if missing
            if not metadata:
                metadata = {"source": f"line_{idx}"}
            metadata["text"] = text  # Save original text with metadata
            vector = generate_embedding(text)
            vectors.append(vector)
            payloads.append(metadata)
        if not vectors:
            raise ValueError("No valid items found for bulk insertion.")
        print(vectors, payloads)
        insert_into_qdrant_bulk(vectors, payloads)
