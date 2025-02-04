from fastapi import APIRouter, Query
from app.models.schemas import SearchRequest, SearchResponse
from app.services.vector_db_context import VectorDBContext
from app.services.strategies.qdrant_strategy import QdrantStrategy
from app.services.strategies.chromadb_strategy import ChromaDBStrategy

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
async def search_data(
        request: SearchRequest,
        db: str = Query("qdrant", enum=["qdrant", "chromadb"])  # Choose DB via query param
):
    # Dynamically set the strategy
    context = VectorDBContext(QdrantStrategy() if db == "qdrant" else ChromaDBStrategy())
    results = context.search_data(request.query, request.top_k)

    return SearchResponse(results=results)
