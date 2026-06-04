# Task 2 — Book schema + `create`

## Summary

Define a **Mongoose schema** for a **`Book`** with a **`title`** field that is **required** and **trimmed**, then prove **`Book.create`** persists normalized data.

## Learning goals

- Create a **model** with `mongoose.model`.
- Use schema options like **`trim`** and **`required`**.

## Environment variables (verbatim)

| Name | Meaning |
|------|---------|
| **`MONGODB_URI`** | Full Mongo connection string (instructor/Atlas/Docker). |
| **`MONGODB_DB_NAME`** | Logical DB — default **`course-node-45`**. |

Files: **`.env`** (local secrets, gitignored), **`.env.example`** (key names only), `src/config/env.js`, `src/db/mongoose.js` (connection — provided wired), **`src/models/Book.js`** (your `TODO`).

## What you will implement

1. Add **`trim: true`** to the existing `title` definition so the provided test normalizes whitespace.

## Constraints

- Only edit `TODO(Day44-task02)` in `src/models/Book.js`.
- Never commit `.env`.

## How to run and verify

```bash
cd "Day 44/practical-tasks/task-02-schema-model-create-book"
npm install
npm test
```

## `TODO` map

| File | Done means |
|------|------------|
| `src/models/Book.js` | Schema enforces trimmed required title. |

## Submission checklist (Git)

- [ ] `npm test` passes.
