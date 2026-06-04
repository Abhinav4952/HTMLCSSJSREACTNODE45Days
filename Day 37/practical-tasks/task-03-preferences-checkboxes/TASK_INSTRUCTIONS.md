# Task 3 — Checkbox preferences

## Summary

Control multiple **checkboxes** from one piece of React state and reflect the combined choices in a **live summary** line.

## What you will implement

1. Immutable toggles for three booleans (`email`, `sms`, `weeklyDigest`).
2. Summary lists which channels are enabled (omit disabled ones).

## How to run and verify

```bash
cd "Day 37/practical-tasks/task-03-preferences-checkboxes"
npm install
npm run dev
```

## Constraints

- Only edit files with `TODO(Day37-task03)`.

## Manual checks

- [ ] Toggling any checkbox updates the summary `<div className="summary">` within the same render cycle.

## `TODO` map

| `PreferencesForm.jsx` | Done means |
|-----------------------|------------|
| Day37-task03 TODOs | Handlers + summary string. |

## Submission checklist (Git)

- [ ] `npm run build` passes.
