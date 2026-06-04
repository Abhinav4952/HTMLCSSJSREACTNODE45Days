# Task 04 — Memoization with Stable Keys (Challenge)

## Summary

Memoize a pure “sum numeric fields” operation on plain objects using a **stable serialization** so `{a:1,b:2}` and `{b:2,a:1}` share a cache entry.

## Learning goals

- See why naive `JSON.stringify(cfg)` keys depend on insertion order.
- Track **cache misses** to prove reuse.

## Provided files

- `package.json`, `.npmrc`
- `src/memoChallenge.js`, `tests/memoChallenge.test.js`

## Prerequisites

- Day 25 theory on memoization and cache keys.

## What you will implement

1. `createCachedNumericSum()` returning `{ sum, misses }` per JSDoc in the source file.

## Constraints

- Do not edit tests.
- `misses()` must increment only on cache miss (first time a given stable key is computed).

## Step-by-step guidance

1. Build a stable string key from each config object (sorted keys stringify is enough here).
2. Store results in a `Map` keyed by that string.

## How to run and verify

### Install dependencies

```bash
cd "Day 25/practical-tasks/task-04-memoize-stable-keys-challenge"
npm install
```

### Run tests

```bash
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `createCachedNumericSum` | `sum` + stable cache + `misses` counter |

## Submission checklist (Git)

- [ ] `npm test` passes

## Hints (optional)

<details><summary>Stable key idea</summary>

`JSON.stringify(obj, Object.keys(obj).sort())` is enough for this task’s tests.

</details>
