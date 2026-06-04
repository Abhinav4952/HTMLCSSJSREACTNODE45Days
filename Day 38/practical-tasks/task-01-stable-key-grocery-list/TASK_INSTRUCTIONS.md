# Task 1 — Grocery list with stable keys

## Summary

Practice **adding list rows** while always using a **stable `id` key** (`createItem` helper provided).

## What you will implement

1. Controlled draft input + **Add** button (`type="button"`).
2. Append new items with `createItem` and render with **`key={item.id}`** (already correct—keep it).

## How to run and verify

```bash
cd "Day 38/practical-tasks/task-01-stable-key-grocery-list"
npm install
npm run dev
```

## Constraints

- Only edit files with `TODO(Day38-task01)`.

## Manual checks

- [ ] Add several items; DevTools shows each `<li>` key tied to a stable id string.

## `TODO` map

| `App.jsx` | Done means |
|-----------|------------|
| Day38-task01 TODOs | Controlled draft + append behavior. |

## Submission checklist (Git)

- [ ] `npm run build` passes.
