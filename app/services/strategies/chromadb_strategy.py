from typing import List, Dict

from app.services.chromadb import insert_into_chromadb, search_chromadb, insert_into_chromadb_bulk
from app.services.chromadb import save_to_chroma, load_history_from_chroma
from app.services.strategies.base import VectorDBStrategy


class ChromaDBStrategy(VectorDBStrategy):
    def insert_data(self, text: str, metadata: dict, collection_name: str) -> str:
        return insert_into_chromadb(text, metadata, collection_name)

        # chat_id = metadata.get("chat_id", "default_chat")
        # # Construct a single-message list; we pass the role if provided.
        # message = {"content": text, "role": metadata.get("role", "unknown")}
        # save_to_chroma(chat_id, [message])
        # return f"{chat_id}_0"
        # return insert_into_chromadb(text, metadata, collection_name=collection_name)

    def search_data(self, query: str, top_k: int, collection_name: str) -> list:
        return search_chromadb(query, top_k, collection_name)

        # return load_history_from_chroma(query, top_k, collection_name=collection_name)
        # return search_chromadb(query, top_k, collection_name=collection_name)

    def insert_bulk_data(self, items: List[Dict], collection_name: str) -> None:
        texts = []
        payloads = []
        for idx, item in enumerate(items):
            text = item.get("text")
            if not text:
                continue  # Skip items without text
            metadata = item.get("metadata", {"source": f"line_{idx}"})
            # Optionally include the text in metadata if needed.
            metadata["text"] = text
            texts.append(text)
            payloads.append(metadata)
        if not texts:
            raise ValueError("No valid items found for bulk insertion.")
        insert_into_chromadb_bulk(texts, payloads, collection_name)

        # for item in items:
        #     chat_id = item.get("chat_id", "default_chat")
        #     groups.setdefault(chat_id, []).append({
        #         "content": item.get("text"),
        #         "role": item.get("role", "unknown")
        #     })
        # print(items)
        # for chat_id, messages in groups.items():
        #     print(chat_id, messages)
        # save_to_chroma(chat_id, messages, collection_name=collection_name)
