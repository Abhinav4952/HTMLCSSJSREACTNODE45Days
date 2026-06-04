import express from 'express';

const todos = [];

export function createApp() {
  const app = express();
  app.use(express.json());

  app.get('/todos', (_req, res) => {
    res.json(todos);
  });

  app.post('/todos', (req, res) => {
    // TODO(Day42-task03): require JSON body { "title": string non-empty }. On success push { id, title } (use `todos.length + 1` as numeric id) and return 201 JSON of saved record. On bad input return 400 JSON { error: 'invalid_title' }.
    res.status(501).json({ error: 'todo_post' });
  });

  return app;
}
