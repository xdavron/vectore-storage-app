from fastapi import APIRouter, BackgroundTasks, Query, UploadFile, File, HTTPException
from app.models.schemas import IngestRequest, IngestResponse
from app.services.vector_db_context import VectorDBContext
from app.services.strategies.qdrant_strategy import QdrantStrategy
from app.services.strategies.chromadb_strategy import ChromaDBStrategy
import uuid
import json


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


# Ingestion endpoint with database selection for uploading file
@router.post("/ingest/file", response_model=IngestResponse)
async def ingest_data(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(None),
    db: str = Query("qdrant", enum=["qdrant", "chromadb"])  # Choose DB via query param
):
    # Check if an uploaded file is provided. If so, process file.
    if file:
        if file.content_type != "application/json":
            raise HTTPException(status_code=400, detail="Only JSON files are supported.")
        try:
            contents = await file.read()
            data = json.loads(contents)
            # Expecting the JSON file to contain at least a 'text' field and optionally 'metadata'
            metadata = data.pop("metadata", {})
            text = json.dumps(data)
            if not text:
                raise HTTPException(status_code=400, detail="JSON file must contain a 'text' field.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing file: {e}")
    else:
        raise HTTPException(status_code=400, detail="No input provided. Provide JSON body or file upload.")

    task_id = uuid.uuid4()

    # Dynamically set the strategy
    context = VectorDBContext(QdrantStrategy() if db == "qdrant" else ChromaDBStrategy())
    background_tasks.add_task(process_ingestion, context, text, metadata)

    return IngestResponse(task_id=task_id, status="Processing")
