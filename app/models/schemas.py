from pydantic import BaseModel, Field
from typing import Optional


class Base64AudioRequest(BaseModel):
    language: str = Field(..., example="English")
    audioFormat: str = Field(..., example="mp3")
    audioBase64: str = Field(..., description="Base64 encoded MP3 audio")


class VoiceDetectionResponse(BaseModel):
    status: str = "success"
    language: str
    classification: str
    confidenceScore: float
    explanation: Optional[str] = None


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
