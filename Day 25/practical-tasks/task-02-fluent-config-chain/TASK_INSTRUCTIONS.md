# Task 02 — Fluent Config Chain

## Summary

Implement a **method-chaining** builder that returns SQL-ish strings (toy DSL).

## Learning goals

- Return `this` from mutating methods to enable fluent style.

## Provided files

- `package.json`, `.npmrc`
- `src/fluentChainLab.js`, `tests/fluentChainLab.test.js`

## Prerequisites

- Day 25 theory on method chaining.

## What you will implement

1. A builder object with `select`, `from`, and `build` methods as described in `src/fluentChainLab.js`.

## Constraints

- Do not edit tests.
- `select` / `from` must return `this` to support chaining.

## Step-by-step guidance

1. Store the last valid `fields` and `table` on the builder instance.
2. `build()` formats `SELECT … FROM …` or returns `""` if incomplete.

## How to run and verify

### Install dependencies

```bash
cd "Day 25/practical-tasks/task-02-fluent-config-chain"
npm install
```

### Run tests

```bash
npm test
```

### Manual checks

- [ ] Chaining works for at least three calls as in the test file.

## `TODO` map

| TODO | Done means |
|------|------------|
| `createQueryBuilder` | `select`/`from`/`build` behavior per JSDoc |

## Submission checklist (Git)

- [ ] `npm test` passes
