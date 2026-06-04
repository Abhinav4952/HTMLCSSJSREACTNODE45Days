import { Router } from 'express';
import { Book } from '../models/Book.js';

export const booksRouter = Router();

booksRouter.get('/', async (_req, res) => {
  // TODO(Day44-task03): return 200 JSON array of books sorted by title ascending (use Book.find().sort({ title: 1 })). Each item should be plain `{ id, title }` where `id` is the hex string of `_id`.
  res.status(501).json({ error: 'todo_list' });
});

booksRouter.post('/', async (req, res) => {
  // TODO(Day44-task03): read { title } from JSON body. If missing/empty after trim -> 400 { error: 'invalid_title' }. Else create book -> 201 { id, title }.
  res.status(501).json({ error: 'todo_create' });
});

booksRouter.get('/:id', async (req, res) => {
  // TODO(Day44-task03): return 200 { id, title } or 404 { error: 'not_found' }. Invalid ObjectId -> 404.
  res.status(501).json({ error: 'todo_get' });
});

booksRouter.patch('/:id', async (req, res) => {
  // TODO(Day44-task03): update title from body { title } (validate like POST). 200 { id, title } or 404.
  res.status(501).json({ error: 'todo_patch' });
});

booksRouter.delete('/:id', async (req, res) => {
  // TODO(Day44-task03): delete by id. 204 on success, 404 if missing.
  res.status(501).json({ error: 'todo_delete' });
});
