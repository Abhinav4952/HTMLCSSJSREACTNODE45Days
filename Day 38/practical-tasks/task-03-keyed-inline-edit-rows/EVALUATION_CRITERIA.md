# Evaluation Criteria — Day 38 — Task 3 — Keyed inline edits

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Keys | 70 | Keys stable across label edits. |
| Correctness | 20 | Controlled updates still work. |
| Code quality | 10 | Minimal diff; no unrelated refactors. |

## Pass / fail gates

- Composite key including `label` remains.
- Build fails.

## AI grading prompt

Verify `<li key=...>` uses only stable ids.
