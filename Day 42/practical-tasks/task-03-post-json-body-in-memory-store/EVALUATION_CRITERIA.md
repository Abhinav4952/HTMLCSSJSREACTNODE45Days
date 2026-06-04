# Evaluation Criteria — Day 42 — Task 3 — POST JSON in-memory todos

## Scope

`src/app.js` POST/GET handlers.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 60 | Status codes + JSON per tests. |
| Validation | 25 | Title must be non-empty string. |
| Structure | 15 | JSON middleware present before routes. |

## Pass / fail gates

- `npm test` fails.
- IDs random or UUID when tests expect deterministic integer pattern.

## AI grading prompt

Validate POST `/todos` rejects blank title, accepts first todo with id 1, GET lists stored record.
