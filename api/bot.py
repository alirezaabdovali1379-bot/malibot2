import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from google import genai
import asyncio

app = Flask(name)

# توکن ربات تلگرام و کلید جمنای
TELEGRAM_TOKEN = "8746800192:AAFvVoTte-9hXipJavPnpI3nCAM2bsqaPiE"
GEMINI_API_KEY = "AQ.Ab8RN6IEWdKPYhka8YOXsDYfFX0r1So4J7bJtYeilT0jA8iEew"  # کلید جمنای خود را اینجا وارد کنید

client = genai.Client(api_key=GEMINI_API_KEY)

telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    user_message = update.message.text
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )
        reply_text = response.text
    except Exception as e:
        reply_text = f"خطا در ارتباط با هوش مصنوعی: {str(e)}"
        
    await update.message.reply_text(reply_text)

telegram_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

_initialized = False

async def initialize_app():
    global _initialized
    if not _initialized:
        await telegram_app.initialize()
        _initialized = True

@app.route('/', methods=['GET'])
def home():
    return "Telegram Bot is running smoothly!"

@app.route('/', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        if data:
            update = Update.de_json(data, telegram_app.bot)
            
            async def process():
                await initialize_app()
                await telegram_app.process_update(update)
            
            asyncio.run(process())
    except Exception as e:
        print(f"Error: {e}")
        
    return "OK", 200