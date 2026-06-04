import express from 'express';
import { loadEnv } from './config/env.js';

const DEMO_USERS = {
  alice: 'wonderland',
};

export function createApp() {
  loadEnv();
  const app = express();
  app.use(express.json());

  app.post('/auth/login', (req, res) => {
    // TODO(Day43-task02): read { username, password } from JSON body. If credentials match DEMO_USERS, return 200 JSON { token } where token is HS256 JWT with payload { sub: username } expiring in 1h. Otherwise 401 JSON { error: 'invalid_credentials' }.
    res.status(501).json({ error: 'todo_login' });
  });

  app.get('/me', (req, res) => {
    // TODO(Day43-task02): parse Authorization: Bearer <token>, verify with JWT_SECRET, return 200 { user: payload.sub }. On missing/invalid token return 401 { error: 'unauthorized' }.
    res.status(501).json({ error: 'todo_me' });
  });

  return app;
}
