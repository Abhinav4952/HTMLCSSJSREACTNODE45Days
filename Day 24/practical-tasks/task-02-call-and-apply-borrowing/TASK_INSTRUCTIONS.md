# Task 02 — `call` and `apply` Borrowing

## Summary

Borrow a method from a shared object using **`.call`**, and forward an array to **`Math.max`** using **`.apply`**.

## Learning goals

- Choose `call` vs `apply` based on argument shape.

## Provided files

- `src/callApplyLab.js`, `tests/callApplyLab.test.js`

## Constraints

- `renderWithHost` must use `.call`.
- `maxWithApply` must use `.apply` (no spread forwarding to `Math.max`).

## How to run and verify

```bash
cd "Day 24/practical-tasks/task-02-call-and-apply-borrowing"
npm install
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `renderWithHost` | `labeler.render.call(host)` |
| `maxWithApply` | `Math.max.apply(null, numbers)` |

## Submission checklist (Git)

- [ ] `npm test` passes
