# Task 04 — Strict `this` Footgun (Challenge)

## Summary

Observe **strict-mode** `this` for standalone calls, then **bind** an extracted method so `this` stays correct.

## Learning goals

- Connect “lost `this`” bugs to calling conventions.
- Use `bind` as a targeted fix.

## Provided files

- `src/strictThisChallenge.js`, `tests/strictThisChallenge.test.js`

## How to run and verify

```bash
cd "Day 24/practical-tasks/task-04-strict-this-footgun-challenge"
npm install
npm test
```

## `TODO` map

| TODO | Done means |
|------|------------|
| `strictStandaloneThisType` | `'use strict'` + IIFE returning `typeof this` |
| `bindGetter` | `getter.bind(host)` |

## Submission checklist (Git)

- [ ] `npm test` passes
