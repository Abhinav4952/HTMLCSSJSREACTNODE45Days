# Evaluation Criteria — Day 43 — Task 1 — JWT helpers

## Scope

`src/jwtLab.js` only.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 60 | Tests pass for sign/verify. |
| Security hygiene | 25 | No secret logging; uses HS256 + expiry. |
| API clarity | 15 | Small surface; throws on bad verify. |

## Pass / fail gates

- `npm test` fails.
- Hard-coded production secret in source.

## AI grading prompt

Confirm HS256 signing with `sub` + `expiresIn: '1h'` and verify throws on wrong secret.
