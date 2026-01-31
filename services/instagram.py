import requests
import re
from config import ONE_API_TOKEN

BASE_URL = "https://api.one-api.ir/instagram/v1/post/"

def extract_shortcode(url):
    """
    Extracts shortcode from Instagram URL.
    Supports: /p/, /reel/, /tv/
    """
    pattern = r'(?:instagram\.com|instagr\.am)/(?:p|reel|tv)/([A-Za-z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_post_data(shortcode):
    """
    Fetches post data from One-API using the shortcode.
    """
    headers = {
        "one-api-token": ONE_API_TOKEN,
        "Accept": "application/json"
    }
    params = {
        "shortcode": shortcode
    }
    
    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
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
