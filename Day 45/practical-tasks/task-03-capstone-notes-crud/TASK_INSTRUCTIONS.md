# Task 3 — Authenticated notes (create + list)

## Summary

Add **`POST /notes`** and **`GET /notes`** protected by JWT auth. Notes are always scoped to the **`userId`** from the token’s **`sub`** claim.

## Environment variables (verbatim)

| Name | Meaning |
|------|---------|
| **`MONGODB_URI`** | Full Mongo URI. |
| **`MONGODB_DB_NAME`** | Logical DB — default **`course-node-45`**. |
| **`JWT_SECRET`** | JWT signing secret. |

## What you will implement

1. `POST /notes` and `GET /notes` per `TODO(Day45-task03)` in `src/routes/notesRouter.js`.

## Constraints

- Only edit `TODO(Day45-task03)` sections in `src/routes/notesRouter.js`.
- Never trust a client-sent `userId` field—derive ownership from **`req.auth.sub`**.

## How to run and verify

```bash
cd "Day 45/practical-tasks/task-03-capstone-notes-crud"
npm install
npm test
```

## `TODO` map

| Route | Done means |
|-------|------------|
| `POST /notes` | Creates row with correct `userId`. |
| `GET /notes` | Lists only that user’s notes, sorted newest first. |

## Submission checklist (Git)

- [ ] `npm test` passes.
