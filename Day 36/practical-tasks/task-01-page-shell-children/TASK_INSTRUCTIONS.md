# Task 1 — `PageShell` with `children`

## Summary

Implement a reusable **page shell** that renders a **title** and places nested JSX into the **`<main>`** region via **`children`**.

## Learning goals

- Use the **`children`** prop.
- Keep layout concerns (header/footer chrome) separate from page content.

## Provided files

- `src/components/PageShell.jsx` — edit surface.
- `src/App.jsx` — passes children content.

## Prerequisites

- Day 36 theory: composition section.

## What you will implement

1. `PageShell` accepts **`title`** and **`children`**.
2. Header shows the title in `<h1>`.
3. Main shows **`children`** (remove the placeholder paragraph).

## Constraints

- Only edit files with `TODO(Day36-task01)`.

## How to run and verify

```bash
cd "Day 36/practical-tasks/task-01-page-shell-children"
npm install
npm run dev
```

Optional: `npm run build`.

### Manual checks

- [ ] Both paragraphs from `App.jsx` appear inside `<main>` in DevTools.

## `TODO` map

| `PageShell.jsx` | Done means |
|-----------------|------------|
| All Day36-task01 TODO lines | Title + children wired correctly. |

## Submission checklist (Git)

- [ ] Build passes.
