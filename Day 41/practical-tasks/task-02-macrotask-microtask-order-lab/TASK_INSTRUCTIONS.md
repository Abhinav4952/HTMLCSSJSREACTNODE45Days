# Task 2 — Macrotasks vs microtasks (measurable ordering)

## Summary

Adjust **timer** and **microtask** registrations so logged steps match the **documented Node ordering** for this small snippet.

## Learning goals

- Predict how **synchronous** code interleaves with **Promise reactions** and **`queueMicrotask`**.
- See why **`setTimeout(..., 0)`** runs after the microtask queue drains.

## Provided files

| File | Purpose |
|------|---------|
| `src/orderLab.js` | Contains the `TODO` — reorder scheduling lines. |
| `tests/orderLab.test.js` | Asserts the final `string[]` ordering. |

## Prerequisites

- Read the Day 41 theory section on the event loop.

## What you will implement

1. Reorder the **`setTimeout`**, **`Promise.resolve().then`**, and **`queueMicrotask`** registrations (and/or their bodies if needed) so `recordExecutionOrder()` resolves to:

   `['sync-a', 'sync-b', 'micro-1', 'promise-1', 'timer-1']`

## Constraints

- Do not change the **labels** (`'sync-a'`, `'micro-1'`, …) — only scheduling structure.
- Only edit `TODO(Day41-task02)` locations in `src/orderLab.js`.

## Step-by-step guidance

1. Write the expected sequence on paper: synchronous logs, then microtasks in FIFO order, then the timer.
2. Register `queueMicrotask` **before** `Promise.resolve().then` if you need `micro-1` before `promise-1`.
3. Keep the final `await new Promise(setTimeout…)` so the macrotask queue gets a turn before the function returns.

## How to run and verify

```bash
cd "Day 41/practical-tasks/task-02-macrotask-microtask-order-lab"
npm install
npm test
```

## `TODO` map

| Location | Done means |
|----------|-------------|
| `src/orderLab.js` | Scheduling produces the exact array asserted in tests. |

## Submission checklist (Git)

- [ ] `npm test` passes.
- [ ] No unrelated files changed.

## Hints

<details>
<summary>Why FIFO matters among microtasks</summary>

Microtasks run in **registration order** for the same turn. Register `queueMicrotask` first if it should precede a Promise reaction scheduled later in the same synchronous block.

</details>
