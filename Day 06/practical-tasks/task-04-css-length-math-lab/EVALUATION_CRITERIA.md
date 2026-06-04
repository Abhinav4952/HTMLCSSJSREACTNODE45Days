# Evaluation Criteria — Day 06 — Task 04 — CSS Length Math Lab

## Scope

Graded: `src/unitsLab.js` behavior as locked by `tests/unitsLab.test.js`.  
Out of scope: performance micro-optimizations, parsing arbitrary CSS units beyond lab API.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 60 | All tests pass |
| Requirements coverage | 25 | Implements full public API |
| Code quality | 15 | Readable, small helpers OK, no cleverness that breaks contracts |

## Pass / fail gates

- Any test failure.
- Tests edited (integrity gate unless instructor explicitly allows).

## Evidence the grader should collect

- Paste `npm test` summary showing all tests passed.

## AI grading prompt

Run vitest in task folder. Confirm unitsLab exports match TASK_INSTRUCTIONS. If tests pass, score high; if failures, enumerate failing test names and likely missing edge case handling.
