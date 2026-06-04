# Task 04 — Hoisting vs TDZ (Challenge)

## Summary

Reproduce two classic **binding lifecycle** behaviors (`var` vs `let`), then implement a tiny **`setTimeout` harness** that stays testable with Vitest fake timers.

## Learning goals

- Explain and reproduce **hoisting initialization** for `var` vs **TDZ** for `let`.
- Build a small **test seam** around async scheduling without flaky real-time waits.

## Provided files

- `src/hoistingTdzChallenge.js`
- `tests/hoistingTdzChallenge.test.js`

## Prerequisites

- Day 21 theory sections on hoisting and TDZ.
- Skim Vitest fake timers (used in tests only).

## What you will implement

1. `varBindingBeforeInit()` returns `["undefined", undefined]` using a nested function that reads `x` before `var x = 1`.
2. `letBindingThrowsInTdz()` returns `true` when a nested function throws `ReferenceError` from touching `y` before `let y = 1`.
3. `createTimeoutHarness(fn, ms = 0)` returns `{ schedule, flush }`:
   - `schedule()` registers a `setTimeout` that will call `fn` **later** (must not call `fn` synchronously inside `schedule`).
   - `flush()` invokes the pending work **immediately** so tests can avoid waiting real clock time.

## Constraints

- Do not edit tests.
- `createTimeoutHarness` must use a **default parameter** `ms = 0` in its signature.

## Step-by-step guidance

1. Implement the `var`/`let` demos inside standalone nested functions to avoid polluting module scope.
2. For the harness, store the function passed to `setTimeout` in a variable `pending` (or similar). `schedule` assigns `pending` and calls `setTimeout(pending, ms)`. `flush` calls `pending()` if present.

## How to run and verify

```bash
cd "Day 21/practical-tasks/task-04-hoisting-vs-tdz-challenge"
npm install
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `varBindingBeforeInit` | Exact tuple from `var` hoisting read |
| `letBindingThrowsInTdz` | `true` when TDZ throws `ReferenceError` |
| `createTimeoutHarness` | Deterministic `schedule`/`flush` behavior |

## Submission checklist (Git)

- [ ] `npm test` passes

## Hints (optional)

<details><summary>TDZ probe</summary>

Touch the binding in an expression statement like `void y;` before the `let` line inside a nested function.

</details>
