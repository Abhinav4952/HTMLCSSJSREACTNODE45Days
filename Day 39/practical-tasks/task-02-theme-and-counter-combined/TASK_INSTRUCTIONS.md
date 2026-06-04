# Task 2 — Theme slice + counter slice in one store

## Summary

The **`counter`** slice is already implemented. Implement **`toggleMode`** in the **`theme`** slice and verify the UI chrome flips between **light** and **dark** modes.

## Learning goals

- Register **multiple reducers** in `configureStore`.
- Keep slice responsibilities separated (theme vs counter).

## Provided files

- `src/features/theme/themeSlice.js` — **edit surface** (`TODO(Day39-task02)`).
- `src/app/store.js` — already combines `counter` + `theme`.
- `src/components/ThemeToggle.jsx` — dispatches `toggleMode`.

## Prerequisites

- Task 1 and Day 39 theory on `configureStore`.

## What you will implement

1. `toggleMode` switches `mode` between **`'light'`** and **`'dark'`** only.

## Constraints

- Only edit files with `TODO(Day39-task02)`.

## How to run and verify

```bash
cd "Day 39/practical-tasks/task-02-theme-and-counter-combined"
npm install
npm run dev
```

Optional:

```bash
npm run build
```

### Manual checks

- [ ] The page background/text contrast visibly changes when toggling.
- [ ] Counter buttons still work after toggling themes.

## `TODO` map

| `themeSlice.js` | Done means |
|-----------------|------------|
| `toggleMode` | Flips between the two allowed string modes. |

## Submission checklist (Git)

- [ ] No secrets committed.
