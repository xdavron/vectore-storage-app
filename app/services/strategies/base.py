from abc import ABC, abstractmethod
from typing import List, Dict


class VectorDBStrategy(ABC):
    @abstractmethod
    def insert_data(self, text: str, metadata: dict, collection_name: str) -> str:
        pass

    @abstractmethod
    def search_data(self, query: str, top_k: int, collection_name: str) -> list:
        pass

    @abstractmethod
    def insert_bulk_data(self, items: List[Dict], collection_name: str) -> None:
        """
        Insert multiple items in bulk.
        Each item should be a dict with a "text" field and optional "metadata".
        """
        pass
