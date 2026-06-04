# Task 4 — Ownership on mutate + error middleware

## Summary

Finish **`PATCH /notes/:id`** and **`DELETE /notes/:id`** with strict **ownership checks** (`note.userId` vs JWT `sub`). Add a final **Express error middleware** that logs server-side but returns a **generic JSON** error for unexpected failures.

## Environment variables (verbatim)

| Name | Meaning |
|------|---------|
| **`MONGODB_URI`** | Full Mongo URI. |
| **`MONGODB_DB_NAME`** | Logical DB — default **`course-node-45`**. |
| **`JWT_SECRET`** | JWT signing secret. |

## What you will implement

1. `PATCH` / `DELETE` behaviors described in `TODO(Day45-task04)` inside `src/routes/notesRouter.js`.
2. Error middleware described in `TODO(Day45-task04)` inside `src/app.js` (register **after** routes).

## Constraints

- Only edit `TODO(Day45-task04)` markers in `src/routes/notesRouter.js` and `src/app.js`.
- Never echo raw `err.message` to clients from the 500 handler.

## How to run and verify

```bash
cd "Day 45/practical-tasks/task-04-capstone-notes-ownership-and-errors"
npm install
npm test
```

## `TODO` map

| File | Done means |
|------|------------|
| `notesRouter.js` | Ownership enforced; correct 204/403/404 semantics. |
| `app.js` | Centralized 500 JSON error handler present **after** routes. |

## Submission checklist (Git)

- [ ] `npm test` passes.
