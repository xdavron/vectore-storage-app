import json

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from app.core.config import settings  # Assuming Qdrant host/port are in .env
import uuid
from app.services.embedding import VECTOR_SIZE  # Dynamically set vector size

# Qdrant client initialization
qdrant_client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

COLLECTION_NAME = "vector_data"


def create_collection_if_not_exists():
    """Check if the collection exists and create it if necessary."""
    try:
        # Attempt to fetch collection info
        qdrant_client.get_collection(collection_name=COLLECTION_NAME)
    except Exception:
        # If the collection doesn't exist, create it with the proper vector size.
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )


# Insert data into Qdrant
def insert_into_qdrant(vector: list, metadata: dict) -> str:
    # Ensure the collection exists
    create_collection_if_not_exists()

    point_id = str(uuid.uuid4())
    #  Ideal for Individual or Small Batch Inserts
    #  Insert or update a small number of points (even just one).

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
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
def search_qdrant(vector: list, top_k: int) -> list:
    results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=top_k
    ).points
    print(results)
    return [{"id": res.id, "score": res.score, "metadata": res.payload} for res in results]