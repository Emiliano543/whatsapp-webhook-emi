from flask import Flask, request
import os

app = Flask(__name__)

VERIFY_TOKEN = "Emi-token-123"

@app.route('/')
def index():
    return 'Webhook activo', 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Unauthorized", 403

    elif request.method == 'POST':
        data = request.get_json()
        print("Mensaje recibido:", data)
        return "EVENT_RECEIVED", 200

if __name__ == '__main__':
    # Render asigna el puerto en la variable de entorno PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
