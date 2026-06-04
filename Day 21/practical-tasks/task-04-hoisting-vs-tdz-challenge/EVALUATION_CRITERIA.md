# Evaluation Criteria — Day 21 — Task 04 — Hoisting vs TDZ (Challenge)

## Scope

Graded: `src/hoistingTdzChallenge.js` vs tests.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 40 | Tests pass |
| Code quality | 20 | Nested functions avoid module-scope pollution |
| Requirements coverage | 25 | TDZ + var demos + timeout harness contract |
| Docs / readability | 15 | Clear naming (`pending`, etc.) |

## Pass / fail gates

- Any test failure.
- `fn` invoked synchronously inside `schedule()` (tests will fail).

## AI-assisted grading prompt (optional)

```markdown
## AI grading prompt (paste into your grader)
Context: `Day 21/practical-tasks/task-04-hoisting-vs-tdz-challenge`.
Verify tests pass and `createTimeoutHarness` uses default `ms = 0` in the signature.
```
