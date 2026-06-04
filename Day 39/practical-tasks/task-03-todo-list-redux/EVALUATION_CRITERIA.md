# Evaluation Criteria — Day 39 — Task 3 — Todo list

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | Add/toggle/remove semantics match instructions. |
| Id discipline | 20 | Stable string ids; ignores blank adds. |
| Immutability / RTK style | 15 | No accidental shared-mutation bugs. |
| Requirements coverage | 10 | Works with provided UI. |

## Pass / fail gates

- Blank todos can be created from whitespace-only input.
- Build fails.

## AI grading prompt

Review `todosSlice.js` reducer implementations against the task brief.
