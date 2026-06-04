import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { MongoMemoryServer } from 'mongodb-memory-server';
import mongoose from 'mongoose';

let mongod;

beforeAll(async () => {
  mongod = await MongoMemoryServer.create();
  process.env.MONGODB_URI = mongod.getUri();
  process.env.MONGODB_DB_NAME = 'course-node-45';
  const { connectMongo } = await import('../src/db/mongoose.js');
  await connectMongo();
});

afterAll(async () => {
  await mongoose.disconnect();
  if (mongod) await mongod.stop();
});

describe('Book validation + timestamps', () => {
  it('rejects short titles', async () => {
    const { Book } = await import('../src/models/Book.js');
    await expect(Book.create({ title: 'ab' })).rejects.toThrow();
  });

  it('stores timestamps', async () => {
    const { Book } = await import('../src/models/Book.js');
    const created = await Book.create({ title: 'Valid' });
    expect(created.createdAt).toBeInstanceOf(Date);
    expect(created.updatedAt).toBeInstanceOf(Date);
  });
});
