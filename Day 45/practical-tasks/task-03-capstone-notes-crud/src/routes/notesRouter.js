import { Router } from 'express';
import { requireAuth } from '../middleware/requireAuth.js';
import { Note } from '../models/Note.js';

export const notesRouter = Router();

notesRouter.post('/', requireAuth, async (req, res) => {
  // TODO(Day45-task03): read `{ title, body }` from JSON (`body` optional string). Validate `title` is a non-empty string after trim; if invalid return 400 `{ error: 'invalid_input' }`. Create a `Note` with `userId` set to `req.auth.sub` (ObjectId). Return 201 `{ id, title, body }` with string `id`.
  res.status(501).json({ error: 'todo_create_note' });
});

notesRouter.get('/', requireAuth, async (req, res) => {
  // TODO(Day45-task03): return 200 JSON array of the authenticated user's notes sorted by `createdAt` descending. Each item should be `{ id, title, body, createdAt }` where `createdAt` is an ISO string (`note.createdAt.toISOString()`).
  res.status(501).json({ error: 'todo_list_notes' });
});
