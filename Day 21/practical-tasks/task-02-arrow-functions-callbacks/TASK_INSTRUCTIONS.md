# Task 02 — Arrow Functions for Callbacks

## Summary

Practice **arrow functions** in `map` and as **returned functions** from a small higher-order helper.

## Learning goals

- Use concise arrow syntax for array transforms.
- Return an arrow function from `makeScaledAdder` with correct **finite number** validation.

## Provided files

- `package.json`, `.npmrc`
- `src/arrowLab.js`
- `tests/arrowLab.test.js`

## Prerequisites

- Day 21 theory on arrow functions.

## What you will implement

1. `sumPairs(pairs)` per file JSDoc; **`map` must use an arrow callback** (no `function` keyword inside the `map` call).
2. `makeScaledAdder(scale)` returns `(x) => …` validating `x` is a finite number.

## Constraints

- Do not edit tests.
- Keep the `map` callback syntactically an arrow function (graders may spot-check).

## Step-by-step guidance

1. Guard `pairs` with `Array.isArray`.
2. Normalize each side of a pair with a tiny helper or inline checks: finite number or `0`.
3. Return `(x) => …` from `makeScaledAdder`; validate `typeof x === "number" && Number.isFinite(x)`.

## How to run and verify

### Install dependencies

```bash
cd "Day 21/practical-tasks/task-02-arrow-functions-callbacks"
npm install
```

### Run tests

```bash
npm test
```

### Manual checks

- [ ] `map` callback is an arrow function in `sumPairs`.

## `TODO` map

| TODO | Done means |
|------|------------|
| `sumPairs` | Correct sums + `map` uses arrow callback |
| `makeScaledAdder` | Returns arrow adder with NaN rules |

## Submission checklist (Git)

- [ ] `npm test` passes
- [ ] No unrelated files changed

## Hints (optional)

<details><summary>Finite helper</summary>

```js
const asFinite = (v) =>
  typeof v === "number" && Number.isFinite(v) ? v : 0;
```

</details>
