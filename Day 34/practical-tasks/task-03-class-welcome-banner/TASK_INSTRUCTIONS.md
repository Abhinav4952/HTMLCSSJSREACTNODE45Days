# Task 3 — Class `WelcomeBanner`

## Summary

Implement a **`WelcomeBanner`** as a **class component** that reads **`title`** and an optional **`subtitle`** from `this.props`. This mirrors patterns still common in legacy React code and previews lifecycle discussions on Day 35.

## Learning goals

- Author `render()` returning JSX.
- Read props via **`this.props`** without mutation.
- Conditionally render the subtitle only when it is provided and non-empty.

## Provided files

- `src/components/WelcomeBanner.jsx` — edit surface.
- `src/App.jsx` — two usage examples.

## Prerequisites

- Day 34 theory: class components section.

## What you will implement

1. `<h1>` shows the **`title`** prop.
2. If **`subtitle`** is a non-empty string, render it beneath the title in a `<p>`.
3. If **`subtitle`** is missing/empty, **do not** render an empty paragraph node.

## Constraints

- Keep `WelcomeBanner` as a **class** extending `React.Component` (or `Component` import).
- Only edit files containing `TODO(Day34-task03)` unless your instructor allows more.

## Step-by-step guidance

1. Destructure `this.props` inside `render` (optional) or read fields directly.
2. Guard subtitle rendering: e.g. only render `<p>` when `subtitle` is truthy.
3. Verify both banners in `App.jsx` match expectations.

## How to run and verify

From the repository root:

```bash
cd "Day 34/practical-tasks/task-03-class-welcome-banner"
npm install
npm run dev
```

Optional:

```bash
npm run build
```

### Manual checks

- [ ] First banner shows title + subtitle.
- [ ] Second banner shows title only (no blank subtitle paragraph spacing from an empty `<p>`—visual check in DevTools Elements tree).

## `TODO` map

| Location | Done means |
|----------|------------|
| `WelcomeBanner.jsx` `render` | Reads props; conditional subtitle; semantic header markup preserved. |

## Submission checklist (Git)

- [ ] No prop mutation.
- [ ] Dev server runs cleanly.
