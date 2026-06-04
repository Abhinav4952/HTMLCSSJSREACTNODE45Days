import jwt from 'jsonwebtoken';
import request from 'supertest';
import { beforeAll, describe, expect, it } from 'vitest';
import { createApp } from '../src/app.js';

beforeAll(() => {
  process.env.JWT_SECRET = 'jwt-test-secret-do-not-reuse';
});

describe('task-04 issuer + audience', () => {
  it('rejects token with wrong audience', async () => {
    const app = createApp();
    const wrong = jwt.sign({ sub: 'demo', scope: 'read' }, process.env.JWT_SECRET, {
      expiresIn: '15m',
      issuer: 'day43-task04-lab',
      audience: 'wrong-audience',
    });
    const res = await request(app).get('/scoped/ping').set('Authorization', `Bearer ${wrong}`);
    expect(res.status).toBe(401);
  });

  it('accepts minted route token', async () => {
    const app = createApp();
    const minted = await request(app).post('/auth/token').send({});
    expect(minted.status).toBe(200);
    const res = await request(app).get('/scoped/ping').set('Authorization', `Bearer ${minted.body.token}`);
    expect(res.status).toBe(200);
    expect(res.body).toEqual({ ok: true, scope: 'read' });
  });
});
