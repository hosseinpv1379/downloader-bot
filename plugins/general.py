from telegram import Update
from telegram.ext import ContextTypes
import database.core as db

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name)
    await update.message.reply_text(
        f"سلام {user.first_name}! 👋\n"
        "من ربات دانلودر هستم.\n"
        "لینک‌های زیر را پشتیبانی می‌کنم:\n"
        "📸 اینستاگرام (پست، ریلز، IGTV)\n"
        "🎧 اسپاتیفای (آهنگ)\n\n"
        "کافیه لینک رو برام بفرستی!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "راهنما:\n"
        "برای دانلود، لینک مورد نظر را کپی کرده و ارسال کنید.\n\n"
        "مثال اینستاگرام:\n"
        "https://www.instagram.com/p/CODE/\n\n"
        "مثال اسپاتیفای:\n"
        "https://open.spotify.com/track/ID"
    )
