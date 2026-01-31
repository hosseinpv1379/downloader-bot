from telegram import Update
from telegram.ext import ContextTypes
import database.core as db

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name)
    await update.message.reply_text(
        f"سلام {user.first_name}! 👋\n"
        "من ربات دانلودر اینستاگرام هستم.\n"
        "لینک پست، ریلز یا IGTV اینستاگرام رو برام بفرست تا فایلشو برات دانلود کنم."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "راهنما:\n"
        "کافیه لینک پست اینستاگرام رو کپی کنی و اینجا بفرستی.\n"
        "مثال: https://www.instagram.com/p/CODE/"
    )
