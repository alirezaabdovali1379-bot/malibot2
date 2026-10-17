import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from google import genai

# تنظیمات کلیدها (بهتر است متغیرهای محیطی باشند یا به صورت مستقیم وارد کنید)
TELEGRAM_TOKEN = "8746800192:AAFvVoTte-9hXipJavPnpI3nCAM2bsqaPiE"
GEMINI_API_KEY = "AQ.Ab8RN6IEWdKPYhka8YOXsDYfFX0r1So4J7bJtYeilT0jA8iEew"

# راه‌اندازی کلاینت جمنای
client = genai.Client(api_key=GEMINI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id
    
    # ارسال پیام وضعیت «در حال تایپ...» به کاربر
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    try:
        # ارسال پیام به مدل جمنای (استفاده از مدل استاندارد gemini-3.8-flash-lite یا نسخه دلخواه)
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=user_message,
        )
        reply_text = response.text
    except Exception as e:
        reply_text = "متأسفانه در ارتباط با هوش مصنوعی خطایی رخ داد."
        print(f"Error: {e}")
        
    # ارسال پاسخ جمنای به کاربر در تلگرام
    await update.message.reply_text(reply_text)

def main():
    # ساخت اپلیکیشن ربات تلگرام
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # افزودن هندلر برای دریافت تمام پیام‌های متنی
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("ربات در حال اجراست...")
    # شروع به کار ربات (Polling)
    app.run_polling()

if __name__ == '__main__':
    main()
