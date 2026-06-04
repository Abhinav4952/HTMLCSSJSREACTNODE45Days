# Task 3 — Async `fs` + JSON parsing

## Summary

Read a UTF-8 JSON file with **`fs.promises`**, validate that the top-level value is an **array**, and return a small summary object.

## Learning goals

- Use **`await fs.readFile(path, 'utf8')`** safely.
- Translate filesystem errors and **invalid JSON** into actionable failures.

## Provided files

| File | Purpose |
|------|---------|
| `src/jsonSummary.js` | Implement `summarizeJsonArrayFile`. |
| `fixtures/items.json` | Valid array payload. |
| `fixtures/object.json` | Invalid shape for negative test. |

## What you will implement

1. Read `absPath` as UTF-8 text asynchronously.
2. `JSON.parse` the text.
3. If the parsed value is **not** an array, throw an `Error` whose message includes the word `array` (lowercase) so tests can match politely.
4. Return `{ count, titles }` where `titles` maps each element’s `title` field (assume present for valid files).

## Constraints

- Use **`node:fs/promises`** only (no sync reads).
- Only edit `TODO(Day41-task03)` sections.

## How to run and verify

```bash
cd "Day 41/practical-tasks/task-03-async-fs-json-summary"
npm install
npm test
```

## `TODO` map

| Location | Done means |
|----------|-------------|
| `summarizeJsonArrayFile` | Passes both Vitest cases. |

## Submission checklist (Git)

- [ ] `npm test` passes.
