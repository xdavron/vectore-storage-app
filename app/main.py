from fastapi import FastAPI
from app.api.v1.endpoints import ingest, search
import uvicorn

app = FastAPI(title="Vector Storage App")

# API routing
app.include_router(ingest.router, prefix="/api/v1/ingest", tags=["Ingestion"])
app.include_router(search.router, prefix="/api/v1/search", tags=["Search"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Vector Storage App API"}


if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run(app, host="127.0.0.1", port=8000)