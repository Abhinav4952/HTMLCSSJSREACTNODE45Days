# Task 3 — Roles: `401` vs `403`

## Summary

Extend login tokens with a **`role`** claim and protect an admin-only route. Valid token but wrong role → **`403 Forbidden`**. Missing/invalid token → **`401 Unauthorized`**.

## Learning goals

- Encode **authorization** data in signed claims (lab-scale; real systems often fetch roles server-side).
- Map outcomes to the correct HTTP status codes.

## Provided files

| File | Purpose |
|------|---------|
| `src/app.js` | Demo users + `TODO` handlers. |
| `src/config/env.js` | `JWT_SECRET` loader. |

## What you will implement

1. **`POST /auth/login`**: same pattern as Day 43 task 2, but JWT payload must include **`role`** from `DEMO_USERS`.
2. **`GET /admin/summary`**: Bearer JWT required. **`401`** `{ error: 'unauthorized' }` when missing/invalid. **`403`** `{ error: 'forbidden' }` when `role !== 'admin'`. Success **`200`** `{ message: 'admin-ok' }`.

## Constraints

- Use **`Authorization: Bearer`** header parsing.
- Only edit `TODO(Day43-task03)` sections in `src/app.js`.

## How to run and verify

```bash
cd "Day 43/practical-tasks/task-03-roles-401-vs-403"
npm install
npm test
```

## `TODO` map

| Route | Done means |
|-------|------------|
| `/auth/login` | JWT includes `role`. |
| `/admin/summary` | Correct 401/403/200 behavior. |

## Submission checklist (Git)

- [ ] `npm test` passes; `.env` not committed.
