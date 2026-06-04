import express from 'express';
import { authRouter } from './routes/authRouter.js';
import { usersRouter } from './routes/usersRouter.js';

export function createApp() {
  const app = express();
  app.use(express.json());
  app.use('/users', usersRouter);
  app.use('/auth', authRouter);
  return app;
}
