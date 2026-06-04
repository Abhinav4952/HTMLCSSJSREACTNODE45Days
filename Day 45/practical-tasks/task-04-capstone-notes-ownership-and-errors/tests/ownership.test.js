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

async function registerAndLogin(app, email) {
  await request(app).post('/users/register').send({ email, password: 'pw', name: 'User' });
  const login = await request(app).post('/auth/login').send({ email, password: 'pw' });
  return login.body.token;
}

describe('ownership + delete', () => {
  it('returns 403 when another user tries to patch a note', async () => {
    const app = createApp();
    const tokenA = await registerAndLogin(app, 'a4@example.com');
    const tokenB = await registerAndLogin(app, 'b4@example.com');

    const created = await request(app).post('/notes').set('Authorization', `Bearer ${tokenA}`).send({ title: 'Secret' });
    expect(created.status).toBe(201);

    const attacked = await request(app)
      .patch(`/notes/${created.body.id}`)
      .set('Authorization', `Bearer ${tokenB}`)
      .send({ title: 'Hacked' });
    expect(attacked.status).toBe(403);
    expect(attacked.body.error).toBe('forbidden');
  });

  it('allows owner to delete', async () => {
    const app = createApp();
    const token = await registerAndLogin(app, 'owner@example.com');
    const created = await request(app).post('/notes').set('Authorization', `Bearer ${token}`).send({ title: 'Temp' });
    const deleted = await request(app).delete(`/notes/${created.body.id}`).set('Authorization', `Bearer ${token}`);
    expect(deleted.status).toBe(204);
  });
});
