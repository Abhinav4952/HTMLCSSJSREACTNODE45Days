# Task 03 — Currying Binary Operations

## Summary

Implement **`curryBinary`** and build **`makeClamp(lo)(hi)(value)`** using nested unary functions.

## Learning goals

- Practice curried call shapes without libraries.

## Provided files

- `package.json`, `.npmrc`
- `src/curryLab.js`, `tests/curryLab.test.js`

## Prerequisites

- Day 25 theory on currying.

## What you will implement

1. `curryBinary(fn)` returning `(a) => (b) => fn(a, b)`.
2. `makeClamp(lo)(hi)(value)` clamping `value` between `lo` and `hi`.

## Constraints

- Do not edit tests.

## Step-by-step guidance

1. Implement `curryBinary` first and sanity-check with addition.
2. Implement `makeClamp` as nested unary functions; use `Math.min` / `Math.max`.

## How to run and verify

### Install dependencies

```bash
cd "Day 25/practical-tasks/task-03-curry-binary-operations"
npm install
```

### Run tests

```bash
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `curryBinary` | Returns unary waiting for second arg |
| `makeClamp` | `makeClamp(lo)(hi)(value)` clamps |

## Submission checklist (Git)

- [ ] `npm test` passes
