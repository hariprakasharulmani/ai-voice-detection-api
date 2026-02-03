"""Example script for making API requests."""
import requests
import json

API_URL = "http://localhost:8000/detect-voice"
API_KEY = "your-secret-api-key-change-in-production"

def test_detection(audio_url: str, language: str = "en"):
    """Test voice detection endpoint."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "audio_url": audio_url,
        "language": language
    }
    
    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        print(json.dumps(result, indent=2))
        return result
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {e.response.text}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_audio_url = "https://example.com/sample.mp3"
    test_detection(test_audio_url, language="en")

