# Task 2 — Fix reorder bugs caused by index keys

## Summary

This task ships a **known-bad** `key={index}` pattern alongside **controlled** row inputs and reorder buttons. You will **switch to stable keys** so row identity survives reordering.

## What you will implement

1. Replace `key={index}` with **`key={item.id}`** (or another stable field already on each item).
2. Keep the controlled inputs and reorder behavior working.

## How to run and verify

```bash
cd "Day 38/practical-tasks/task-02-reorder-keys-regression-fix"
npm install
npm run dev
```

## Constraints

- Only edit files with `TODO(Day38-task02)`.

## Manual checks

- [ ] Type different text into each row, then move rows up/down: each input should keep the text that belongs to that row’s **`id`** after the fix.

## `TODO` map

| `App.jsx` | Done means |
|-----------|------------|
| Day38-task02 TODO | Stable `key` usage. |

## Submission checklist (Git)

- [ ] `npm run build` passes.
