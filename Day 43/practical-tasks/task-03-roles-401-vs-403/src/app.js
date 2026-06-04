import express from 'express';
import { loadEnv } from './config/env.js';

const DEMO_USERS = {
  alice: { password: 'wonderland', role: 'student' },
  root: { password: 'sekret', role: 'admin' },
};

export function createApp() {
  loadEnv();
  const app = express();
  app.use(express.json());

  app.post('/auth/login', (req, res) => {
    // TODO(Day43-task03): validate username/password against DEMO_USERS. Return 200 { token } JWT HS256 exp 1h with claims { sub: username, role }. Invalid -> 401 { error: 'invalid_credentials' }.
    res.status(501).json({ error: 'todo_login' });
  });

  app.get('/admin/summary', (req, res) => {
    // TODO(Day43-task03): require Bearer JWT. If missing/invalid -> 401 { error: 'unauthorized' }. If valid but role !== 'admin' -> 403 { error: 'forbidden' }. Admins -> 200 { message: 'admin-ok' }.
    res.status(501).json({ error: 'todo_admin' });
  });

  return app;
}
