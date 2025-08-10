"""
Pydantic models for the Webpage Summarizer API
"""

from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class SummarizeRequest(BaseModel):
    """Request model for webpage summarization"""
    url: HttpUrl
    provider: Optional[str] = None
    model: Optional[str] = None

class StructuredSummary(BaseModel):
    """Structured output schema for LLM summarization"""
    topic: str = Field(
        description="Main topic in 3-6 descriptive words that identifies the subject matter",
        min_length=3,
        max_length=50
    )
    summary: str = Field(
        description="Comprehensive and extremely detailed summary (8-10 substantial paragraphs, 300-500+ words minimum) with specific facts, dates, numbers, quotes, and comprehensive coverage of all aspects",
        min_length=300
    )

class SummarizeResponse(BaseModel):
    """Response model for webpage summarization"""
    summary: str
    main_topic: str
    session_id: Optional[str] = None

class ChatRequest(BaseModel):
    """Request model for chat with summary"""
    session_id: str
    question: str

class ChatResponse(BaseModel):
    """Response model for chat interaction"""
    answer: str
    session_id: str

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
