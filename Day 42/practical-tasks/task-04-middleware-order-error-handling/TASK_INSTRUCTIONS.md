# Task 4 — Fix middleware order (`express.json`)

## Summary

The starter registers **`express.json()`** *after* the **`/v1`** router. That means **`req.body`** is still **`undefined`** when your POST handler runs. Move middleware so JSON parsing happens **before** routed handlers execute.

## Learning goals

- Explain why **body-parser middleware** must precede routes that read **`req.body`**.
- Keep an **error middleware** registered after routes (pattern preserved).

## Provided files

| File | Purpose |
|------|---------|
| `src/app.js` | Broken order + `TODO` comment. |
| `tests/app.test.js` | Supertest POST with JSON body. |

## What you will implement

1. Reorder middleware so **`POST /v1/widgets`** receives parsed JSON and returns **`201`** with trimmed `sku` per handler logic.

## Constraints

- Do not weaken validation (`sku` must be non-empty string after trim).
- Only edit the `TODO(Day42-task04)` region / lines necessary to fix ordering (you may relocate `express.json()` registration).

## How to run and verify

```bash
cd "Day 42/practical-tasks/task-04-middleware-order-error-handling"
npm install
npm test
```

## `TODO` map

| Location | Done means |
|----------|-------------|
| `src/app.js` | `express.json()` runs before `/v1` router; tests pass. |

## Submission checklist (Git)

- [ ] `npm test` passes.

## Hints

<details>
<summary>Spoiler</summary>

Call `app.use(express.json())` **before** `app.use('/v1', v1)`.

</details>
