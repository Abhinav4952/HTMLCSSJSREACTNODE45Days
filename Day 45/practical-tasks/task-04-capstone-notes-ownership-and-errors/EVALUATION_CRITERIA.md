# Evaluation Criteria — Day 45 — Task 4 — Ownership + errors

## Scope

`src/routes/notesRouter.js` patch/delete + `src/app.js` error middleware.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Ownership | 55 | Non-owner receives **403** `{ error: 'forbidden' }` on mutate attempts. |
| HTTP semantics | 25 | Correct **404** / **204** behavior for owner flows. |
| Error middleware | 20 | Last middleware; logs; static JSON for 500 path. |

## Pass / fail gates

- `npm test` fails.
- Cross-tenant update succeeds (automatic fail).

## AI grading prompt

Verify ObjectId ownership checks compare to JWT `sub`, DELETE returns 204 for owner, and error middleware does not leak stack messages to clients.
