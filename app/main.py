"""Main FastAPI application."""
import time
import logging
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.settings import settings
from app.models.schemas import (
    VoiceDetectionRequest,
    VoiceDetectionResponse,
    ErrorResponse
)
from app.middleware.auth import verify_api_key
from app.services.audio_downloader import AudioDownloader
from app.services.audio_preprocessor import AudioPreprocessor
from app.services.inference_service import InferenceService

logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

inference_service = None
audio_downloader = None
audio_preprocessor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    global inference_service, audio_downloader, audio_preprocessor
    
    logger.info("Starting up application...")
    inference_service = InferenceService()
    audio_downloader = AudioDownloader()
    audio_preprocessor = AudioPreprocessor()
    logger.info("Application startup complete")
    
    yield
    
    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.API_VERSION}


@app.post(
    "/detect-voice",
    response_model=VoiceDetectionResponse,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    tags=["Voice Detection"]
)
async def detect_voice(
    request: VoiceDetectionRequest,
    authenticated: bool = Depends(verify_api_key)
) -> VoiceDetectionResponse:
    """
    Detect if audio contains AI-generated voice.
    
    Args:
        request: Voice detection request with audio URL
        authenticated: Authentication dependency
        
    Returns:
        VoiceDetectionResponse with prediction and metadata
    """
    temp_file_path = None
    
    try:
        logger.info(f"Received detection request for URL: {request.audio_url}")
        
        temp_file_path = await audio_downloader.download(str(request.audio_url))
        
        audio_preprocessor.check_duration(temp_file_path, max_seconds=30.0)
        
        processing_start_time = time.time()
        audio = audio_preprocessor.preprocess(temp_file_path)
        
        prediction, confidence = inference_service.predict(audio)
        processing_time_ms = int((time.time() - processing_start_time) * 1000)
        
        language = request.language or "unknown"
        
        response = VoiceDetectionResponse(
            prediction=prediction,
            confidence=confidence,
            language=language,
            model_version=inference_service.model_version,
            processing_time_ms=processing_time_ms
        )
        
        logger.info(
            f"Detection complete: {prediction} (confidence={confidence:.4f}, "
            f"time={processing_time_ms}ms)"
        )
        
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        error_msg = str(e)
        if "duration exceeds" in error_msg.lower():
            raise HTTPException(status_code=400, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        logger.error(f"Internal server error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if temp_file_path:
            audio_preprocessor.cleanup(temp_file_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

