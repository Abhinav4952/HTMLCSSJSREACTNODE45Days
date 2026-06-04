# Task 1 — Users: `POST /users/register`

## Summary

Persist a **`User`** with **`bcryptjs`** password hashing. Never return secrets or password hashes in JSON.

## Environment variables (verbatim)

| Name | Meaning |
|------|---------|
| **`MONGODB_URI`** | Full Mongo URI (Atlas/Docker/instructor). |
| **`MONGODB_DB_NAME`** | Logical DB — default **`course-node-45`**. |
| **`JWT_SECRET`** | Used in later Day 45 tasks; set any dev value locally. |

**Connection logic:** `src/db/mongoose.js` (provided). **Configuration:** `.env` + `src/config/env.js`.

## What you will implement

1. `POST /users/register` per inline `TODO(Day45-task01)` contract in `src/routes/usersRouter.js`.

## Constraints

- Only edit `TODO(Day45-task01)` in `src/routes/usersRouter.js`.
- Never commit `.env`.

## How to run and verify

```bash
cd "Day 45/practical-tasks/task-01-capstone-users-register"
npm install
npm test
```

## `TODO` map

| Location | Done means |
|----------|-------------|
| `usersRouter.js` | Passes `tests/users.test.js`. |

## Submission checklist (Git)

- [ ] `npm test` passes.
