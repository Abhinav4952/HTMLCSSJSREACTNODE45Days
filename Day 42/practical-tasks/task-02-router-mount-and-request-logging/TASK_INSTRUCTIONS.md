# Task 2 — Router mount + request middleware

## Summary

Mount an **`express.Router`** under **`/api/v1`** and add **middleware** on that router so every response includes a custom **`X-Lab-Tag`** header.

## Learning goals

- Practice **`app.use(prefix, router)`** mounting.
- Implement middleware that always calls **`next()`** unless you intentionally short-circuit.

## Provided files

| File | Purpose |
|------|---------|
| `src/app.js` | Router + `TODO` middleware. |
| `tests/app.test.js` | Supertest checks JSON + header. |

## What you will implement

1. Middleware on **`api`** that runs for `/ping` too, setting **`X-Lab-Tag: day-42-task-02`** via `res.setHeader` or `res.set`.
2. Keep **`GET /api/v1/ping`** returning `{ pong: true }`.

## Constraints

- Middleware must be registered **before** the `/ping` route on the same `api` router.
- Only edit `TODO(Day42-task02)` in `src/app.js`.

## How to run and verify

```bash
cd "Day 42/practical-tasks/task-02-router-mount-and-request-logging"
npm install
npm test
```

## `TODO` map

| Location | Done means |
|----------|-------------|
| `api.use(...)` middleware | Sets `X-Lab-Tag` header; calls `next()`. |

## Submission checklist (Git)

- [ ] `npm test` passes.
