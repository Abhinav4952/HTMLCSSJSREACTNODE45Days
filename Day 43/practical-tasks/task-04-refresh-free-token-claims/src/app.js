import express from 'express';
import { loadEnv } from './config/env.js';

const ISSUER = 'day43-task04-lab';
const AUDIENCE = 'course-api';

export function createApp() {
  loadEnv();
  const app = express();
  app.use(express.json());

  app.post('/auth/token', (_req, res) => {
    // TODO(Day43-task04): mint HS256 JWT exp 15m with claims { sub: 'demo', scope: 'read' }, issuer ISSUER, audience AUDIENCE (use jwt.sign options issuer/audience). Return { token }.
    res.status(501).json({ error: 'todo_token' });
  });

  app.get('/scoped/ping', (req, res) => {
    // TODO(Day43-task04): verify Bearer token with jwt.verify using { issuer: ISSUER, audience: AUDIENCE }. On success return 200 { ok:true, scope: payload.scope }. Missing/invalid -> 401 { error: 'unauthorized' }.
    res.status(501).json({ error: 'todo_scoped' });
  });

  return app;
}
