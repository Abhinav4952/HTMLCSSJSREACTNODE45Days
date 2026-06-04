# Evaluation Criteria — Day 42 — Task 1 — Express JSON health

## Scope

`src/app.js` health route; tests are authoritative.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 60 | Supertest expectations satisfied. |
| Code quality | 25 | Small handler; uses `res.json`. |
| Conventions | 15 | Keeps `createApp` export for testing. |

## Pass / fail gates

- `npm test` fails.
- Hard-coded port inside `createApp` (listen should stay in `server.js` only).

## AI grading prompt

Verify `/health` returns JSON `{status:'ok'}` with HTTP 200 via Supertest contract.
