# Evaluation Criteria — Day 41 — Task 1 — ESM path and URL basics

## Scope

Graders evaluate **`src/pathLab.js`** only. Tests are authoritative for behavior.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 50 | Both helpers match Vitest expectations on POSIX paths. |
| Requirements coverage | 30 | Uses `fileURLToPath` + `path.join` / `path.dirname` idioms. |
| Code quality | 20 | Small, readable functions; no `process.cwd()` shortcuts. |

## Pass / fail gates

- `npm test` does not pass.
- Uses hard-coded absolute paths copied from the grader machine.

## Detailed rubric

### Correctness

- `moduleDirname` returns the parent directory of the module file, not the file itself.
- `joinRelativeToModule` resolves `../fixtures/hello.txt` from `src/pathLab.js` correctly.

### Security / privacy

- No network calls; no secrets.

## Evidence the grader should collect

- Command: `npm test` (green output).

## AI grading prompt (paste into your grader)

You are evaluating a graduate-level Node ESM lab. Verify only `src/pathLab.js` changed (plus accidental formatting). Confirm `moduleDirname` and `joinRelativeToModule` use `fileURLToPath` and `path` APIs. Return Pass/Fail with blocking issues.
