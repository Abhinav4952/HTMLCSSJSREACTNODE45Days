# Evaluation Criteria — Day 41 — Task 4 — Blocking vs async reads

## Scope

`src/lineCounter.js` only.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 45 | Both helpers return 3 for provided fixture. |
| API choice | 35 | Sync path uses `readFileSync`; async path uses `fs.promises`. |
| Understanding | 20 | Candidate explanation (manual checklist) distinguishes server risk. |

## Pass / fail gates

- `npm test` fails.
- Async helper uses sync read internally.

## Evidence the grader should collect

- `npm test` output.
- Candidate notes answering the manual self-review question (README snippet, PR description, or instructor template).

## AI grading prompt

Verify implementations: sync uses `node:fs` sync read; async uses `node:fs/promises`; identical counts for fixture. Mention blocking risk in feedback if manual note missing.
