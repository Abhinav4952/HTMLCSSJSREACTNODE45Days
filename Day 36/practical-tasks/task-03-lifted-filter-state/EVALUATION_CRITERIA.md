# Evaluation Criteria — Day 36 — Task 3 — Lifted filter

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 50 | Filtering rules + controlled field behavior. |
| State placement | 25 | Query owned by `App`; no second hidden query state. |
| Code quality | 15 | Keys on list items; readable handlers. |
| Requirements | 10 | Case-insensitive match; empty query shows all. |

## Pass / fail gates

- Build fails.
- Filter logic embedded only inside `SearchField` instead of list (wrong decomposition).

## AI grading prompt

Verify three files for TODO completion and list keys.
