import express from 'express';

export function createApp() {
  const app = express();
  const v1 = express.Router();

  v1.post('/widgets', (req, res) => {
    if (!req.body || typeof req.body.sku !== 'string' || req.body.sku.trim() === '') {
      return res.status(400).json({ error: 'sku_required' });
    }
    return res.status(201).json({ sku: req.body.sku.trim() });
  });

  // Intentionally wrong: JSON parser runs AFTER the router, so `req.body` stays undefined.
  app.use('/v1', v1);

  // TODO(Day42-task04): move `express.json()` (and any related middleware) so JSON bodies are parsed BEFORE requests hit `/v1` routes. Keep routes otherwise identical.
  app.use(express.json());

  app.use((err, _req, res, _next) => {
    console.error(err);
    res.status(500).json({ error: 'internal_error' });
  });

  return app;
}
