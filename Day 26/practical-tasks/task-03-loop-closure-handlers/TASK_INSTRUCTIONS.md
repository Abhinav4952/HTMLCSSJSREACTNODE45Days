# Task 03 — Loop + Closure Handlers

## Summary

Build `count` callbacks that each return their **own** index—practice avoiding the classic loop capture bug.

## Learning goals

- Use **`let`** (or another correct per-iteration binding strategy) so each handler closes over a distinct index.

## Provided files

- `package.json`, `.npmrc`
- `src/loopClosureHandlers.js`, `tests/loopClosureHandlers.test.js`

## Prerequisites

- Day 26 theory on loop closures.

## What you will implement

1. `createIndexHandlers(count)` per JSDoc.

## Constraints

- Do not edit tests.

## How to run and verify

```bash
cd "Day 26/practical-tasks/task-03-loop-closure-handlers"
npm install
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `createIndexHandlers` | Correct per-index closures |

## Submission checklist (Git)

- [ ] `npm test` passes
