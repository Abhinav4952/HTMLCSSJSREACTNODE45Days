import express from 'express';
import { authRouter } from './routes/authRouter.js';
import { notesRouter } from './routes/notesRouter.js';
import { usersRouter } from './routes/usersRouter.js';

export function createApp() {
  const app = express();
  app.use(express.json());
  app.use('/users', usersRouter);
  app.use('/auth', authRouter);
  app.use('/notes', notesRouter);

  // TODO(Day45-task04): add Express error-handling middleware `(err, req, res, next)` registered **after** all routes. It should `console.error(err)` and respond with **500** JSON `{ error: 'server_error' }` using a **static** message (do not echo `err.message` to clients in this lab).
  return app;
}
