import express from 'express';

export function createApp() {
  const app = express();

  app.get('/health', (_req, res) => {
    // TODO(Day42-task01): return HTTP 200 with JSON body { "status": "ok" }.
    res.status(501).json({ error: 'todo_health' });
  });

  return app;
}
