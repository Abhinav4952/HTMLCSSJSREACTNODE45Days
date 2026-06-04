# Task 04 — Coercion Safety Kit (Challenge)

## Summary

Parse a bounded **percent string** into a numeric fraction, then **merge numeric maps** without accidental string concatenation.

## Learning goals

- Validate strings before `Number(...)` coercion.
- When merging tallies, treat non-numbers as missing.

## Provided files

- `src/coercionSafetyKit.js`, `tests/coercionSafetyKit.test.js`

## What you will implement

1. `parsePercentToFraction(input)` per JSDoc (trim, single `%` suffix, finite number).
2. `mergeCountObjects(left, right)` summing finite numeric values per key.

## Constraints

- Do not edit tests.

## How to run and verify

```bash
cd "Day 23/practical-tasks/task-04-coercion-safety-kit-challenge"
npm install
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `parsePercentToFraction` | Regex or manual parse + validation |
| `mergeCountObjects` | Immutable merge with numeric filtering |

## Submission checklist (Git)

- [ ] `npm test` passes

## Hints (optional)

<details><summary>Regex sketch</summary>

Trim then match `^-?\d+(\.\d+)?%$` (adjust to reject extras carefully).

</details>
