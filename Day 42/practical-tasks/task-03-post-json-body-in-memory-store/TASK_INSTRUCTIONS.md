# Task 3 — POST JSON + in-memory store

## Summary

Accept **`POST /todos`** with JSON **`{ "title": string }`**, validate it, append to an **in-memory array**, and expose **`GET /todos`** for listing.

## Learning goals

- Use **`express.json()`** before body-reading routes.
- Return **`201 Created`** for successful inserts with a minimal payload echo.

## Provided files

| File | Purpose |
|------|---------|
| `src/app.js` | Express app + TODO handler logic. |
| `tests/app.test.js` | Supertest scenarios. |

## What you will implement

1. Reject empty or non-string `title` with **`400`** JSON `{ "error": "invalid_title" }`.
2. On success, assign **`id`** as `todos.length + 1` **before** pushing (matches test expectation for first item).
3. Return **`201`** with the saved `{ id, title }`.

## Constraints

- In-memory array only (no database).
- Only edit `TODO(Day42-task03)` in `src/app.js`.

## How to run and verify

```bash
cd "Day 42/practical-tasks/task-03-post-json-body-in-memory-store"
npm install
npm test
```

## `TODO` map

| Location | Done means |
|----------|-------------|
| `POST /todos` handler | Validates body, mutates `todos`, correct status codes. |

## Submission checklist (Git)

- [ ] `npm test` passes.
