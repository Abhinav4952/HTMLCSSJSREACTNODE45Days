import { Router } from 'express';
import { requireAuth } from '../middleware/requireAuth.js';
import { Note } from '../models/Note.js';

export const notesRouter = Router();

notesRouter.post('/', requireAuth, async (req, res) => {
  const { title, body = '' } = req.body ?? {};
  if (!title || typeof title !== 'string' || title.trim() === '') {
    return res.status(400).json({ error: 'invalid_input' });
  }
  if (body !== undefined && typeof body !== 'string') {
    return res.status(400).json({ error: 'invalid_input' });
  }
  const note = await Note.create({ userId: req.auth.sub, title: title.trim(), body: String(body).trim() });
  return res.status(201).json({ id: note._id.toString(), title: note.title, body: note.body });
});

notesRouter.get('/', requireAuth, async (req, res) => {
  const notes = await Note.find({ userId: req.auth.sub }).sort({ createdAt: -1 });
  return res.json(
    notes.map((n) => ({
      id: n._id.toString(),
      title: n.title,
      body: n.body,
      createdAt: n.createdAt.toISOString(),
    })),
  );
});

notesRouter.patch('/:id', requireAuth, async (req, res) => {
  // TODO(Day45-task04): validate optional `{ title, body }` strings similar to POST. Load note by `:id`. If not found -> 404 `{ error: 'not_found' }`. If `note.userId` does not equal `req.auth.sub` -> 403 `{ error: 'forbidden' }`. Apply updates and return 200 `{ id, title, body }`.
  res.status(501).json({ error: 'todo_patch' });
});

notesRouter.delete('/:id', requireAuth, async (req, res) => {
  // TODO(Day45-task04): delete note only if owned by `req.auth.sub`. Wrong owner -> 403 `{ error: 'forbidden' }`. Missing -> 404. Success -> 204 no body.
  res.status(501).json({ error: 'todo_delete' });
});
