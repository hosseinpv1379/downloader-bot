import requests
import io
from config import ONE_API_TOKEN

BASE_URL = "https://api.one-api.ir/tts/v1/google/"

def text_to_speech(text, lang="fa"):
    """
    Converts text to speech using Google TTS via One-API.
    Returns io.BytesIO object containing audio data.
    """
    headers = {
        "one-api-token": ONE_API_TOKEN,
        "Content-Type": "application/json"
    }
    
    payload = {
        "lang": lang,
        "text": text
    }
    
    try:
        response = requests.post(BASE_URL, json=payload, headers=headers)
        response.raise_for_status()
        
        content_type = response.headers.get("Content-Type", "")
        
        # Check if response is actually audio
        if "audio" not in content_type and "mpeg" not in content_type:
            print(f"TTS API Error: Expected audio but got {content_type}")
            # Try to print body if it's text/json
            if "json" in content_type or "text" in content_type:
                print(f"Response body: {response.text}")
            return None
            
        if not response.content:
            print("TTS API Error: Empty response content")
            return None

        # Create file-like object
        audio_file = io.BytesIO(response.content)
        audio_file.name = "voice.mp3"  # Important for Telegram to recognize format
        return audio_file
        
    except Exception as e:
        print(f"TTS API Error: {e}")
        return None
