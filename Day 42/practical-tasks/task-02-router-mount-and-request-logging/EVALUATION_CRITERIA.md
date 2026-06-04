# Evaluation Criteria — Day 42 — Task 2 — Router mount + logging header

## Scope

`src/app.js` router wiring and middleware.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | JSON body + header per Supertest. |
| Middleware discipline | 30 | Header applied via middleware before handler; uses `next()`. |
| Structure | 15 | Router mounted at `/api/v1`. |

## Pass / fail gates

- `npm test` fails.
- Header set manually inside `/ping` route only (bypasses middleware learning goal).

## AI grading prompt

Ensure `X-Lab-Tag` header is set from middleware on the `api` router, not only inside the `/ping` handler.
