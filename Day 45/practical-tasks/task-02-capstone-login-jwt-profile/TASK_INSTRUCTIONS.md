# Task 2 — Login + JWT + `/auth/me`

## Summary

Add **`POST /auth/login`** (bcrypt verify + JWT) and **`GET /auth/me`** protected by **`Authorization: Bearer`**.

## Environment variables (verbatim)

| Name | Meaning |
|------|---------|
| **`MONGODB_URI`** | Full Mongo URI. |
| **`MONGODB_DB_NAME`** | Logical DB — default **`course-node-45`**. |
| **`JWT_SECRET`** | HS256 signing secret (dev value in `.env`). |

**Connection:** `src/db/mongoose.js`. **Secrets:** `.env` (gitignored) + `.env.example`.

## What you will implement

1. `requireAuth` middleware + `POST /auth/login` + `GET /auth/me` per `TODO(Day45-task02)` in `src/routes/authRouter.js`.

## Constraints

- Only edit `TODO(Day45-task02)` markers in `src/routes/authRouter.js` (you may replace stub bodies entirely within that file for the TODO sections).
- Use **Bearer** tokens only.

## How to run and verify

```bash
cd "Day 45/practical-tasks/task-02-capstone-login-jwt-profile"
npm install
npm test
```

## `TODO` map

| Location | Done means |
|----------|------------|
| `authRouter.js` | Tests pass for login + `/me`. |

## Submission checklist (Git)

- [ ] `.env` not committed.
