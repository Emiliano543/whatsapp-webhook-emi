from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "Emi-token-123"

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        mode = request.args.get("hub.mode")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verificación fallida", 403
    elif request.method == "POST":
        return "OK", 200
