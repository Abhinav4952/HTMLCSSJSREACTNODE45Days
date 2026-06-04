# Evaluation Criteria — Day 21 — Task 01 — Function Declarations vs Expressions

## Scope

Graded: `src/functionFormsLab.js` vs automated tests and quick manual form checks.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 40 | All Vitest cases pass |
| Code quality | 20 | Clear guards; no duplicated validation logic beyond reason |
| Requirements coverage | 25 | Declaration vs expression shapes preserved |
| Docs / readability | 15 | JSDoc intent honored; naming consistent |

## Pass / fail gates (automatic fail if violated)

- Any `npm test` failure.
- `square` rewritten as a `const` arrow/FE instead of a declaration.
- `cube` implemented as an arrow function.

## Detailed rubric

### Correctness

- Returns `NaN` on non-numbers and non-finite values.
- Correct `n * n` and `n * n * n` for finite numbers.

### Edge cases

- `0`, negatives, fractional numbers behave mathematically.

## Evidence the grader should collect

- `npm test` output (all tests passed).

## AI-assisted grading prompt (optional)

```markdown
## AI grading prompt (paste into your grader)
Repository context: `Day 21/practical-tasks/task-01-function-declarations-and-expressions`.
Check: (1) tests pass, (2) `square` is a function declaration, (3) `cube` is `const ... = function`.
Return: Pass/Fail, score table, blocking issues, non-blocking suggestions.
```
