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

describe('login + profile', () => {
  it('returns JWT and profile via Bearer', async () => {
    const app = createApp();
    await request(app).post('/users/register').send({ email: 'me@example.com', password: 'hunter2', name: 'Me' });

    const login = await request(app).post('/auth/login').send({ email: 'me@example.com', password: 'hunter2' });
    expect(login.status).toBe(200);
    expect(login.body.token).toBeTruthy();

    const profile = await request(app).get('/auth/me').set('Authorization', `Bearer ${login.body.token}`);
    expect(profile.status).toBe(200);
    expect(profile.body.email).toBe('me@example.com');
    expect(profile.body.name).toBe('Me');
    expect(profile.body.id).toBeTruthy();
  });
});
