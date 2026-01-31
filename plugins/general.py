from telegram import Update
from telegram.ext import ContextTypes
import database.core as db

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name)
    await update.message.reply_text(
        f"سلام {user.first_name}! 👋\n"
        "من ربات چندکاره هستم.\n"
        "قابلیت‌های من:\n"
        "📸 دانلود از اینستاگرام (پست، ریلز، IGTV)\n"
        "🎧 دانلود از اسپاتیفای (آهنگ)\n"
        "🗣 تبدیل متن به صدا (TTS)\n\n"
        "برای شروع کافیه لینک بفرستی یا از دستور /tts استفاده کنی!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "راهنما:\n\n"
        "1️⃣ **دانلودر:**\n"
        "لینک پست اینستاگرام یا آهنگ اسپاتیفای را ارسال کنید.\n"
        "مثال: https://www.instagram.com/p/CODE/\n\n"
        "2️⃣ **متن به صدا:**\n"
        "از دستور /tts به همراه متن استفاده کنید.\n"
        "مثال: /tts سلام چطوری؟"
    )
