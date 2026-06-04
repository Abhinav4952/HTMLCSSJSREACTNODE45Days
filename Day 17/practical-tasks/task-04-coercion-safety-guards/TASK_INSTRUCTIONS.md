# Task 04 — Coercion Safety Guards (Vitest)

## Summary

Implement **`toIntegerOrNull`** with explicit, test-locked conversion rules and a tiny **`stringifyForLog`** helper for safe debug strings.

## Learning goals

- Avoid accidental coercion by centralizing conversion rules.

## Provided files

- `package.json`, `.npmrc`
- `src/coercionLab.js`
- `tests/coercionLab.test.js`

## Prerequisites

- Day 17 theory: coercion preview.

## What you will implement

Complete every `// TODO(Day17-task04):` in `src/coercionLab.js`.

## Constraints

- Do not edit tests.

## How to run and verify

```bash
cd "Day 17/practical-tasks/task-04-coercion-safety-guards"
npm install
npm test
```

## `TODO` map

| Function | Done means |
|----------|------------|
| `toIntegerOrNull` | Matches coercion rules in test file |
| `stringifyForLog` | JSON for objects/arrays; `String` otherwise |

## Submission checklist (Git)

- [ ] `npm test` passes locally
- [ ] `package-lock.json` exists in this folder
