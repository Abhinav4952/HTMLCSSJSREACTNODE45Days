# Evaluation Criteria — Day 45 — Task 1 — Register users

## Scope

`src/routes/usersRouter.js` register handler.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | Tests pass for happy + duplicate paths. |
| Security | 30 | bcrypt hashing; no password material in JSON. |
| Validation | 15 | Sensible 400/409 mapping. |

## Pass / fail gates

- Plaintext password persisted in Mongo field other than bcrypt hash.
- `npm test` fails.

## AI grading prompt

Verify bcrypt hashing, duplicate email handling, normalized lowercase email, and absence of password fields in HTTP JSON.
