import express from 'express';

export function createApp() {
  const app = express();
  const api = express.Router();

  // TODO(Day42-task02): register a middleware on `api` BEFORE `/ping` that sets response header `X-Lab-Tag` to `day-42-task-02` for every API request.
  api.get('/ping', (_req, res) => {
    res.json({ pong: true });
  });

  app.use('/api/v1', api);
  return app;
}
