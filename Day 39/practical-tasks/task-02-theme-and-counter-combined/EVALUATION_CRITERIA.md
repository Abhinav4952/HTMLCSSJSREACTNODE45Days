# Evaluation Criteria — Day 39 — Task 2 — Theme slice

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 60 | Toggle alternates only `light`/`dark`. |
| Store composition | 20 | Does not break `counter` slice behavior. |
| Code quality | 20 | Minimal, idiomatic RTK reducer. |

## Pass / fail gates

- `npm run build` fails.
- Introduces invalid `mode` strings.

## AI grading prompt

Evaluate `themeSlice.js` for `toggleMode` behavior only.
