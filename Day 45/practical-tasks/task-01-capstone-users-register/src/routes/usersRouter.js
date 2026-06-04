import { Router } from 'express';
import { User } from '../models/User.js';

export const usersRouter = Router();

usersRouter.post('/register', async (req, res) => {
  // TODO(Day45-task01): read { email, password, name } from JSON. Validate non-empty strings (trim). Hash password with bcryptjs (`await bcrypt.hash(password, 10)`). Create `User` with `passwordHash` only (never store plaintext). Return 201 JSON { id, email, name } where `id` is the user `_id` string. On duplicate email (Mongo code 11000) return 409 { error: 'email_in_use' }. On validation failure return 400 { error: 'invalid_input' }.
  res.status(501).json({ error: 'todo_register' });
});
