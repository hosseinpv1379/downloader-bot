import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_IDS
import database.core as db

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS and not db.is_admin(user_id):
        return

    users_count, downloads_count = db.get_stats()
    await update.message.reply_text(
        f"📊 آمار ربات:\n\n"
        f"👤 تعداد کاربران: {users_count}\n"
        f"📥 تعداد دانلودها: {downloads_count}"
    )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS and not db.is_admin(user_id):
        return

    if not context.args:
        await update.message.reply_text("لطفا متن پیام را بعد از دستور وارد کنید.\nمثال: /broadcast سلام به همه")
        return

    message = " ".join(context.args)
    users = db.get_all_users()
    sent_count = 0
    
    await update.message.reply_text(f"در حال ارسال پیام به {len(users)} کاربر...")
    
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=message)
            sent_count += 1
        except Exception as e:
            logging.error(f"Failed to send to {uid}: {e}")
            
    await update.message.reply_text(f"✅ پیام به {sent_count} کاربر ارسال شد.")
