from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "Emi-token-123"
ACCESS_TOKEN = "ACA_VA_TU_TOKEN_DE_META"

@app.route("/", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Error de verificación", 403

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if data.get("object") == "whatsapp_business_account":
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                for message in messages:
                    phone_number_id = value["metadata"]["phone_number_id"]
                    from_number = message["from"]
                    msg_text = message["text"]["body"].lower()

                    # Lógica del mensaje automático
                    if "ingreso" in msg_text:
                        send_message(from_number, phone_number_id,
                                     "Mensaje recibido ✅ después de 5 minutos sin no te contactamos el ingreso queda AUTORIZADO, no olvides informar el retiro, gracias.")
                    elif "salida" in msg_text:
                        send_message(from_number, phone_number_id,
                                     "Mensaje recibido ✅")
    return "OK", 200

def send_message(to, phone_number_id, text):
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    app.run(debug=True)
