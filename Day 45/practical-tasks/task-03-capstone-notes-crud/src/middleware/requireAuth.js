import jwt from 'jsonwebtoken';
import { getJwtSecret } from '../config/env.js';

export function requireAuth(req, res, next) {
  const header = req.get('authorization') || '';
  const [scheme, token] = header.split(' ');
  if (scheme !== 'Bearer' || !token) {
    return res.status(401).json({ error: 'unauthorized' });
  }
  try {
    req.auth = jwt.verify(token, getJwtSecret());
    return next();
  } catch {
    return res.status(401).json({ error: 'unauthorized' });
  }
}
