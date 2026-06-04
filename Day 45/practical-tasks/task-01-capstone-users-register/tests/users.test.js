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

describe('register', () => {
  it('creates user without leaking password fields', async () => {
    const app = createApp();
    const res = await request(app).post('/users/register').send({
      email: 'Ada@Example.com',
      password: 'super-secret',
      name: 'Ada',
    });
    expect(res.status).toBe(201);
    expect(res.body).toMatchObject({ email: 'ada@example.com', name: 'Ada' });
    expect(res.body.id).toBeTruthy();
    expect(res.body.password ?? res.body.passwordHash).toBeUndefined();
  });

  it('returns 409 on duplicate email', async () => {
    const app = createApp();
    await request(app).post('/users/register').send({ email: 'dup@example.com', password: 'a', name: 'A' });
    const dup = await request(app).post('/users/register').send({ email: 'dup@example.com', password: 'b', name: 'B' });
    expect(dup.status).toBe(409);
  });
});
