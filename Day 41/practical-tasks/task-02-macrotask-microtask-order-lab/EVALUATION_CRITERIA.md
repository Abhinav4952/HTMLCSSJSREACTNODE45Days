# Evaluation Criteria — Day 41 — Task 2 — Macrotask / microtask lab

## Scope

Grade `src/orderLab.js` scheduling only.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 60 | `npm test` ordering matches specification. |
| Concept demonstration | 25 | Uses microtasks before macrotimer without hacks (`while` busy loops, etc.). |
| Code quality | 15 | Clear ordering; no dead code. |

## Pass / fail gates

- Tests fail.
- Busy-waits or `Atomics.wait` used to force ordering.

## Evidence the grader should collect

- `npm test` output.

## AI grading prompt (paste into your grader)

Confirm only `src/orderLab.js` was edited to satisfy Vitest ordering `['sync-a','sync-b','micro-1','promise-1','timer-1']` without changing label strings. Reject hacks that block the event loop.
