from abc import ABC, abstractmethod
from typing import List, Dict


class VectorDBStrategy(ABC):
    @abstractmethod
    def insert_data(self, text: str, metadata: dict) -> str:
        pass

    @abstractmethod
    def search_data(self, query: str, top_k: int) -> list:
        pass

    @abstractmethod
    def insert_bulk_data(self, items: List[Dict]) -> None:
        """
        Insert multiple items in bulk.
        Each item should be a dict with a "text" field and optional "metadata".
        """
        pass
