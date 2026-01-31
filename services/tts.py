import requests
from config import ONE_API_TOKEN

BASE_URL = "https://api.one-api.ir/tts/v1/google/"

def text_to_speech(text, lang="fa"):
    """
    Converts text to speech using Google TTS via One-API.
    Returns binary audio data.
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
        return response.content # Returns binary content (audio/mpeg)
    except Exception as e:
        print(f"TTS API Error: {e}")
        return None
