from pydantic import BaseModel, Field
from typing import Literal


class Base64AudioRequest(BaseModel):
    language: Literal["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
    audioFormat: Literal["mp3"]
    audioBase64: str


class VoiceDetectionResponse(BaseModel):
    status: Literal["success"]
    language: str
    classification: Literal["AI_GENERATED", "HUMAN"]
    confidenceScore: float = Field(ge=0.0, le=1.0)
    explanation: str


class ErrorResponse(BaseModel):
    status: Literal["error"]
    message: str
