from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "Emi-token-123"

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verificación del webhook
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return 'Verification failed', 403
    elif request.method == 'POST':
        # Procesar mensajes entrantes aquí (se puede ampliar)
        data = request.json
        print('Mensaje recibido:', data)
        return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)