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
  process.env.JWT_SECRET = 'jwt-test-secret';
  const { connectMongo } = await import('../src/db/mongoose.js');
  await connectMongo();
  ({ createApp } = await import('../src/app.js'));
});

afterAll(async () => {
  await mongoose.disconnect();
  if (mongod) await mongod.stop();
});

async function login(app) {
  await request(app).post('/users/register').send({ email: 'notes@example.com', password: 'hunter2', name: 'Notes' });
  const res = await request(app).post('/auth/login').send({ email: 'notes@example.com', password: 'hunter2' });
  return res.body.token;
}

describe('notes CRUD (create + list)', () => {
  it('creates and lists notes for the authenticated user', async () => {
    const app = createApp();
    const token = await login(app);

    const created = await request(app)
      .post('/notes')
      .set('Authorization', `Bearer ${token}`)
      .send({ title: ' First ', body: ' hello ' });
    expect(created.status).toBe(201);
    expect(created.body.title).toBe('First');
    expect(created.body.body).toBe('hello');

    const listed = await request(app).get('/notes').set('Authorization', `Bearer ${token}`);
    expect(listed.status).toBe(200);
    expect(listed.body).toHaveLength(1);
    expect(listed.body[0].id).toBe(created.body.id);
    expect(typeof listed.body[0].createdAt).toBe('string');
  });
});
