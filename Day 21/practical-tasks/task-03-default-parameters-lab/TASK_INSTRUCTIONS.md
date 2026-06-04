# Task 03 — Default Parameters Lab

## Summary

Implement **`buildLabel`** and **`repeatText`** using ES2015 **default parameters** where specified, while keeping validation rules explicit.

## Learning goals

- Use defaults that trigger only for `undefined` arguments.
- Avoid treating `null`/`0` as “missing” unless the spec says so.

## Provided files

- `src/defaultParamsLab.js`
- `tests/defaultParamsLab.test.js`

## Prerequisites

- Day 21 theory on default parameters.

## What you will implement

1. `buildLabel(parts, separator = " | ", emptyFallback = "(none)")` per JSDoc.
2. `repeatText(text, times = 1)` with string guard and `times` clamping rules in tests.

## Constraints

- `buildLabel` must declare `separator` and `emptyFallback` defaults in the **function signature** (not only `??` fallback inside the body for those parameters).
- Do not edit tests.

## Step-by-step guidance

1. Guard `parts` early.
2. Normalize strings: trim, drop empties, join.
3. For `repeatText`, after default binding resolves, normalize `times` to an integer in `[0, 5]`; otherwise behave as `times === 1`.

## How to run and verify

```bash
cd "Day 21/practical-tasks/task-03-default-parameters-lab"
npm install
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `buildLabel` | Join + fallback + null guard |
| `repeatText` | Repeat rules + non-string guard |

## Submission checklist (Git)

- [ ] `npm test` passes
