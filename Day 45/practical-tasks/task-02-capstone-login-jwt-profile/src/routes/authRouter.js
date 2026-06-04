import { Router } from 'express';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { getJwtSecret } from '../config/env.js';
import { User } from '../models/User.js';

export const authRouter = Router();

function requireAuth(req, res, next) {
  // TODO(Day45-task02): parse `Authorization: Bearer <token>`, verify with `jwt.verify` + `getJwtSecret()`, attach `req.auth = payload`, call `next()`. On failures respond 401 `{ error: 'unauthorized' }`.
  res.status(501).json({ error: 'todo_auth' });
}

authRouter.post('/login', async (req, res) => {
  // TODO(Day45-task02): read { email, password }. Find user by email including passwordHash (`User.findOne(...).select('+passwordHash')`). Compare with `bcrypt.compare`. On success return 200 `{ token }` where token is HS256 JWT `{ sub: user.id string, email: user.email }` expiring `12h` using `getJwtSecret()`. Wrong creds -> 401 `{ error: 'invalid_credentials' }`.
  res.status(501).json({ error: 'todo_login' });
});

authRouter.get('/me', requireAuth, async (req, res) => {
  // TODO(Day45-task02): load user by `req.auth.sub`, return 200 `{ id, email, name }` or 404 `{ error: 'not_found' }`.
  res.status(501).json({ error: 'todo_me' });
});
