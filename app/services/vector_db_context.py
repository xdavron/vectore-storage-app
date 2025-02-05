from app.services.strategies.qdrant_strategy import QdrantStrategy
from app.services.strategies.chromadb_strategy import ChromaDBStrategy
from app.services.strategies.base import VectorDBStrategy


class VectorDBContext:
    def __init__(self, strategy: VectorDBStrategy = QdrantStrategy()):  # Default is Qdrant
        self.strategy = strategy

    def set_strategy(self, strategy: VectorDBStrategy):
        self.strategy = strategy

    def insert_data(self, text: str, metadata: dict) -> str:
        return self.strategy.insert_data(text, metadata)

    def search_data(self, query: str, top_k: int) -> list:
        return self.strategy.search_data(query, top_k)

    def insert_bulk_data(self, items: list) -> None:
        return self.strategy.insert_bulk_data(items)
