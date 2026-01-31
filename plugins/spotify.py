import logging
from telegram import Update
from telegram.ext import ContextTypes
import services.spotify as spotify_api
import database.core as db

async def handle_spotify_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    user_id = update.effective_user.id
    
    # Check if it's a Spotify link
    if "spotify.com" not in message_text:
        return False # Not handled by this plugin

    track_id = spotify_api.extract_track_id(message_text)
    if not track_id:
        await update.message.reply_text("لینک اسپاتیفای نامعتبر است. فقط لینک آهنگ (Track) پشتیبانی می‌شود.")
        return True # Handled (with error)

    msg = await update.message.reply_text("🎧 در حال دانلود موزیک از اسپاتیفای...")
    
    try:
        data = spotify_api.get_track_download_link(track_id)
        
        # The structure of 'data' depends on the API response.
        # Based on doc, it returns a result object.
        # Assuming result contains 'link' or similar.
        # Since I cannot see the exact response example for download in the snippet (it was truncated or generic),
        # I will assume standard One-API format: result -> download_link or url.
        # Let's try to inspect the data safely.
        
        if not data:
            await msg.edit_text("❌ خطا در دریافت فایل. ممکن است سرویس در دسترس نباشد.")
            return True

        # Common patterns for download APIs
        download_url = data.get('link') or data.get('url') or data.get('download_link')
        
        if not download_url:
            await msg.edit_text("❌ لینک دانلود یافت نشد.")
            return True

        db.log_download(user_id, message_text)
        
        # Send as audio
        await update.message.reply_audio(audio=download_url, caption="Downloaded via Bot 🎧")
        await msg.delete()
        return True

    except Exception as e:
        logging.error(f"Error handling spotify link: {e}")
        await msg.edit_text("❌ متاسفانه خطایی رخ داد.")
        return True
