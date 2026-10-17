from flask import Flask, request
from google import genai
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = "8746800192:AAFvVoTte-9hXipJavPnpI3nCAM2bsqaPiE"
GEMINI_API_KEY = "AQ.Ab8RN6IEWdKPYhka8YOXsDYfFX0r1So4J7bJtYeilT0jA8iEew"  # کلید جمنای خودت رو اینجا بذار

@app.route('/', methods=['GET'])
def home():
    return "Telegram Bot is running on Vercel!"

@app.route('/', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        if data and "message" in data:
            chat_id = data["message"]["chat"]["id"]
            user_text = data["message"].get("text", "")
            
            if user_text:
                try:
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=user_text,
                    )
                    reply_text = response.text
                except Exception as e:
                    reply_text = f"خطای جمنای: {str(e)}"
                
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": reply_text}
                )
    except Exception as e:
        print(f"Error: {e}")
        
    return "OK", 200
