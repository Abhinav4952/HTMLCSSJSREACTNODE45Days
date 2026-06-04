# Task 3 — Stable keys while editing

## Summary

Fix a **composite key** that incorrectly includes **`label`**, causing remounts as the user types.

## What you will implement

1. Use **`key={item.id}`** (stable) instead of a key that changes with `label`.

## How to run and verify

```bash
cd "Day 38/practical-tasks/task-03-keyed-inline-edit-rows"
npm install
npm run dev
```

## Constraints

- Only edit files with `TODO(Day38-task03)`.

## Manual checks

- [ ] Typing continuously in one field does not move focus to another row.

## `TODO` map

| `App.jsx` | Done means |
|-----------|------------|
| Day38-task03 TODOs | Stable keys + preserved controlled updates. |

## Submission checklist (Git)

- [ ] `npm run build` passes.
