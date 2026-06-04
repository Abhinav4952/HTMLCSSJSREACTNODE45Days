# Evaluation Criteria — Day 38 — Task 2 — Reorder keys fix

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Keys | 60 | Uses stable per-item keys; no index keys remain. |
| Correctness | 25 | Reorder + controlled editing behave coherently after fix. |
| Code quality | 15 | No unnecessary rerender hacks. |

## Pass / fail gates

- Index keys remain.
- Build fails.

## AI grading prompt

Search `App.jsx` for `key={` patterns; confirm stable ids used.
