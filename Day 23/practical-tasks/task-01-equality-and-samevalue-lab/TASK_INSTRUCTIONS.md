# Task 01 — Equality & `Object.is`

## Summary

Implement a tiny classifier that surfaces the difference between **`Object.is`**, **`===`**, and **`==`**.

## Learning goals

- Use `Object.is` for `NaN` and signed-zero comparisons.

## Provided files

- `src/equalityLab.js`, `tests/equalityLab.test.js`

## Prerequisites

- Day 23 theory on sameness.

## What you will implement

1. `classifyEquality(a, b)` exactly per JSDoc ordering (`Object.is` first, then `===`, then `==`).

## Constraints

- Do not edit tests.

## How to run and verify

```bash
cd "Day 23/practical-tasks/task-01-equality-and-samevalue-lab"
npm install
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `classifyEquality` | Correct branch ordering |

## Submission checklist (Git)

- [ ] `npm test` passes
