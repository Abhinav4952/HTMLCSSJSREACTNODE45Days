# Task 4 — Three-slot dashboard layout

## Summary

Implement **explicit slot props** (`leftAside`, `main`, `rightAside`) to compose a responsive **CSS grid** shell.

## Learning goals

- Use **element props** as composition slots (not only `children`).
- Keep layout markup centralized.

## What you will implement

1. `DashboardLayout` renders three columns: left aside, center section, right aside.
2. Each slot renders the React node passed from `App.jsx`.

## How to run and verify

```bash
cd "Day 36/practical-tasks/task-04-dashboard-three-slot-layout"
npm install
npm run dev
```

Optional: `npm run build`.

## Constraints

- Only edit files with `TODO(Day36-task04)`.

## Manual checks

- [ ] At wide widths, three columns appear left/center/right.
- [ ] At narrow widths, the CSS media query stacks rows (visual check).

## `TODO` map

| `DashboardLayout.jsx` | Done means |
|-----------------------|------------|
| Day36-task04 TODOs | Three props placed in grid regions with semantic tags suggested in TODO. |

## Submission checklist (Git)

- [ ] Build passes.
