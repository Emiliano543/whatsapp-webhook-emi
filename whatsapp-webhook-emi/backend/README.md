# Consola CMD Montevideo (Backend)

## Requisitos
- Node.js 18+
- Twilio Account (sandbox activado)
- Frontend React ya configurado

## Instalación

```bash
cd backend
cp .env.example .env
# Editar .env con tus credenciales de Twilio
npm install
node server.js
```

## Endpoints

### POST /webhook
Twilio enviará aquí los mensajes entrantes.

### GET /activos (futuro)
Obtener mensajes activos desde el frontend.

---
Proyecto UTE - Automatización de ingresos/salidas por WhatsApp
