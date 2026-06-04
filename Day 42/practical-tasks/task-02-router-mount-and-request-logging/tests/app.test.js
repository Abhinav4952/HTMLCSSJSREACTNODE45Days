import request from 'supertest';
import { describe, expect, it } from 'vitest';
import { createApp } from '../src/app.js';

describe('task-02 router + header middleware', () => {
  it('mounts router at /api/v1/ping and sets X-Lab-Tag header', async () => {
    const app = createApp();
    const res = await request(app).get('/api/v1/ping');
    expect(res.status).toBe(200);
    expect(res.body).toEqual({ pong: true });
    expect(res.headers['x-lab-tag']).toBe('day-42-task-02');
  });
});
