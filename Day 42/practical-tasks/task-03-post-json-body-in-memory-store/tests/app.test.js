import request from 'supertest';
import { describe, expect, it } from 'vitest';
import { createApp } from '../src/app.js';

describe('task-03 todos memory store', () => {
  it('creates and lists todos', async () => {
    const app = createApp();
    const bad = await request(app).post('/todos').send({ title: '' });
    expect(bad.status).toBe(400);

    const created = await request(app).post('/todos').send({ title: 'Learn middleware' });
    expect(created.status).toBe(201);
    expect(created.body).toMatchObject({ id: 1, title: 'Learn middleware' });

    const listed = await request(app).get('/todos');
    expect(listed.status).toBe(200);
    expect(listed.body).toEqual([{ id: 1, title: 'Learn middleware' }]);
  });
});
