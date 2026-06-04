# Evaluation Criteria — Day 38 — Task 1 — Stable key grocery list

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | Adds items; clears draft; keys remain ids. |
| Keys | 25 | Never downgrades to index keys. |
| Code quality | 20 | Controlled input; `type="button"`. |

## Pass / fail gates

- Build fails.
- Keys use array index.

## AI grading prompt

Verify `App.jsx` implements TODOs and preserves `key={item.id}`.
