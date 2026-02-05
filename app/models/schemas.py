from pydantic import BaseModel
from typing import Literal

class Base64AudioRequest(BaseModel):
    language: Literal["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
    audioFormat: Literal["mp3"]
    audioBase64: str


class VoiceDetectionResponse(BaseModel):
    status: str
    language: str
    classification: Literal["AI_GENERATED", "HUMAN"]
    confidenceScore: float
    explanation: str
