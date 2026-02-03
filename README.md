# AI Voice Detection API

Production-grade REST API for detecting AI-generated voices in audio files. Built for national-level hackathon automated evaluation.

## Features

- 🔐 API key authentication via Bearer token
- 🌐 Accepts audio input as URL (MP3/WAV/M4A/FLAC)
- ⚡ Low latency inference (<1s target)
- 🛡️ Robust error handling and validation
- 📊 Structured JSON responses
- 🎯 Production-ready with logging and monitoring

## Tech Stack

- Python 3.10+
- FastAPI
- PyTorch
- librosa & soundfile
- Pydantic

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd cur
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
Create a `.env` file in the root directory:
```env
API_KEY=your-secret-api-key-here
DEBUG=False
HOST=0.0.0.0
PORT=8000
MODEL_PATH=/path/to/model  # Optional, if model is stored locally
```

## Running the API

### Development Mode
```bash
python main.py
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /detect-voice

Detect if audio contains AI-generated voice.

**Authentication:** Required (Bearer token in Authorization header)

**Request Body:**
```json
{
  "audio_url": "https://example.com/audio.mp3",
  "language": "en"
}
```

**Success Response (200):**
```json
{
  "prediction": "AI_GENERATED",
  "confidence": 0.87,
  "language": "en",
  "model_version": "1.0.0",
  "processing_time_ms": 450
}
```

**Error Response (400/401/500):**
```json
{
  "error": "Error message description"
}
```

## Example Usage

### cURL Request
```bash
curl -X POST "http://localhost:8000/detect-voice" \
  -H "Authorization: Bearer your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/sample.mp3",
    "language": "en"
  }'
```

### Python Request
```python
import requests

url = "http://localhost:8000/detect-voice"
headers = {
    "Authorization": "Bearer your-secret-api-key-here",
    "Content-Type": "application/json"
}
data = {
    "audio_url": "https://example.com/sample.mp3",
    "language": "en"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

## Project Structure

```
cur/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic models
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py             # API key authentication
│   └── services/
│       ├── __init__.py
│       ├── audio_downloader.py  # Audio download service
│       ├── audio_preprocessor.py # Audio preprocessing
│       └── inference_service.py  # ML inference wrapper
├── config/
│   ├── __init__.py
│   └── settings.py             # Configuration
├── tests/
│   └── __init__.py
├── main.py                      # Entry point
├── requirements.txt
├── .env                         # Environment variables (create this)
└── README.md
```

## Model Integration

**IMPORTANT:** The current implementation includes a placeholder inference service. You need to:

1. Choose a pretrained model for AI voice detection
2. Update `app/services/inference_service.py` to load and use the actual model
3. Ensure the model input/output format matches the preprocessing pipeline

Popular options for AI voice detection:
- Wav2Vec2-based models
- ASVspoof models
- Custom fine-tuned models

## Configuration

Key settings in `config/settings.py`:
- `API_KEY`: Secret API key for authentication
- `AUDIO_DOWNLOAD_TIMEOUT`: Download timeout in seconds (default: 30)
- `MAX_AUDIO_DURATION_SECONDS`: Maximum audio length (default: 60)
- `SAMPLE_RATE`: Target sample rate for preprocessing (default: 16000)
- `MODEL_VERSION`: Model version string

## Error Handling

The API handles:
- Invalid API keys (401)
- Malformed requests (400)
- Download failures (400)
- Audio processing errors (400)
- Model inference errors (500)
- Network timeouts (400)

## Deployment

### Docker (Recommended)

Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t voice-detection-api .
docker run -p 8000:8000 -e API_KEY=your-key voice-detection-api
```

### Production Considerations

1. Use environment variables for sensitive data
2. Set up proper logging and monitoring
3. Use reverse proxy (nginx) for SSL termination
4. Configure rate limiting
5. Set up health check monitoring
6. Use process manager (systemd, supervisor, or PM2)

## License

[Specify your license]

## Support

For issues or questions, please contact [your contact information]

