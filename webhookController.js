const twilio = require('twilio');
const { classifyMessage } = require('../utils/classifier');

const activeMessages = new Map();

exports.handleIncomingMessage = async (req, res) => {
  const msg = req.body.Body?.trim().toLowerCase();
  const from = req.body.From;
  const now = new Date();

  const type = classifyMessage(msg);

  if (type === 'ingreso') {
    activeMessages.set(from, { msg, type, time: now });
    return res.send(`<Response><Message>✅ Ingreso registrado. ¡Bienvenido!</Message></Response>`);
  }

  if (type === 'salida') {
    activeMessages.delete(from);
    return res.send(`<Response><Message>👋 Salida registrada. ¡Hasta luego!</Message></Response>`);
  }

  return res.send(`<Response><Message>🤖 Mensaje recibido. Por favor indique "ingreso" o "salida".</Message></Response>`);
};

exports.getActiveMessages = (req, res) => {
  const data = Array.from(activeMessages.entries()).map(([from, info]) => ({
    from,
    ...info,
  }));
  res.json(data);
};
