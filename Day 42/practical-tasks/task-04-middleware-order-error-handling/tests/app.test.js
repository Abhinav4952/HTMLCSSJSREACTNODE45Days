import request from 'supertest';
import { describe, expect, it } from 'vitest';
import { createApp } from '../src/app.js';

describe('task-04 middleware order', () => {
  it('parses JSON before hitting /v1/widgets', async () => {
    const app = createApp();
    const res = await request(app).post('/v1/widgets').send({ sku: '  ABC  ' });
    expect(res.status).toBe(201);
    expect(res.body).toEqual({ sku: 'ABC' });
  });
});
