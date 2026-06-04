# Evaluation Criteria — Day 43 — Task 2 — Login + Bearer auth

## Scope

`src/app.js` authentication routes; config loader is provided.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | Supertest flows pass. |
| Header format | 25 | Uses `Authorization: Bearer` parsing. |
| Secret handling | 20 | Reads secret from env; no hard-coded prod secret. |

## Pass / fail gates

- `npm test` fails.
- `.env` committed with real production secret.

## AI grading prompt

Verify Bearer parsing, JWT HS256 with `sub`, 401 paths, and absence of committed `.env`.
