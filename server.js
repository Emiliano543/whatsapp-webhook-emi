const express = require('express');
const app = express();
const PORT = process.env.PORT || 10000;
app.use(express.json());
app.post('/webhook', (req, res) => {
  console.log(req.body);
  res.sendStatus(200);
});
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));