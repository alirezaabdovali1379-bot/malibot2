from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = "8746800192:AAFvVoTte-9hXipJavPnpI3nCAM2bsqaPiE"
GEMINI_API_KEY = "AQ.Ab8RN6L-MseJmNRPCojeruDlt7qi5S6cHoqVM_EGO8LGmmyrng"  # کلید جمنای خودت رو اینجا بذار

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
                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={GEMINI_API_KEY}"
                payload = {"contents": [{"parts": [{"text": user_text}]}]}
                
                res = requests.post(gemini_url, json=payload)
                if res.status_code == 200:
                    reply_text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    reply_text = f"خطای جمنای: {res.text}"
                
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": reply_text}
                )
    except Exception as e:
        print(f"Error: {e}")
        
    return "OK", 200
