import express from 'express';
import cors from 'cors';
import morgan from 'morgan';
import welcomeRoutes from './routes/welcome.routes.js';
import { notFound } from './middleware/notFound.js';
import { errorHandler } from './middleware/errorHandler.js';

/**
 * Build the Express app (exported so Vitest can import it without listening).
 * Candidates: mount new routers under /api/... here.
 */
export function createApp() {
  const app = express();

  app.use(
    cors({
      origin: process.env.CLIENT_ORIGIN || 'http://localhost:5173',
    }),
  );
  app.use(express.json());
  app.use(morgan('dev'));

  app.get('/api/health', (_req, res) => {
    res.status(200).json({ status: 'ok' });
  });

  app.use('/api/welcome', welcomeRoutes);

  // Candidate routes go here, for example:
  // app.use('/api/auth', authRoutes);
  // app.use('/api/products', productRoutes);

  app.use(notFound);
  app.use(errorHandler);

  return app;
}
