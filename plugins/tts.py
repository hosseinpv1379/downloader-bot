from telegram import Update
from telegram.ext import ContextTypes
import services.tts as tts_service
import logging

async def tts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("لطفا متن مورد نظر را بعد از دستور وارد کنید.\nمثال: /tts سلام چطوری")
        return

    text = " ".join(context.args)
    
    # Simple heuristic: If text contains mostly ASCII, assume English, else Persian
    # This covers English inputs, while defaults to Persian for mixed/other inputs which is safe for this context.
    lang = "fa"
    if text.isascii():
        lang = "en"
        
    msg = await update.message.reply_text("🗣 در حال تبدیل متن به صدا...")
    
    try:
        audio_data = tts_service.text_to_speech(text, lang)
        
        if audio_data:
            await update.message.reply_voice(voice=audio_data, caption=f"🗣 {text[:50]}...")
            await msg.delete()
        else:
            await msg.edit_text("❌ خطا در دریافت صدا. سرویس پاسخگو نیست.")
            
    except Exception as e:
        logging.error(f"TTS Error: {e}")
        await msg.edit_text("❌ خطایی رخ داد.")
