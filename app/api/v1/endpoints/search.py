from fastapi import APIRouter, Query
from app.models.schemas import SearchRequest, SearchResponse
from app.services.vector_db_context import VectorDBContext
from app.services.strategies.qdrant_strategy import QdrantStrategy
from app.services.strategies.chromadb_strategy import ChromaDBStrategy
from app.core.config import settings
DEFAULT_COLLECTION = settings.DEFAULT_COLLECTION

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
async def search_data(
        request: SearchRequest,
        collection_name: str = Query(None, description="Optional collection name; default is used if not provided."),
        db: str = Query("qdrant", enum=["qdrant", "chromadb"])  # Choose DB via query param
):
    if not collection_name:
        collection_name = DEFAULT_COLLECTION
    # Dynamically set the strategy
    context = VectorDBContext(QdrantStrategy() if db == "qdrant" else ChromaDBStrategy())
    results = context.search_data(request.query, request.top_k, collection_name=collection_name)

    return SearchResponse(results=results)
