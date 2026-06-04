import dotenv from 'dotenv';

dotenv.config();

export function loadEnv() {
  const JWT_SECRET = process.env.JWT_SECRET;
  if (!JWT_SECRET) {
    throw new Error('JWT_SECRET missing — copy .env.example to .env');
  }
  return { JWT_SECRET };
}
