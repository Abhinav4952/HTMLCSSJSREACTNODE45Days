# Task 04 — `for..of` + `Object.values` Pipeline

## Summary

Iterate collections with **`for...of`**, combining **`Object.values`** for plain-object scans.

## Learning goals

- Prefer `for..of` when you need early `break`/`continue` and readable loops.
- Avoid mutating inputs while aggregating.

## Provided files

- `src/forOfLab.js`, `tests/forOfLab.test.js`

## Prerequisites

- Day 22 theory on `for..of`.

## What you will implement

1. `productOfNumericValues(record)` using `for (const v of Object.values(record))`.
2. `sumPairValues(entries)` using `for..of` directly on the `entries` array.

## Constraints

- Do not edit tests.
- Both functions must include a `for...of` loop (not only `.forEach`).

## How to run and verify

```bash
cd "Day 22/practical-tasks/task-04-for-of-and-entries-pipeline"
npm install
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `productOfNumericValues` | Product with `Object.values` + `for..of` |
| `sumPairValues` | Sum pairs with `for..of` |

## Submission checklist (Git)

- [ ] `npm test` passes
