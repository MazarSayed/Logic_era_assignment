"""
Pydantic models for the Webpage Summarizer API
"""

from pydantic import BaseModel, HttpUrl
from typing import Optional

class SummarizeRequest(BaseModel):
    """Request model for webpage summarization"""
    url: HttpUrl

class SummarizeResponse(BaseModel):
    """Response model for webpage summarization"""
    summary: str
    main_topic: str

class ConversationRequest(BaseModel):
    """Request model for conversation questions"""
    question: str
    session_id: str

class ConversationResponse(BaseModel):
    """Response model for conversation answers"""
    answer: str
    session_id: str

class ProviderInfo(BaseModel):
    """Model for provider information"""
    models: list[str]
    default_model: str

class ProvidersResponse(BaseModel):
    """Response model for available providers"""
    available_providers: dict[str, ProviderInfo]
    total_providers: int

class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    service: str
