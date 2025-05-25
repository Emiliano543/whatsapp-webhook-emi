from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VERIFY_TOKEN = "Emi-token-123"
ACCESS_TOKEN = "TU_ACCESS_TOKEN"
PHONE_NUMBER_ID = "TU_PHONE_NUMBER_ID"

def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
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
    print("Respuesta WhatsApp:", response.status_code, response.text)

def mark_as_read(message_id):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id
    }
    response = requests.post(url, headers=headers, json=data)
    print("Mensaje marcado como leído:", response.status_code)

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verificación fallida", 403

    elif request.method == "POST":
        data = request.get_json()
        try:
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']
            messages = value.get('messages')

            if messages:
                message = messages[0]
                msg_text = message['text']['body'].lower().strip()
                msg_id = message['id']
                from_number = message['from']

                if any(palabra in msg_text for palabra in ["ingreso", "ingresó", "ingrese"]):
                    send_whatsapp_message(
                        from_number,
                        "Mensaje recibido ✅ después de 5 minutos sin no te contactamos el ingreso queda AUTORIZADO, no olvides informar el retiro, gracias."
                    )

                elif any(palabra in msg_text for palabra in ["salida", "salgo", "salí"]):
                    mark_as_read(msg_id)
                    send_whatsapp_message(
                        from_number,
                        "Mensaje recibido ✅"
                    )

        except Exception as e:
            print("Error procesando mensaje:", e)

        return "EVENT_RECEIVED", 200
