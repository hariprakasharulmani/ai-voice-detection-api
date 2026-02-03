"""Audio downloader service with validation and timeout."""
import httpx
import logging
from typing import Optional
from pathlib import Path
from config.settings import settings
import tempfile
import os

logger = logging.getLogger(__name__)


class AudioDownloader:
    """Service for downloading and validating audio files from URLs."""
    
    def __init__(self):
        self.timeout = 10.0  # 10-second timeout as required
        self.max_duration = settings.MAX_AUDIO_DURATION_SECONDS
        self.supported_formats = settings.SUPPORTED_AUDIO_FORMATS
        self.max_file_size = 10 * 1024 * 1024  # 10 MB limit
    
    async def download(self, url: str) -> str:
        """
        Download audio file from URL with validation (async).
        
        Args:
            url: URL of the audio file
            
        Returns:
            Path to downloaded temporary file
            
        Raises:
            ValueError: If download fails or file is invalid
        """
        try:
            logger.info(f"Downloading audio from URL: {url}")
            
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; VoiceDetectionAPI/1.0)"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                async with client.stream("GET", url, headers=headers) as response:
                    # Validate HTTP status code
                    if response.status_code < 200 or response.status_code >= 300:
                        raise ValueError(f"HTTP {response.status_code}: Invalid status code")
                    
                    response.raise_for_status()
                    
                    content_type = response.headers.get("Content-Type", "").lower()
                    content_length = response.headers.get("Content-Length")
                    
                    # Check file size from Content-Length header
                    if content_length:
                        size_bytes = int(content_length)
                        if size_bytes > self.max_file_size:
                            size_mb = size_bytes / (1024 * 1024)
                            raise ValueError(f"File too large: {size_mb:.2f}MB (max 10MB)")
                    
                    # Create temp directory if needed
                    try:
                        os.makedirs(settings.TEMP_DIR, exist_ok=True)
                    except Exception:
                        pass
                    
                    temp_file = tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".tmp",
                        dir=settings.TEMP_DIR if os.path.exists(settings.TEMP_DIR) else None
                    )
                    
                    downloaded_bytes = 0
                    
                    # Stream download with size validation
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        if chunk:
                            temp_file.write(chunk)
                            downloaded_bytes += len(chunk)
                            if downloaded_bytes > self.max_file_size:
                                temp_file.close()
                                os.unlink(temp_file.name)
                                raise ValueError("File size exceeds 10MB limit")
                    
                    temp_file.close()
                    
                    file_extension = self._get_file_extension(url, content_type)
                    if file_extension not in self.supported_formats:
                        logger.warning(f"Unsupported format detected: {file_extension}, will attempt conversion")
                    
                    logger.info(f"Successfully downloaded audio file: {temp_file.name} ({downloaded_bytes / (1024*1024):.2f}MB)")
                    return temp_file.name
                    
        except httpx.TimeoutException:
            logger.error(f"Timeout downloading audio from {url}")
            raise ValueError(f"Download timeout after {self.timeout} seconds")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error downloading audio: {e.response.status_code}")
            raise ValueError(f"HTTP {e.response.status_code}: Failed to download audio")
        except httpx.RequestError as e:
            logger.error(f"Request error downloading audio: {str(e)}")
            raise ValueError(f"Failed to download audio: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during download: {str(e)}")
            raise ValueError(f"Download failed: {str(e)}")
    
    def _get_file_extension(self, url: str, content_type: str) -> str:
        """Extract file extension from URL or content type."""
        url_lower = url.lower()
        
        for ext in self.supported_formats:
            if ext in url_lower:
                return ext
        
        if "audio/mpeg" in content_type or "audio/mp3" in content_type:
            return ".mp3"
        elif "audio/wav" in content_type or "audio/wave" in content_type:
            return ".wav"
        elif "audio/x-m4a" in content_type or "audio/m4a" in content_type:
            return ".m4a"
        elif "audio/flac" in content_type:
            return ".flac"
        
        return ".mp3"

