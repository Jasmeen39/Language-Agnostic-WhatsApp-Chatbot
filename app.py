from flask import Flask, request
import requests
from main import ask_user  
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Webhook verification (done once on Meta dashboard)"""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print(" Webhook verified successfully!")
        return challenge, 200
    else:
        return "Verification failed", 403


@app.route('/webhook', methods=['POST'])
def receive_message():
    """Receive WhatsApp messages"""
    data = request.get_json()
    print(" Received webhook data:", data)

    if data and "entry" in data:
        for entry in data["entry"]:
            if "changes" in entry:
                for change in entry["changes"]:
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    if messages:
                        for message in messages:
                            phone_number_id = value["metadata"]["phone_number_id"]
                            from_number = message["from"]
                            msg_text = message["text"]["body"]

                            print(f" Message from {from_number}: {msg_text}")

                            #  Get chatbot-generated response
                            try:
                                reply_text = ask_user(msg_text)
                            except Exception as e:
                                print(f" Chatbot error: {e}")
                                reply_text = "Sorry, something went wrong while processing your message."

                            send_whatsapp_message(phone_number_id, from_number, reply_text)

    return "EVENT_RECEIVED", 200


def send_whatsapp_message(phone_number_id, to, message):
    """Send reply back to WhatsApp user"""
    url = f"https://graph.facebook.com/v24.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }
    response = requests.post(url, headers=headers, json=data)
    print(" Sent message:", response.text)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
