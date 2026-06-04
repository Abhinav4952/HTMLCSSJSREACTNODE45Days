# Evaluation Criteria — Day 44 — Task 2 — Book schema

## Scope

`src/models/Book.js` schema definition.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 60 | Vitest create + trim expectation passes. |
| Modeling | 25 | Uses Mongoose schema options idiomatically. |
| Hygiene | 15 | No secrets committed. |

## Pass / fail gates

- `npm test` fails.
- Uses native Mongo driver instead of Mongoose.

## AI grading prompt

Verify `Book` schema requires trimmed string `title` and `Book.create` normalizes whitespace per test.
