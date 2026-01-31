import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
import database.core as db
from plugins import general, admin, instagram

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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
    
    # Admin Handlers
    application.add_handler(CommandHandler("stats", admin.stats))
    application.add_handler(CommandHandler("broadcast", admin.broadcast))
    
    # Instagram Handler
    instagram_filter = filters.TEXT & ~filters.COMMAND
    application.add_handler(MessageHandler(instagram_filter, instagram.handle_instagram_link))

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
