# Evaluation Criteria — Day 44 — Task 4 — Validation + timestamps

## Scope

`src/models/Book.js` schema options.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 65 | Vitest cases pass. |
| Validation | 20 | Uses `minlength` (not ad-hoc checks everywhere). |
| Timestamps | 15 | `createdAt` / `updatedAt` via schema option. |

## Pass / fail gates

- `npm test` fails.
- Manual date fields added instead of `timestamps: true` (does not meet learning goal).

## AI grading prompt

Verify `minlength: 3` after trim and `{ timestamps: true }` on schema options object.
