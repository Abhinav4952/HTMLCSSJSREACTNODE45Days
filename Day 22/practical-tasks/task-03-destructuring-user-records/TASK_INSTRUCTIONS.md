# Task 03 — Destructuring User Records

## Summary

Use **parameter object destructuring** with defaults and a small **array destructuring** parse.

## Learning goals

- Defaults in destructuring patterns (`role = "viewer"`).
- Rename fields logically (`email` → `primaryEmail`).

## Provided files

- `src/destructureLab.js`, `tests/destructureLab.test.js`

## Prerequisites

- Day 22 theory on destructuring.

## What you will implement

1. `normalizeProfile(profile)` using destructuring in the **function parameter**.
2. `parsePair(pairString)` using array destructuring on `split`.

## Constraints

- Do not edit tests.
- `normalizeProfile` must destructure fields **in its parameter list** (e.g. `function normalizeProfile({ email, ... } = {}) { ... }`). Callers in tests always pass a plain object; you do not need to accept `null` without throwing unless you choose to add an extra guard (not required by tests).

## How to run and verify

```bash
cd "Day 22/practical-tasks/task-03-destructuring-user-records"
npm install
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `normalizeProfile` | Destructuring defaults + rename + validation |
| `parsePair` | Array destructuring on `split` |

## Submission checklist (Git)

- [ ] `npm test` passes
