import os
from flask import Flask, request, jsonify
from google import genai
import requests

app = Flask(name)

# توکن ربات تلگرام و کلید جمنای
TELEGRAM_TOKEN = "8746800192:AAFvVoTte-9hXipJavPnpI3nCAM2bsqaPiE"
GEMINI_API_KEY = "AQ.Ab8RN6IEWdKPYhka8YOXsDYfFX0r1So4J7bJtYeilT0jA8iEew"  # کلید API جمنای خود را اینجا بگذارید

# راه‌اندازی کلاینت جمنای
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY != "YOUR_GEMINI_API_KEY" else None

@app.route('/', methods=['GET'])
def home():
    return "Telegram Bot is running smoothly on Vercel!"

@app.route('/', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        
        # بررسی اینکه آیا پیامی از تلگرام رسیده است
        if data and "message" in data:
            message = data["message"]
            chat_id = message["chat"]["id"]
            user_text = message.get("text", "")
            
            if user_text:
                # گرفتن پاسخ از جمنای
                try:
                    if client:
                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=user_text,
                        )
                        reply_text = response.text
                    else:
                        reply_text = "خطا: کلید API جمنای در کد تنظیم نشده است."
                except Exception as ai_err:
                    print(f"Gemini Error: {ai_err}")
                    reply_text = "متأسفانه در ارتباط با هوش مصنوعی خطایی رخ داد."
                
                # ارسال پاسخ به تلگرام
                telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                requests.post(telegram_url, json={
                    "chat_id": chat_id,
                    "text": reply_text
                })
                
    except Exception as e:
        print(f"Webhook Error: {e}")
        
    return jsonify({"status": "ok"}), 200
