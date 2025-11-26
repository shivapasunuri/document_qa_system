from pydantic import BaseModel
from typing import Optional, List

class QueryRequest(BaseModel):
    question: str
    collection_name: Optional[str] = "default"

class QueryResponse(BaseModel):
    answer: Optional[str]
    status: str
    error: Optional[str]
    question: str

class DocumentUploadResponse(BaseModel):
    message: str
    documents_processed: int
    collection_name: str