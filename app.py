from flask import Flask, request
import json

app = Flask(__name__)

VERIFY_TOKEN = "Emi-token-123"

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification token mismatch", 403
    if request.method == "POST":
        data = request.get_json()
        print("Mensaje recibido:", json.dumps(data, indent=2))
        return "EVENT_RECEIVED", 200

    return "Unsupported Method", 405

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)