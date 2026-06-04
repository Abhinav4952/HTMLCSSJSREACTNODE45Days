# Task 03 — Lexicographic vs Numeric Comparisons

## Summary

Contrast **string relational comparison** with **numeric coercion**—the classic `"2" > "12"` trap.

## Learning goals

- Predict `<`/`>` behavior when both operands are strings.
- Use explicit `Number(...)` when you mean math.

## Provided files

- `src/relationalLab.js`, `tests/relationalLab.test.js`

## How to run and verify

```bash
cd "Day 23/practical-tasks/task-03-comparison-and-relationals"
npm install
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `isLexicographicGreater` | String `>` |
| `isNumericGreater` | Finite number guard + numeric `>` |

## Submission checklist (Git)

- [ ] `npm test` passes
