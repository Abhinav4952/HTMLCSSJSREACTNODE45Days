# Task 1 — Express JSON health route

## Summary

Create a minimal Express app exposing **`GET /health`** returning JSON **`{ "status": "ok" }`** with status **200**.

## Learning goals

- Wire an Express **`app.get`** route.
- Return JSON with correct status codes.

## Provided files

| File | Purpose |
|------|---------|
| `src/app.js` | Export `createApp()` for tests and reuse. |
| `src/server.js` | Optional manual run (`npm start`). |
| `tests/app.test.js` | Supertest contract (read-only). |

## What you will implement

1. Replace the `TODO(Day42-task01)` stub so `/health` matches the test contract.

## Constraints

- Node **18+**; **ESM** (`"type": "module"`).
- Only edit files containing `TODO(Day42-task01)`.

## How to run and verify

```bash
cd "Day 42/practical-tasks/task-01-express-json-health"
npm install
npm test
```

Optional manual server:

```bash
npm start
# visit http://localhost:4001/health
```

## `TODO` map

| Location | Done means |
|----------|-------------|
| `src/app.js` `/health` handler | Returns `200` + `{ status: 'ok' }`. |

## Submission checklist (Git)

- [ ] `npm test` passes.
