import { Router } from 'express';

const router = Router();

/**
 * Sample route used by the frontend Home page.
 * Keep this as a smoke-test of FE ↔ BE integration.
 * Candidates: add your real feature routes under /api/... later.
 */
router.get('/', (_req, res) => {
  res.status(200).json({
    message: 'Welcome to the Library Management API',
    project: 'Library Management',
    ok: true,
  });
});

export default router;
