import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env file")

# One-API Token for Instagram
ONE_API_TOKEN = os.getenv("ONE_API_TOKEN")
if not ONE_API_TOKEN:
    raise ValueError("ONE_API_TOKEN is not set in .env file")

# Admin IDs (List of integers)
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]
