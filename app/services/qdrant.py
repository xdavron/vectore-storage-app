import json

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from app.core.config import settings  # Assuming Qdrant host/port are in .env
import uuid
from app.services.embedding import VECTOR_SIZE  # Dynamically set vector size
import numpy as np
DEFAULT_COLLECTION = settings.DEFAULT_COLLECTION

# Qdrant client initialization
qdrant_client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

# COLLECTION_NAME = "vector_data"


def create_collection_if_not_exists(collection_name: str = DEFAULT_COLLECTION):
    """Check if the collection exists and create it if necessary."""
    try:
        # Attempt to fetch collection info
        qdrant_client.get_collection(collection_name=collection_name)
    except Exception:
        # If the collection doesn't exist, create it with the proper vector size.
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )


# Insert data into Qdrant
def insert_into_qdrant(vector: list, metadata: dict, collection_name: str = DEFAULT_COLLECTION) -> str:
    # Ensure the collection exists
    create_collection_if_not_exists()

    point_id = str(uuid.uuid4())
    #  Ideal for Individual or Small Batch Inserts
    #  Insert or update a small number of points (even just one).

    qdrant_client.upsert(
        collection_name=collection_name,
        points=[PointStruct(id=point_id, vector=vector, payload=metadata)],
    )
    # print(vector)
    # payload = map(json.loads, metadata.get('data'))
    # qdrant_client.upload_collection(
    #     collection_name=COLLECTION_NAME,
    #     vectors=[vector],
    #     payload=metadata.get('data'),
    #     ids=None,
    #     batch_size=256
    # )
    return point_id


# Search in Qdrant
def search_qdrant(vector: list, top_k: int, collection_name: str = DEFAULT_COLLECTION) -> list:
    results = qdrant_client.query_points(
        collection_name=collection_name,
        query=vector,
        limit=top_k
    ).points
    print(results)
    return [{"id": res.id, "score": res.score, "metadata": res.payload} for res in results]


def insert_into_qdrant_bulk(vectors: list, payloads: list, collection_name: str = DEFAULT_COLLECTION, batch_size: int = 256):
    """Bulk insert vectors and their payloads into Qdrant."""
    create_collection_if_not_exists(collection_name)
    vectors = np.array(vectors)
    qdrant_client.upload_collection(
        collection_name=collection_name,
        vectors=vectors,
        payload=payloads,
        ids=None,  # Auto-generate IDs
        batch_size=batch_size
    )