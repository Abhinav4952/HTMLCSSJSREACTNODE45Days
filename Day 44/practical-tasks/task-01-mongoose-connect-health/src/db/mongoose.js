import mongoose from 'mongoose';
import { getMongoConfig } from '../config/env.js';

/**
 * Single place for Mongoose to connect (per cohort standard).
 * Uses `MONGODB_URI` and `MONGODB_DB_NAME` from the environment.
 */
export async function connectMongo() {
  // TODO(Day44-task01): read { MONGODB_URI, MONGODB_DB_NAME } via getMongoConfig() then await mongoose.connect(MONGODB_URI, { dbName: MONGODB_DB_NAME }) (official Mongoose pattern). Re-throw or wrap errors with context if connect fails.
  throw new Error('TODO(Day44-task01): implement connectMongo');
}

export function mongoState() {
  return mongoose.connection.readyState === 1 ? 'connected' : 'disconnected';
}
