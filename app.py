
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VERIFY_TOKEN = 'emi-verificacion'
WHATSAPP_TOKEN = 'AQUÍ_VA_TU_TOKEN_DE_META'

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Forbidden", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if data.get("object") == "whatsapp_business_account":
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                if messages:
                    for message in messages:
                        phone_number_id = value["metadata"]["phone_number_id"]
                        from_number = message["from"]
                        text = message["text"]["body"]
                        response = ""

                        if text.lower() == "ingreso":
                            response = ("Mensaje recibido ✅ después de 5 minutos sin no te contactamos "
                                        "el ingreso queda AUTORIZADO, no olvides informar el retiro, gracias.")
                        elif text.lower() == "salida":
                            response = "Mensaje recibido ✅"

                        if response:
                            send_message(phone_number_id, from_number, response)

    return "EVENT_RECEIVED", 200

def send_message(phone_number_id, to_number, message_text):
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "text": {"body": message_text}
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
