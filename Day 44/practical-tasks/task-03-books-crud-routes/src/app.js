import express from 'express';
import { booksRouter } from './routes/booksRouter.js';

export function createApp() {
  const app = express();
  app.use(express.json());
  app.use('/books', booksRouter);
  return app;
}
