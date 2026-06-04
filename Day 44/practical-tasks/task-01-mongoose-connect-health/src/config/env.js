import dotenv from 'dotenv';

dotenv.config();

/**
 * Reads Mongo connection settings from the environment (after dotenv).
 * Throws with a clear message when `MONGODB_URI` is missing so `npm start` fails fast.
 */
export function getMongoConfig() {
  const MONGODB_URI = process.env.MONGODB_URI;
  const MONGODB_DB_NAME = process.env.MONGODB_DB_NAME || 'course-node-45';
  if (!MONGODB_URI) {
    throw new Error('MONGODB_URI missing — copy .env.example to .env and paste your URI');
  }
  return { MONGODB_URI, MONGODB_DB_NAME };
}
