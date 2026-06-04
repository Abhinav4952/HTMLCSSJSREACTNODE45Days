# Task 3 — Books CRUD over HTTP

## Summary

Implement REST endpoints backed by the **`Book`** Mongoose model: **list, create, read, update, delete**.

## Learning goals

- Map Mongoose documents to **JSON-safe** shapes (`id` string vs `_id`).
- Return meaningful **404**/**400** statuses.

## Environment variables (verbatim)

| Name | Meaning |
|------|---------|
| **`MONGODB_URI`** | Full Mongo URI. |
| **`MONGODB_DB_NAME`** | Logical DB (default **`course-node-45`**). |

Connection logic lives in **`src/db/mongoose.js`**; configuration in **`.env`** / **`src/config/env.js`**.

## What you will implement

1. `GET /books` → `200` sorted by `title` ascending, shape `[{ id, title }, ...]`.
2. `POST /books` → validates `title`, **`201`** `{ id, title }`.
3. `GET /books/:id` → **`200`** or **`404`**.
4. `PATCH /books/:id` → update title with same validation as POST.
5. `DELETE /books/:id` → **`204`** on success, **`404`** if not found.

## Constraints

- Only edit `TODO(Day44-task03)` sections in `src/routes/booksRouter.js`.
- Do not commit `.env`.

## How to run and verify

```bash
cd "Day 44/practical-tasks/task-03-books-crud-routes"
npm install
npm test
```

Optional:

```bash
cp .env.example .env
npm start
```

## `TODO` map

| Route | Done means |
|-------|------------|
| All handlers in `booksRouter.js` | Meet Supertest flow in `tests/books.test.js`. |

## Submission checklist (Git)

- [ ] `npm test` passes.
