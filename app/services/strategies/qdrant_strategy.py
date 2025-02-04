from app.services.qdrant import insert_into_qdrant, search_qdrant
from app.services.embedding import generate_embedding
from app.services.strategies.base import VectorDBStrategy


class QdrantStrategy(VectorDBStrategy):
    def insert_data(self, text: str, metadata: dict) -> str:
        vector = generate_embedding(text)
        return insert_into_qdrant(vector, metadata)

    def search_data(self, query: str, top_k: int) -> list:
        vector = generate_embedding(query)
        return search_qdrant(vector, top_k)