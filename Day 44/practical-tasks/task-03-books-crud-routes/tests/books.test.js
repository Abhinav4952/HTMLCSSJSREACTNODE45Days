import request from 'supertest';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { MongoMemoryServer } from 'mongodb-memory-server';
import mongoose from 'mongoose';

let mongod;
let createApp;

beforeAll(async () => {
  mongod = await MongoMemoryServer.create();
  process.env.MONGODB_URI = mongod.getUri();
  process.env.MONGODB_DB_NAME = 'course-node-45';
  const mod = await import('../src/app.js');
  createApp = mod.createApp;
  const { connectMongo } = await import('../src/db/mongoose.js');
  await connectMongo();
});

afterAll(async () => {
  await mongoose.disconnect();
  if (mongod) await mongod.stop();
});

describe('books CRUD', () => {
  it('supports full CRUD flow', async () => {
    const app = createApp();

    const empty = await request(app).get('/books');
    expect(empty.status).toBe(200);
    expect(empty.body).toEqual([]);

    const bad = await request(app).post('/books').send({ title: '  ' });
    expect(bad.status).toBe(400);

    const created = await request(app).post('/books').send({ title: ' Atlas Notes ' });
    expect(created.status).toBe(201);
    expect(created.body.title).toBe('Atlas Notes');
    const id = created.body.id;

    const listed = await request(app).get('/books');
    expect(listed.status).toBe(200);
    expect(listed.body.map((b) => b.title)).toEqual(['Atlas Notes']);

    const one = await request(app).get(`/books/${id}`);
    expect(one.status).toBe(200);
    expect(one.body).toMatchObject({ id, title: 'Atlas Notes' });

    const updated = await request(app).patch(`/books/${id}`).send({ title: 'Mongo Notes' });
    expect(updated.status).toBe(200);
    expect(updated.body.title).toBe('Mongo Notes');

    const deleted = await request(app).delete(`/books/${id}`);
    expect(deleted.status).toBe(204);

    const missing = await request(app).get(`/books/${id}`);
    expect(missing.status).toBe(404);
  });
});
