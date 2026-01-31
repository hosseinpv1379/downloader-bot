import requests
import re
from config import ONE_API_TOKEN

BASE_URL = "https://api.one-api.ir/spotify/v1"

def extract_track_id(url):
    """
    Extracts track ID from Spotify URL.
    Supports: open.spotify.com/track/ID
    """
    pattern = r'spotify\.com/track/([A-Za-z0-9]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_track_download_link(track_id):
    """
    Fetches download link for a Spotify track.
    Using default quality: OGG_320
    """
    headers = {
        "one-api-token": ONE_API_TOKEN,
        "Accept": "application/json"
    }
    
    # Using OGG_320 as default high quality
    url = f"{BASE_URL}/tracks/{track_id}/download/OGG_320"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == 200:
            return data.get("result")
        else:
            print(f"API Error: {data}")
            return None
            
    except Exception as e:
        print(f"Request Error: {e}")
        return None

def get_track_info(track_id):
    """
    Fetches track info (title, artist, cover) before downloading.
    Since there isn't a direct single track info endpoint in the snippet, 
    we might need to rely on the download endpoint or search.
    However, for now, we'll try to use the download endpoint result directly if it provides metadata.
    Checking the doc, /tracks/{id} is not explicitly shown in full detail but /artists/{id} is.
    Let's assume the download endpoint returns metadata or we just send the file.
    
    Wait, looking at the doc again, there is a "Search" tag and "Track" tag.
    The download endpoint returns "result": { "type": "object" }.
    Let's assume it returns a download link.
    """
    # NOTE: The provided doc snippet shows /tracks/{id}/download/{quality}
    # It doesn't show a simple /tracks/{id} metadata endpoint in the read snippet,
    # but standard REST APIs usually have it. 
    # For now, we will focus on getting the download link.
    return get_track_download_link(track_id)
