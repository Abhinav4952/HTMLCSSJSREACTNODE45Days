import 'dotenv/config';
import { createApp } from './app.js';
import connectDB from './config/db.js';

const PORT = Number(process.env.PORT) || 5000;

async function start() {
  // Requires a valid MONGO_URI in .env (copy from .env.example and replace the placeholder).
  await connectDB();
  const app = createApp();
  app.listen(PORT, () => {
    console.log(`Server listening on http://localhost:${PORT}`);
  });
}

start();
