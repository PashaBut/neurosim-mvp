from pydantic import BaseModel
from typing import List, Optional

class UploadResponse(BaseModel):
    file_id: str
    user_id: str
    filename: str
    status: str
    message: str

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    question: str
    answer: str
    sources_used: int
    user_id: str

class HealthResponse(BaseModel):
    status: str
    model: str
    security_level: str
    vector_db_connected: bool
    privacy_features: List[str]
  
