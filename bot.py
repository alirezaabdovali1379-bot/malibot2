import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from google import genai

# تنظیمات توکن‌ها (بهتر است بعداً در رندر به صورت متغیر محیطی وارد کنید)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "TOKEN_BOTFATHER_YOU_GOT")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

# راه‌اندازی کلاینت جمنای
client = genai.Client(api_key=GEMINI_API_KEY)

# راه‌اندازی اپلیکیشن وب Flask (برای اینکه رندر سرویس را فعال نگه دارد)
app = Flask(name)

# ساخت ربات تلگرام
telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id
    
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )
        reply_text = response.text
    except Exception as e:
        reply_text = "متأسفانه در ارتباط با هوش مصنوعی خطایی رخ داد."
        print(f"Error: {e}")
        
    await update.message.reply_text(reply_text)

# افزودن هندلر پیام‌ها به ربات
telegram_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

@app.route('/')
def home():
    return "Telegram Bot is running via Webhook!"

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    """این مسیر پیام‌های ارسالی از تلگرام را دریافت می‌کند"""
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        # اجرای پردازش پیام به صورت ناهمگام در لوپ رویداد
        import asyncio
        asyncio.run(telegram_app.process_update(update))
    return "ok", 200

if name == 'main':
    # پورت پیش‌فرض رندر
    port = int(os.environ.get('PORT', 5000))
    
    # تنظیم خودکار وب‌هوک در تلگرام (آدرس رندر شما بعد از دیپلوی جایگزین می‌شود)
    # به طور مثال: https://your-app-name.onrender.com
    RENDER_EXTERNAL_URL = os.environ.get('RENDER_EXTERNAL_URL')
    if RENDER_EXTERNAL_URL:
        webhook_url = f"{RENDER_EXTERNAL_URL}/{TELEGRAM_TOKEN}"
        import requests
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={webhook_url}")
        print(f"Webhook set to: {webhook_url}")

    # اجرای اپلیکیشن وب
    app.run(host='0.0.0.0', port=port)