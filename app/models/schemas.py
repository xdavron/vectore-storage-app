from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID


# Request schema for data ingestion
class IngestRequest(BaseModel):
    text: str
    metadata: Optional[dict] = Field(default={})


# Response schema after ingestion
class IngestResponse(BaseModel):
    task_id: UUID
    status: str


# Schema for search queries
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5  # Number of similar results to return


# Response schema for search results
class SearchResult(BaseModel):
    id: str
    score: float
    metadata: Optional[dict]


class SearchResponse(BaseModel):
    results: List[SearchResult]
