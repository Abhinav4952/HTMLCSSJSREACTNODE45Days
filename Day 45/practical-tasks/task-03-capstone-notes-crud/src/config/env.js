import dotenv from 'dotenv';

dotenv.config();

export function getMongoConfig() {
  const MONGODB_URI = process.env.MONGODB_URI;
  const MONGODB_DB_NAME = process.env.MONGODB_DB_NAME || 'course-node-45';
  if (!MONGODB_URI) {
    throw new Error('MONGODB_URI missing — copy .env.example to .env and paste your URI');
  }
  return { MONGODB_URI, MONGODB_DB_NAME };
}

export function getJwtSecret() {
  const JWT_SECRET = process.env.JWT_SECRET;
  if (!JWT_SECRET) {
    throw new Error('JWT_SECRET missing — copy .env.example to .env');
  }
  return JWT_SECRET;
}
