# Task 2 — Login route + `Authorization: Bearer` profile

## Summary

Implement **`POST /auth/login`** to mint a JWT for a demo user, then protect **`GET /me`** using the **`Authorization: Bearer <token>`** header.

## Learning goals

- Load secrets from **`.env`** via **`dotenv`** and `src/config/env.js`.
- Parse the **Bearer** scheme case-sensitively (`Bearer` per spec).

## Provided files

| File | Purpose |
|------|---------|
| `.env.example` | Lists `JWT_SECRET` placeholder (committed). |
| `src/config/env.js` | Validates `JWT_SECRET` presence. |
| `src/app.js` | Express routes with `TODO`s. |
| `src/server.js` | Local listen helper. |

## Prerequisites

- Copy **`.env.example` → `.env`** and set **`JWT_SECRET`** to any non-empty string for `npm start`.
- Vitest sets `JWT_SECRET` automatically in `tests/app.test.js` for CI-like runs.

## What you will implement

1. **`POST /auth/login`**: validate `{ username, password }` against `DEMO_USERS` (`alice` / `wonderland`). Return **`200`** `{ token }` where `token` is an HS256 JWT with `{ sub: username }` and **`expiresIn: '1h'`**. Wrong credentials → **`401`** `{ error: 'invalid_credentials' }`.
2. **`GET /me`**: require header **`Authorization: Bearer <jwt>`**. Verified → **`200`** `{ user: <sub> }`**. Missing/invalid → **`401`** `{ error: 'unauthorized' }**.

## Constraints

- Never commit **`.env`**; rubric fails if secrets appear in git history for this assignment.
- Only edit `TODO(Day43-task02)` sections in `src/app.js`.

## How to run and verify

```bash
cd "Day 43/practical-tasks/task-02-login-route-bearer-auth"
npm install
npm test
```

Optional manual:

```bash
cp .env.example .env # then edit JWT_SECRET
npm start
```

## `TODO` map

| Location | Done means |
|----------|-------------|
| `/auth/login` | Issues JWT for valid demo user. |
| `/me` | Validates Bearer token; returns `sub`. |

## Submission checklist (Git)

- [ ] `.env` not committed.
- [ ] `npm test` passes.
