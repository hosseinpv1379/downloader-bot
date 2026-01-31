import logging
from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import ContextTypes
import services.instagram as instagram_api
import database.core as db

async def handle_instagram_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    user_id = update.effective_user.id
    
    # Simple check if it looks like a URL
    if "instagram.com" not in message_text:
        await update.message.reply_text("لطفا یک لینک معتبر اینستاگرام ارسال کنید.")
        return

    shortcode = instagram_api.extract_shortcode(message_text)
    if not shortcode:
        await update.message.reply_text("لینک نامعتبر است. نتوانستم کد پست را پیدا کنم.")
        return

    msg = await update.message.reply_text("⏳ در حال پردازش و دانلود...")
    
    try:
        data = instagram_api.get_post_data(shortcode)
        
        if not data or 'media' not in data:
            await msg.edit_text("❌ خطا در دریافت اطلاعات. ممکن است پیج خصوصی باشد یا توکن نامعتبر باشد.")
            return

        media_list = data['media']
        caption = data.get('caption', '')
        # Truncate caption if too long
        if len(caption) > 1000:
            caption = caption[:1000] + "..."

        db.log_download(user_id, message_text)

        if len(media_list) == 1:
            item = media_list[0]
            if item['type'] == 'video':
                await update.message.reply_video(video=item['url'], caption=caption)
            else:
                await update.message.reply_photo(photo=item['url'], caption=caption)
        else:
            # Album
            media_group = []
            for i, item in enumerate(media_list):
                # Only add caption to the first item
                cap = caption if i == 0 else ""
                if item['type'] == 'video':
                    media_group.append(InputMediaVideo(media=item['url'], caption=cap))
                else:
                    media_group.append(InputMediaPhoto(media=item['url'], caption=cap))
            
            await update.message.reply_media_group(media=media_group)
        
        await msg.delete()

    except Exception as e:
        logging.error(f"Error handling link: {e}")
        await msg.edit_text("❌ متاسفانه خطایی رخ داد.")
