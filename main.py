import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN
import database.core as db
from plugins import general, admin, instagram, spotify, tts

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Central message handler to route messages to appropriate plugins.
    """
    message_text = update.message.text
    
    # Try Spotify
    if "spotify.com" in message_text:
        await spotify.handle_spotify_link(update, context)
        return

    # Try Instagram
    if "instagram.com" in message_text:
        await instagram.handle_instagram_link(update, context)
        return
        
    # Default response if no link matched
    await update.message.reply_text("لینک ارسال شده پشتیبانی نمی‌شود. لطفا لینک اینستاگرام یا اسپاتیفای ارسال کنید.\nبرای تبدیل متن به صدا از دستور /tts استفاده کنید.")

def main():
    # Initialize DB
    db.init_db()
    
    if not BOT_TOKEN:
        print("Error: Please set your BOT_TOKEN in .env")
        exit(1)

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # General Handlers
    application.add_handler(CommandHandler("start", general.start))
    application.add_handler(CommandHandler("help", general.help_command))
    
    # TTS Handler
    application.add_handler(CommandHandler("tts", tts.tts_command))
    
    # Admin Handlers
    application.add_handler(CommandHandler("stats", admin.stats))
    application.add_handler(CommandHandler("broadcast", admin.broadcast))
    
    # Universal Message Handler for Links
    # We use a single handler to route based on content, avoiding conflicts
    link_filter = filters.TEXT & ~filters.COMMAND
    application.add_handler(MessageHandler(link_filter, handle_message))

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
