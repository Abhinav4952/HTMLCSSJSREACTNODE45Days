# Evaluation Criteria — Day 39 — Task 1 — Counter slice

## Scope

Graded: `src/features/counter/counterSlice.js` reducer behavior.  
Out of scope: changing `Counter.jsx` unless instructor override.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | Increment/decrement/reset semantics, including clamp at 0. |
| Redux idioms | 25 | Uses RTK/Immer-style updates; no illegal external mutation of `state`. |
| Requirements coverage | 20 | Works with provided UI without further edits. |

## Pass / fail gates

- `npm run build` fails after candidate changes.
- Counter can become negative.

## AI grading prompt (paste into your grader)

Evaluate only `counterSlice.js`. Check reducer logic for `increment`, `decrement` (clamp), and `reset`. Return Pass/Fail + brief notes.
