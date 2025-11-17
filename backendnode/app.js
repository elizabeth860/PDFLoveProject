const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Ruta principal que responde con texto simple
app.get('/', (req, res) => {
  res.send('Hola desde Node.js en cPanel!');
});

// Inicia el servidor en el puerto definido
app.listen(PORT, () => {
  console.log(`Servidor corriendo en puerto ${PORT}`);
});
