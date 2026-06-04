import request from 'supertest';
import { beforeAll, describe, expect, it } from 'vitest';
import { createApp } from '../src/app.js';

beforeAll(() => {
  process.env.JWT_SECRET = 'jwt-test-secret-do-not-reuse';
});

describe('task-03 roles', () => {
  it('returns 403 for student token on admin route', async () => {
    const app = createApp();
    const login = await request(app).post('/auth/login').send({ username: 'alice', password: 'wonderland' });
    expect(login.status).toBe(200);
    const res = await request(app).get('/admin/summary').set('Authorization', `Bearer ${login.body.token}`);
    expect(res.status).toBe(403);
    expect(res.body.error).toBe('forbidden');
  });

  it('allows admin token', async () => {
    const app = createApp();
    const login = await request(app).post('/auth/login').send({ username: 'root', password: 'sekret' });
    expect(login.status).toBe(200);
    const res = await request(app).get('/admin/summary').set('Authorization', `Bearer ${login.body.token}`);
    expect(res.status).toBe(200);
    expect(res.body).toEqual({ message: 'admin-ok' });
  });

  it('returns 401 without token', async () => {
    const app = createApp();
    const res = await request(app).get('/admin/summary');
    expect(res.status).toBe(401);
  });
});
