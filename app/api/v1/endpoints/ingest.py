from fastapi import APIRouter, BackgroundTasks, Query
from app.models.schemas import IngestRequest, IngestResponse
from app.services.vector_db_context import VectorDBContext
from app.services.strategies.qdrant_strategy import QdrantStrategy
from app.services.strategies.chromadb_strategy import ChromaDBStrategy
import uuid


router = APIRouter()


# Background task for data ingestion
async def process_ingestion(context: VectorDBContext, text: str, metadata: dict):
    context.insert_data(text, metadata)


# Ingestion endpoint with database selection
@router.post("/ingest", response_model=IngestResponse)
async def ingest_data(
    request: IngestRequest,
    background_tasks: BackgroundTasks,
    db: str = Query("qdrant", enum=["qdrant", "chromadb"])  # Choose DB via query param
):
    task_id = uuid.uuid4()

    # Dynamically set the strategy
    context = VectorDBContext(QdrantStrategy() if db == "qdrant" else ChromaDBStrategy())
    background_tasks.add_task(process_ingestion, context, request.text, request.metadata)

    return IngestResponse(task_id=task_id, status="Processing")
