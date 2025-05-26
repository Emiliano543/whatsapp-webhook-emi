require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const webhookController = require('./controllers/webhookController');

const app = express();
const port = process.env.PORT || 3001;

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.post('/webhook', webhookController.handleIncomingMessage);

app.listen(port, () => {
  console.log(`🚀 Backend server running on port ${port}`);
});
