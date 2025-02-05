from app.services.strategies.qdrant_strategy import QdrantStrategy
from app.services.strategies.chromadb_strategy import ChromaDBStrategy
from app.services.strategies.base import VectorDBStrategy


class VectorDBContext:
    def __init__(self, strategy: VectorDBStrategy = QdrantStrategy()):  # Default is Qdrant
        self.strategy = strategy

    def set_strategy(self, strategy: VectorDBStrategy):
        self.strategy = strategy

    def insert_data(self, text: str, metadata: dict, collection_name: str) -> str:
        return self.strategy.insert_data(text, metadata, collection_name)

    def search_data(self, query: str, top_k: int, collection_name: str) -> list:
        return self.strategy.search_data(query, top_k, collection_name)

    def insert_bulk_data(self, items: list, collection_name: str) -> None:
        return self.strategy.insert_bulk_data(items, collection_name)
