# Evaluation Criteria — Day 43 — Task 3 — Roles 401 vs 403

## Scope

`src/app.js` only.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 60 | Supertest matrix passes. |
| Status semantics | 30 | 401 vs 403 distinction is correct. |
| Token claims | 10 | `role` present in JWT for both users. |

## Pass / fail gates

- Returns **401** for wrong password (still invalid auth).
- Returns **403** (not 401) for student hitting admin route.

## AI grading prompt

Verify JWT carries `role`, admin route rejects student with 403, rejects missing token with 401.
