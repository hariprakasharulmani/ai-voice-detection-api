"""Pydantic models for request/response validation."""
from pydantic import BaseModel, HttpUrl, Field
from typing import Literal, Optional


class VoiceDetectionRequest(BaseModel):
    """Request model for voice detection endpoint."""
    audio_url: HttpUrl = Field(..., description="URL of the audio file to analyze")
    language: Optional[str] = Field(None, description="Optional language code (e.g., 'en', 'es')")


class VoiceDetectionResponse(BaseModel):
    """Response model for voice detection endpoint."""
    prediction: Literal["AI_GENERATED", "HUMAN"] = Field(..., description="Detection result")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    language: str = Field(..., description="Detected or specified language")
    model_version: str = Field(..., description="Model version used for inference")
    processing_time_ms: int = Field(..., ge=0, description="Processing time in milliseconds")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")

