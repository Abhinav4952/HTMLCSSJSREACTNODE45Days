# Evaluation Criteria — Day 21 — Task 02 — Arrow Functions for Callbacks

## Scope

Graded: `src/arrowLab.js` vs tests + light manual check for arrow usage in `map`.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 40 | Tests pass |
| Code quality | 20 | Small pure helpers; readable pair normalization |
| Requirements coverage | 25 | Arrow callback in `map`; returned arrow from HOF |
| Docs / readability | 15 | Matches JSDoc contract |

## Pass / fail gates

- Any test failure.
- `map` rewritten to use a `function` keyword callback.

## Detailed rubric

### Correctness

- `null` for non-arrays; numeric coercion rules per tests.

### Edge cases

- Missing pair elements become `0`.

## Evidence the grader should collect

- `npm test` log.

## AI-assisted grading prompt (optional)

```markdown
## AI grading prompt (paste into your grader)
Context: `Day 21/practical-tasks/task-02-arrow-functions-callbacks`.
Verify tests pass and `sumPairs` uses `.map((...) => ...)` (arrow). Summarize issues.
```
