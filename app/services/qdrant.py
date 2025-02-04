from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from app.core.config import settings  # Assuming Qdrant host/port are in .env
import uuid

# Qdrant client initialization
qdrant_client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

COLLECTION_NAME = "vector_data"


# Insert data into Qdrant
def insert_into_qdrant(vector: list, metadata: dict) -> str:
    point_id = str(uuid.uuid4())
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[PointStruct(id=point_id, vector=vector, payload=metadata)]
    )
    return point_id


# Search in Qdrant
def search_qdrant(vector: list, top_k: int) -> list:
    results = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=top_k
    )
    return [{"id": res.id, "score": res.score, "payload": res.payload} for res in results]