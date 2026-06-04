# Evaluation Criteria — Day 45 — Task 2 — Login + JWT profile

## Scope

`src/routes/authRouter.js` middleware + routes.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | Supertest flow passes. |
| JWT hygiene | 25 | HS256 with secret from env; sensible expiry. |
| bcrypt usage | 20 | Compares with `bcrypt.compare`; loads hash with `select`. |

## Pass / fail gates

- `npm test` fails.
- Password hash returned in any JSON response.

## AI grading prompt

Verify Bearer parsing, bcrypt compare, JWT includes `sub` + `email`, `/me` loads user by id from token.
