# Task 04 — Module Pattern Budget (Challenge)

## Summary

Implement a **budget** object with **private balance** and careful **withdraw** semantics.

## Learning goals

- Model a tiny “module” surface: only exported methods touch internal state.

## Provided files

- `package.json`, `.npmrc`
- `src/budgetModule.js`, `tests/budgetModule.test.js`

## Prerequisites

- Day 26 theory on module pattern + closures.

## What you will implement

1. `createBudget(startingBalance)` per JSDoc.

## Constraints

- Do not edit tests.
- Balance must not be a public property on the returned object.

## How to run and verify

```bash
cd "Day 26/practical-tasks/task-04-module-pattern-budget-challenge"
npm install
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `createBudget` | Private balance + deposit/withdraw rules |

## Submission checklist (Git)

- [ ] `npm test` passes
