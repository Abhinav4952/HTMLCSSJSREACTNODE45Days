# Task 02 — Rest Parameters Aggregator

## Summary

Practice **rest parameters** to collect trailing arguments and forward values to **`Math.max`** with **call-time spread**.

## Learning goals

- Use `...rest` in a function signature (not only spread in arrays).
- Combine rest with validation filters.

## Provided files

- `src/restLab.js`, `tests/restLab.test.js`

## Prerequisites

- Day 22 theory on rest vs `arguments`.

## What you will implement

1. `firstAndRestSum(first, ...rest)` per JSDoc.
2. `maxFinite(...values)` ignoring non-finite numbers; return `Math.max` over the remaining list, or `NaN` if empty.

## Constraints

- `firstAndRestSum` must declare `...rest` in its signature.
- Do not edit tests.

## How to run and verify

```bash
cd "Day 22/practical-tasks/task-02-rest-parameters-aggregator"
npm install
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `firstAndRestSum` | Rest aggregation + validation |
| `maxFinite` | `Math.max(...finiteNumbers)` pattern |

## Submission checklist (Git)

- [ ] `npm test` passes
