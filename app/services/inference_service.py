"""ML inference service wrapper for voice detection."""
import numpy as np
import logging
from typing import Tuple
from config.settings import settings

logger = logging.getLogger(__name__)

# Lazy import torch to handle DLL errors gracefully
try:
    import torch
    TORCH_AVAILABLE = True
except (ImportError, OSError) as e:
    logger.warning(f"PyTorch not available: {e}. Using placeholder mode.")
    TORCH_AVAILABLE = False
    torch = None


class InferenceService:
    """Service for performing AI voice detection inference."""
    
    def __init__(self):
        self.model_version = settings.MODEL_VERSION
        self.model = None
        if TORCH_AVAILABLE:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"Initialized inference service on device: {self.device}")
        else:
            self.device = None
            logger.warning("PyTorch not available - running in placeholder mode")
        self._load_model()
    
    def _load_model(self) -> None:
        """
        Load pretrained model.
        
        NOTE: This is a placeholder. Replace with actual model loading logic
        based on the chosen pretrained model.
        """
        logger.warning("Using placeholder model. Please implement actual model loading.")
        self.model = None
    
    def predict(self, audio: np.ndarray) -> Tuple[str, float]:
        """
        Perform inference on preprocessed audio.
        
        Args:
            audio: Preprocessed audio array (mono, normalized, resampled)
            
        Returns:
            Tuple of (prediction, confidence)
            - prediction: "AI_GENERATED" or "HUMAN"
            - confidence: float between 0 and 1
        """
        try:
            logger.info(f"Running inference on audio shape: {audio.shape}")
            
            if not TORCH_AVAILABLE or self.model is None:
                logger.warning("PyTorch not available or model not loaded, using placeholder prediction")
                return self._placeholder_predict(audio)
            
            with torch.no_grad():
                audio_tensor = self._prepare_input(audio)
                output = self.model(audio_tensor)
                prediction, confidence = self._process_output(output)
            
            logger.info(f"Prediction: {prediction}, Confidence: {confidence:.4f}")
            return prediction, confidence
            
        except Exception as e:
            logger.error(f"Inference failed: {str(e)}")
            raise ValueError(f"Inference failed: {str(e)}")
    
    def _prepare_input(self, audio: np.ndarray):
        """Prepare audio array for model input."""
        if not TORCH_AVAILABLE:
            return None
        audio_tensor = torch.from_numpy(audio).float().unsqueeze(0)
        if self.device and self.device.type == "cuda":
            audio_tensor = audio_tensor.cuda()
        return audio_tensor
    
    def _process_output(self, output) -> Tuple[str, float]:
        """Process model output to get prediction and confidence."""
        if not TORCH_AVAILABLE or output is None:
            return "HUMAN", 0.5
        
        if isinstance(output, (list, tuple)):
            output = output[0]
        
        if output.dim() > 1:
            output = output.squeeze()
        
        if output.shape[0] == 2:
            probs = torch.softmax(output, dim=0)
            ai_prob = probs[1].item()
            human_prob = probs[0].item()
        else:
            ai_prob = torch.sigmoid(output).item()
            human_prob = 1.0 - ai_prob
        
        prediction = "AI_GENERATED" if ai_prob > 0.5 else "HUMAN"
        confidence = max(ai_prob, human_prob)
        
        return prediction, confidence
    
    def _placeholder_predict(self, audio: np.ndarray) -> Tuple[str, float]:
        """
        Placeholder prediction function.
        Replace this with actual model inference once model is chosen.
        """
        duration = len(audio) / settings.SAMPLE_RATE
        
        if duration < 1.0:
            return "HUMAN", 0.6
        elif duration > 10.0:
            return "AI_GENERATED", 0.7
        else:
            return "HUMAN", 0.65

