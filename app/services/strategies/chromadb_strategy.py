from app.services.chromadb import insert_into_chromadb, search_chromadb
from app.services.strategies.base import VectorDBStrategy


class ChromaDBStrategy(VectorDBStrategy):
    def insert_data(self, text: str, metadata: dict) -> str:
        return insert_into_chromadb(text, metadata)

    def search_data(self, query: str, top_k: int) -> list:
        return search_chromadb(query, top_k)