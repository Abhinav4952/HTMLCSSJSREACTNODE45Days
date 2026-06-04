import express from 'express';
import { mongoState } from './db/mongoose.js';

export function createApp() {
  const app = express();

  app.get('/health', (_req, res) => {
    res.json({ ok: true, mongo: mongoState() });
  });

  return app;
}
