import { Router } from 'express';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { getJwtSecret } from '../config/env.js';
import { User } from '../models/User.js';
import { requireAuth } from '../middleware/requireAuth.js';

export const authRouter = Router();

authRouter.post('/login', async (req, res) => {
  const { email, password } = req.body ?? {};
  if (!email || !password || typeof email !== 'string' || typeof password !== 'string') {
    return res.status(400).json({ error: 'invalid_input' });
  }
  const user = await User.findOne({ email: email.trim().toLowerCase() }).select('+passwordHash');
  if (!user) {
    return res.status(401).json({ error: 'invalid_credentials' });
  }
  const ok = await bcrypt.compare(password, user.passwordHash);
  if (!ok) {
    return res.status(401).json({ error: 'invalid_credentials' });
  }
  const token = jwt.sign({ sub: user._id.toString(), email: user.email }, getJwtSecret(), { expiresIn: '12h' });
  return res.json({ token });
});

authRouter.get('/me', requireAuth, async (req, res) => {
  const user = await User.findById(req.auth.sub);
  if (!user) {
    return res.status(404).json({ error: 'not_found' });
  }
  return res.json({ id: user._id.toString(), email: user.email, name: user.name });
});
