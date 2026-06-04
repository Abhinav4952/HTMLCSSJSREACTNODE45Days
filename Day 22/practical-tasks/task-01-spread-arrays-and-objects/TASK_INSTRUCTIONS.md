# Task 01 — Spread: Arrays and Objects

## Summary

Use **spread** to **merge plain objects** and **prepend** to arrays immutably.

## Learning goals

- Prefer `{ ...a, ...b }` for shallow merges with explicit precedence.
- Build new arrays without mutating inputs.

## Provided files

- `src/spreadLab.js`, `tests/spreadLab.test.js`

## Prerequisites

- Day 22 theory on spread.

## What you will implement

1. `shallowMerge(base, patch)` per JSDoc (reject non-plain objects).
2. `prepend(list, value)` using array spread.

## Constraints

- Do not edit tests.
- `shallowMerge` must use object spread syntax.

## How to run and verify

```bash
cd "Day 22/practical-tasks/task-01-spread-arrays-and-objects"
npm install
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `shallowMerge` | Plain-object guard + merge |
| `prepend` | Array spread prepend |

## Submission checklist (Git)

- [ ] `npm test` passes
