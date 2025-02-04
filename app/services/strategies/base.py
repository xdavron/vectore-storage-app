from abc import ABC, abstractmethod


class VectorDBStrategy(ABC):
    @abstractmethod
    def insert_data(self, text: str, metadata: dict) -> str:
        pass

    @abstractmethod
    def search_data(self, query: str, top_k: int) -> list:
        pass