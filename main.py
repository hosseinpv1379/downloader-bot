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
    chat_type = update.message.chat.type
    
    # Check for 'عرفان' in both private chats and groups
    # If bot receives this message, it means either:
    # - It's a private chat
    # - Bot is mentioned in group
    # - Privacy mode is disabled (bot can see all messages)
    if message_text and 'عرفان' in message_text:
        # Check if bot is mentioned (for groups) or it's a private chat
        is_group = chat_type in ['group', 'supergroup']
        bot_mentioned = False
        
        if is_group:
            # Check if bot is mentioned
            if context.bot.username and f"@{context.bot.username}" in message_text:
                bot_mentioned = True
            # Check if message is a reply to bot
            if update.message.reply_to_message:
                bot_mentioned = bot_mentioned or (update.message.reply_to_message.from_user.id == context.bot.id)
        
        # Respond if: private chat OR bot mentioned OR privacy disabled (bot can see message)
        if not is_group or bot_mentioned or message_text.strip() == 'عرفان':
            for i in range(30):
                await update.message.reply_text(f"کیر تو عرفان شماره :  {i+1}")
            return
    
    # Try Spotify
    if message_text and "spotify.com" in message_text:
        await spotify.handle_spotify_link(update, context)
        return

    # Try Instagram
    if message_text and "instagram.com" in message_text:
        await instagram.handle_instagram_link(update, context)
        return
        
    # Default response if no link matched (only in private chats)
    if chat_type == 'private':
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
