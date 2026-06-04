# Evaluation Criteria — Day 42 — Task 4 — Middleware order fix

## Scope

`src/app.js` ordering; handler logic should remain equivalent aside from parsing fix.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 70 | Supertest POST succeeds with JSON body. |
| Middleware reasoning | 20 | Candidate explanation in PR/comments optional but encouraged. |
| Safety | 10 | Error middleware remains last among non-router layers. |

## Pass / fail gates

- `npm test` fails.
- Candidate hacks handler to read raw string instead of fixing middleware order (reject: defeats learning goal).

## AI grading prompt

Verify fix uses proper `express.json()` ordering ahead of router; POST `/v1/widgets` returns trimmed sku.
