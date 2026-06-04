# Evaluation Criteria — Day 45 — Task 3 — Notes create/list

## Scope

`src/routes/notesRouter.js`.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 60 | Supertest flow passes. |
| Ownership | 25 | `userId` always derived from JWT `sub`. |
| Serialization | 15 | ISO timestamps in JSON list. |

## Pass / fail gates

- `npm test` fails.
- Accepts `userId` from request body/query overriding JWT subject.

## AI grading prompt

Verify notes are filtered by authenticated user, sorted `createdAt` desc, and `POST` validates `title`.
