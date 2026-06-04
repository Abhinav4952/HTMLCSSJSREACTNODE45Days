import mongoose from 'mongoose';
import { getMongoConfig } from '../config/env.js';

export async function connectMongo() {
  const { MONGODB_URI, MONGODB_DB_NAME } = getMongoConfig();
  if (mongoose.connection.readyState === 1) return;
  await mongoose.connect(MONGODB_URI, { dbName: MONGODB_DB_NAME });
}
