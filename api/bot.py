from flask import Flask, request, jsonify
import requests

app = Flask(name)

# توکن تلگرام شما
TELEGRAM_TOKEN = "8746800192:AAFvVoTte-9hXipJavPnpI3nCAM2bsqaPiE"

# کلید جمنای خود را دقیقاً بین دو علامت کوتیشن زیر قرار دهید
GEMINI_API_KEY = "AQ.Ab8RN6IEWdKPYhka8YOXsDYfFX0r1So4J7bJtYeilT0jA8iEew"

@app.route('/', methods=['GET'])
def home():
    return "Bot is alive and running 100%!"

@app.route('/', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        if data and "message" in data:
            chat_id = data["message"]["chat"]["id"]
            user_text = data["message"].get("text", "")

            if user_text:
                try:
                    from google import genai
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=user_text,
                    )
                    reply_text = response.text
                except Exception as e:
                    reply_text = f"خطای هوش مصنوعی: {str(e)}"

                # ارسال پیام به تلگرام
                url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                requests.post(url, json={"chat_id": chat_id, "text": reply_text})
    except Exception as e:
        print(f"Webhook Error: {e}")

    return jsonify({"status": "ok"}), 200
