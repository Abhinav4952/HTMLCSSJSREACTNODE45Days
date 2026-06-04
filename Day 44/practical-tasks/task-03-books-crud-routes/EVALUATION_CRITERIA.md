# Evaluation Criteria — Day 44 — Task 3 — Books CRUD

## Scope

`src/routes/booksRouter.js` handlers; model file is provided.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 60 | CRUD Supertest flow passes. |
| HTTP semantics | 25 | Correct 201/204/404/400 usage. |
| Data mapping | 15 | Returns string `id` fields, sorted list. |

## Pass / fail gates

- `npm test` fails.
- Leaks raw Mongo `_id` objects without serializing.

## AI grading prompt

Verify CRUD behavior, validation on POST/PATCH, sorted GET list, and 404 handling for missing/invalid ids.
