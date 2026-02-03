"""Audio preprocessing pipeline for model input."""
import librosa
import soundfile as sf
import numpy as np
import logging
from pathlib import Path
from config.settings import settings
import os

logger = logging.getLogger(__name__)


class AudioPreprocessor:
    """Service for preprocessing audio files for model inference."""
    
    def __init__(self):
        self.target_sr = settings.SAMPLE_RATE
        self.max_duration = settings.MAX_AUDIO_DURATION_SECONDS
    
    def check_duration(self, audio_path: str, max_seconds: float = 30.0) -> None:
        """
        Quickly check audio duration using metadata (fast, no full load).
        
        Args:
            audio_path: Path to audio file
            max_seconds: Maximum allowed duration in seconds
            
        Raises:
            ValueError: If duration exceeds max_seconds or file cannot be read
        """
        try:
            info = sf.info(audio_path)
            duration = info.duration
            
            if duration > max_seconds:
                raise ValueError(f"Audio duration exceeds {max_seconds} seconds")
                
        except Exception as e:
            if "exceeds" in str(e):
                raise
            raise ValueError(f"Failed to read audio metadata: {str(e)}")
    
    def preprocess(self, audio_path: str) -> np.ndarray:
        """
        Preprocess audio file: load, convert format, normalize, resample.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Preprocessed audio array (mono, normalized, resampled)
            
        Raises:
            ValueError: If audio processing fails
        """
        try:
            logger.info(f"Preprocessing audio file: {audio_path}")
            
            if not os.path.exists(audio_path):
                raise ValueError(f"Audio file not found: {audio_path}")
            
            # Check if file is WAV format for optimized loading
            file_ext = Path(audio_path).suffix.lower()
            is_wav = file_ext == '.wav'
            
            if is_wav:
                # Fast path: Use soundfile for WAV files
                audio, sr = sf.read(audio_path, dtype='float32')
                
                # Apply 10-second limit
                max_samples = int(10 * sr)
                if len(audio) > max_samples:
                    audio = audio[:max_samples]
                
                # Convert to mono if stereo
                if audio.ndim > 1:
                    audio = np.mean(audio, axis=1)
                
                # Resample only if sample rate != 16000
                if sr != self.target_sr:
                    audio = librosa.resample(audio, orig_sr=sr, target_sr=self.target_sr, res_type="kaiser_fast")
                    sr = self.target_sr
            else:
                # Fallback: Use librosa for non-WAV formats (MP3, M4A, FLAC, etc.)
                audio, sr = librosa.load(
                    audio_path,
                    sr=self.target_sr,
                    mono=True,
                    duration=10,
                    res_type="kaiser_fast"
                )
            
            if len(audio) == 0:
                raise ValueError("Audio file is empty or corrupted")
            
            audio = self._normalize(audio)
            
            logger.info(f"Preprocessed audio: shape={audio.shape}, sr={sr}, duration={len(audio)/sr:.2f}s")
            return audio
            
        except Exception as e:
            logger.error(f"Audio preprocessing failed: {str(e)}")
            raise ValueError(f"Audio preprocessing failed: {str(e)}")
    
    def _normalize(self, audio: np.ndarray) -> np.ndarray:
        """Normalize audio to [-1, 1] range."""
        if np.max(np.abs(audio)) > 0:
            audio = audio / (np.max(np.abs(audio)) + 1e-8)
        return audio
    
    def cleanup(self, file_path: str) -> None:
        """Clean up temporary audio file."""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
                logger.debug(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup file {file_path}: {str(e)}")

