# Evaluation Criteria — Day 41 — Task 3 — Async FS JSON summary

## Scope

`src/jsonSummary.js` implementation; tests are provided.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | Happy path summary; rejects non-array JSON. |
| Error handling | 25 | Meaningful errors for bad JSON / shape. |
| Async style | 20 | Uses `fs.promises`; no blocking reads. |

## Pass / fail gates

- `npm test` fails.
- Uses `readFileSync`.

## Evidence

- `npm test` green.

## AI grading prompt

Verify `summarizeJsonArrayFile` uses async FS, validates array JSON, maps `title` fields, and throws on invalid top-level shape with `array` in message.
