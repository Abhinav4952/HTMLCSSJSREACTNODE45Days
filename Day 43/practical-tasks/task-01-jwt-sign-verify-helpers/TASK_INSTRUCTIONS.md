# Task 1 — Sign and verify JWT helpers

## Summary

Implement **`signUserToken`** and **`verifyUserToken`** using **`jsonwebtoken`** with **HS256** and a **`sub`** claim.

## Learning goals

- Use **`jwt.sign`** and **`jwt.verify`** safely.
- Understand that verification **throws** on invalid tokens.

## Provided files

| File | Purpose |
|------|---------|
| `src/jwtLab.js` | Implement the two exported functions. |
| `tests/jwtLab.test.js` | Unit tests (read-only). |

## What you will implement

1. `signUserToken(subject, secret)` → JWT string with payload `{ sub: subject }`, **`expiresIn: '1h'`**, algorithm **HS256**.
2. `verifyUserToken(token, secret)` → decoded payload object; propagate errors for bad tokens.

## Constraints

- Do not log secrets.
- Only edit `TODO(Day43-task01)` sections.

## How to run and verify

```bash
cd "Day 43/practical-tasks/task-01-jwt-sign-verify-helpers"
npm install
npm test
```

## `TODO` map

| Function | Done means |
|----------|-------------|
| `signUserToken` | Produces verifiable token with `sub`. |
| `verifyUserToken` | Validates signature + returns payload. |

## Submission checklist (Git)

- [ ] `npm test` passes.
