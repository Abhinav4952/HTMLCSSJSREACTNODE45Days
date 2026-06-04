# Task 01 — Counter Factory (Closure State)

## Summary

Implement **`createCounter`** using a **closure** so the numeric total is not a public property on the returned object.

## Learning goals

- Hide mutable state while exposing a small method surface.

## Provided files

- `package.json`, `.npmrc`
- `src/counterFactory.js`, `tests/counterFactory.test.js`

## Prerequisites

- Day 26 theory on factories and private state.

## What you will implement

1. `createCounter(initial = 0)` returning `{ read, inc, reset }` per JSDoc in `src/counterFactory.js`.

## Constraints

- Do not edit tests.
- The running total must not be exposed as `counter.total` or similar on the returned API object (use a closure variable).

## Step-by-step guidance

1. Declare `let total = initial` inside `createCounter`.
2. Return methods that close over `total`.

## How to run and verify

```bash
cd "Day 26/practical-tasks/task-01-counter-factory"
npm install
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `createCounter` | Private `read` / `inc` / `reset` behavior |

## Submission checklist (Git)

- [ ] `npm test` passes
