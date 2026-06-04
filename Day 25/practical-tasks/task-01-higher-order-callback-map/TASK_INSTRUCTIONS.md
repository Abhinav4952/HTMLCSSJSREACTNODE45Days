# Task 01 — Higher-Order Callbacks

## Summary

Implement **`mapWith`** as a tiny HOF-style wrapper and build **`negate`** for predicate composition.

## Learning goals

- Pass functions as values (`fn` parameter to `mapWith`).
- Return a new function from `negate` that closes over the supplied predicate.

## Provided files

- `package.json`, `.npmrc`
- `src/callbackLab.js`, `tests/callbackLab.test.js`

## Prerequisites

- Day 25 theory on callbacks and higher-order functions.

## What you will implement

1. `mapWith(items, fn)` — array guard + `map` delegating `(item, index)` to `fn`.
2. `negate(predicate)` — returns `(...args) => Boolean(!predicate(...args))` (or equivalent boolean coercion of the negation).

## Constraints

- Do not edit tests.
- `negate` must not call `predicate` at creation time—only when the returned function is invoked.

## Step-by-step guidance

1. Implement the `Array.isArray` guard first.
2. Implement `negate` as a one-line wrapper if you like—readability matters more than cleverness.

## How to run and verify

### Install dependencies

```bash
cd "Day 25/practical-tasks/task-01-higher-order-callback-map"
npm install
```

### Run tests

```bash
npm test
```

### Manual checks

- [ ] `mapWith` returns a **new** array (do not mutate the input array in tests’ expectations).

## `TODO` map

| TODO | Done means |
|------|------------|
| `mapWith` | `Array.isArray` guard + `map` |
| `negate` | returns function inverting truthiness of predicate result via `Boolean` |

## Submission checklist (Git)

- [ ] `npm test` passes
- [ ] Only intentional files changed
