from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "Emi-token-123"

@app.route("/", methods=["GET"])
def home():
    return "Webhook activo", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Error de verificación", 403

    if request.method == "POST":
        print("Mensaje recibido:", request.json)
        return "Evento recibido", 200
