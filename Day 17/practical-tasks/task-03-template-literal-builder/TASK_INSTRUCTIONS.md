# Task 03 — Template Literal Builder (Vitest)

## Summary

Build a **`formatIssue`** string using **template literals** with exact newline formatting locked by tests.

## Learning goals

- Interpolate values into readable multi-line strings without manual `+` concatenation.

## Provided files

- `package.json`, `.npmrc`
- `src/templatesLab.js`
- `tests/templatesLab.test.js`

## Prerequisites

- Day 17 theory: template literals.

## What you will implement

Implement `formatIssue(issue)` exactly as:

```txt
ISSUE <id>: <title>
Severity: <SEVERITY UPPERCASED>
Link: <url>

```

Notes:

- The output must end with a **trailing newline** after the `Link:` line (i.e., a blank third line is acceptable—match tests exactly).
- `issue.severity` must be uppercased via `String.prototype.toUpperCase()`.

## Constraints

- Do not edit tests.

## How to run and verify

```bash
cd "Day 17/practical-tasks/task-03-template-literal-builder"
npm install
npm test
```

## `TODO` map

| Location | Done means |
|----------|------------|
| `formatIssue` | Exact formatting + uppercase severity |

## Submission checklist (Git)

- [ ] `npm test` passes locally
- [ ] `package-lock.json` exists in this folder
