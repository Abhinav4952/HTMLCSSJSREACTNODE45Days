import bcrypt from 'bcryptjs';
import { Router } from 'express';
import { User } from '../models/User.js';

export const usersRouter = Router();

usersRouter.post('/register', async (req, res) => {
  const { email, password, name } = req.body ?? {};
  if (!email || !password || !name) {
    return res.status(400).json({ error: 'invalid_input' });
  }
  if ([email, password, name].some((v) => typeof v !== 'string' || v.trim() === '')) {
    return res.status(400).json({ error: 'invalid_input' });
  }
  try {
    const passwordHash = await bcrypt.hash(password, 10);
    const user = await User.create({ email: email.trim(), name: name.trim(), passwordHash });
    return res.status(201).json({ id: user._id.toString(), email: user.email, name: user.name });
  } catch (err) {
    if (err && err.code === 11000) {
      return res.status(409).json({ error: 'email_in_use' });
    }
    console.error(err);
    return res.status(500).json({ error: 'server_error' });
  }
});
