# Task 4 — Issuer / audience claims (no refresh server)

## Summary

Mint a short-lived JWT with **`issuer`** and **`audience`** options, then verify those constraints on a protected route. This models **claim validation** without building a refresh-token service.

## Learning goals

- Use **`jwt.sign`** / **`jwt.verify`** `issuer` + `audience` options.
- Understand why mismatched **`aud`** should yield **`401`**, not silent success.

## Provided files

| File | Purpose |
|------|---------|
| `src/app.js` | `ISSUER` / `AUDIENCE` constants + `TODO`s. |

## What you will implement

1. **`POST /auth/token`**: return **`200`** `{ token }` where `token` signs `{ sub: 'demo', scope: 'read' }`, **`expiresIn: '15m'`**, **`issuer: ISSUER`**, **`audience: AUDIENCE`**.
2. **`GET /scoped/ping`**: verify Bearer token with **`jwt.verify(token, JWT_SECRET, { issuer: ISSUER, audience: AUDIENCE })`**. Success → **`200`** `{ ok: true, scope: <payload.scope> }`. Failures → **`401`** `{ error: 'unauthorized' }`.

## Constraints

- Only edit `TODO(Day43-task04)` sections in `src/app.js`.

## How to run and verify

```bash
cd "Day 43/practical-tasks/task-04-refresh-free-token-claims"
npm install
npm test
```

## `TODO` map

| Route | Done means |
|-------|------------|
| `/auth/token` | JWT includes issuer/audience + scope claim. |
| `/scoped/ping` | Strict verify options enforced. |

## Submission checklist (Git)

- [ ] `npm test` passes.
