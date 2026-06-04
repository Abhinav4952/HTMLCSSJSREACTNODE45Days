# Task 03 — `bind` and Partial Application

## Summary

Use **`bind`** to fix the first argument of a function and to **detach a method** safely bound to its object.

## Learning goals

- Partially apply arguments without invoking immediately.
- Prevent `this` loss when extracting methods.

## Provided files

- `src/bindLab.js`, `tests/bindLab.test.js`

## Constraints

- `bindFirstArg` must use `Function.prototype.bind`.
- `bindMethod` must use `bind`.

## How to run and verify

```bash
cd "Day 24/practical-tasks/task-03-bind-partial-application"
npm install
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `bindFirstArg` | `fn.bind(null, first)` or equivalent receiver |
| `bindMethod` | `obj[methodName].bind(obj)` |

## Submission checklist (Git)

- [ ] `npm test` passes
