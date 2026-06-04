# Task 4 — Blocking vs async file reads

## Summary

Implement the **same line-counting behavior** twice: once with **`readFileSync`** (blocking) and once with **`fs.promises.readFile`** (non-blocking). Reflect on when each is appropriate.

## Learning goals

- See how **sync** APIs are simpler but occupy the event loop for the entire disk read.
- Practice mirroring behavior between sync and async helpers.

## Provided files

| File | Purpose |
|------|---------|
| `src/lineCounter.js` | Implement both counting strategies. |
| `fixtures/three-lines.txt` | Three logical lines (file may end with newline). |

## What you will implement

1. `countLinesSync(absPath)` reads UTF-8 text synchronously and returns the number of lines. Treat `\n` as delimiter; trim trailing empty segments caused by a final newline so **`three-lines.txt` counts as 3**.
2. `countLinesAsync(absPath)` returns a `Promise` resolving to the **same** count for the same input.

## Constraints

- `countLinesSync` must use **`node:fs`** synchronous read APIs.
- `countLinesAsync` must use **`node:fs/promises`**.
- Only edit `TODO(Day41-task04)` markers.

## Manual checks (candidate self-review)

- [ ] In your own words, explain why `readFileSync` inside an Express request handler is risky under load.

## How to run and verify

```bash
cd "Day 41/practical-tasks/task-04-blocking-vs-async-file-read"
npm install
npm test
```

## `TODO` map

| Function | Done means |
|----------|-------------|
| `countLinesSync` | Matches Vitest expectation for fixture. |
| `countLinesAsync` | Matches sync helper for same path. |

## Submission checklist (Git)

- [ ] `npm test` passes.
