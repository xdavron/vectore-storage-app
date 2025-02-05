from fastapi import APIRouter, BackgroundTasks, Query, UploadFile, File, HTTPException
from app.models.schemas import IngestRequest, IngestResponse
from app.services.vector_db_context import VectorDBContext
from app.services.strategies.qdrant_strategy import QdrantStrategy
from app.services.strategies.chromadb_strategy import ChromaDBStrategy
from app.core.config import settings
DEFAULT_COLLECTION = settings.DEFAULT_COLLECTION
import uuid
import json


router = APIRouter()


# Background task for data ingestion
async def process_ingestion(context: VectorDBContext, text: str, metadata: dict, collection_name: str):
    context.insert_data(text, metadata, collection_name)


async def process_bulk_ingestion(items: list, context: VectorDBContext, collection_name: str):
    context.insert_bulk_data(items, collection_name)


# Ingestion endpoint with database selection
@router.post("/ingest", response_model=IngestResponse)
async def ingest_data(
    request: IngestRequest,
    background_tasks: BackgroundTasks,
    collection_name: str = Query(None, description="Optional collection name; default is used if not provided."),
    db: str = Query("qdrant", enum=["qdrant", "chromadb"])  # Choose DB via query param
):
    task_id = uuid.uuid4()

    if not collection_name:
        collection_name = DEFAULT_COLLECTION

    # Dynamically set the strategy
    context = VectorDBContext(QdrantStrategy() if db == "qdrant" else ChromaDBStrategy())
    background_tasks.add_task(process_ingestion, context, request.text, request.metadata, collection_name)

    return IngestResponse(task_id=task_id, status="Processing")


# Ingestion endpoint with database selection for uploading file
@router.post("/ingest/file", response_model=IngestResponse)
async def ingest_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(None),
    collection_name: str = Query(None, description="Optional collection name; default is used if not provided."),
    db: str = Query("qdrant", enum=["qdrant", "chromadb"])  # Choose DB via query param
):
    # Check if an uploaded file is provided. If so, process file.
    # if file:
    #     if file.content_type != "application/json":
    #         raise HTTPException(status_code=400, detail="Only JSON files are supported.")
    #     try:
    #         contents = await file.read()
    #         data = json.loads(contents)
    #         # Expecting the JSON file to contain at least a 'text' field and optionally 'metadata'
    #         metadata = data.pop("metadata", {})
    #         if not metadata:
    #             metadata = data
    #         text = json.dumps(data)
    #         if not text:
    #             raise HTTPException(status_code=400, detail="JSON file must contain a 'text' field.")
    #     except Exception as e:
    #         raise HTTPException(status_code=400, detail=f"Error processing file: {e}")
    # else:
    #     raise HTTPException(status_code=400, detail="No input provided. Provide JSON body or file upload.")
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {e}")

    # Try to parse as a JSON array first.
    try:
        items = json.loads(contents)
        if not isinstance(items, list):
            raise ValueError("JSON is not an array.")
    except Exception:
        # If not an array, treat as newline-delimited JSON.
        items = []
        try:
            for line in contents.decode().splitlines():
                if line.strip():
                    items.append(json.loads(line))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing JSON lines: {e}")

        if not items:
            raise HTTPException(status_code=400, detail="No valid items found in the file.")

    if not collection_name:
        collection_name = DEFAULT_COLLECTION

    task_id = uuid.uuid4()

    # Dynamically set the strategy
    context = VectorDBContext(QdrantStrategy() if db == "qdrant" else ChromaDBStrategy())
    background_tasks.add_task(process_bulk_ingestion, items, context, collection_name)

    return IngestResponse(task_id=task_id, status="Bulk processing started")
