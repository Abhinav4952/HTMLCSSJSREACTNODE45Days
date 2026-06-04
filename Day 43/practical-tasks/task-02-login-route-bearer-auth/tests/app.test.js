import request from 'supertest';
import { beforeAll, describe, expect, it } from 'vitest';
import { createApp } from '../src/app.js';

beforeAll(() => {
  process.env.JWT_SECRET = 'jwt-test-secret-do-not-reuse';
});

describe('task-02 login + bearer', () => {
  it('logs in demo user and reads /me with Bearer token', async () => {
    const app = createApp();
    const login = await request(app).post('/auth/login').send({ username: 'alice', password: 'wonderland' });
    expect(login.status).toBe(200);
    expect(login.body.token).toBeTruthy();

    const me = await request(app).get('/me').set('Authorization', `Bearer ${login.body.token}`);
    expect(me.status).toBe(200);
    expect(me.body).toEqual({ user: 'alice' });
  });

  it('rejects bad password', async () => {
    const app = createApp();
    const res = await request(app).post('/auth/login').send({ username: 'alice', password: 'wrong' });
    expect(res.status).toBe(401);
  });
});
