# Task 4 — Dashboard: function + class components

## Summary

You will finish a tiny **dashboard** layout: two **`MetricCard`** function components and one **`TeamNote`** class component, then wrap them in a **CSS grid** container in `App.jsx`.

## Learning goals

- Mix **function** and **class** components in one screen.
- Practice **prop-driven** rendering for numbers and text.
- Apply provided layout classes (`grid`, `metric`, `note`).

## Provided files

- `src/App.jsx` — contains a JSX comment `TODO` for wrapping layout.
- `src/components/MetricCard.jsx` — function component starter.
- `src/components/TeamNote.jsx` — class component starter.
- `src/index.css` — layout + card styles.

## Prerequisites

- Tasks 1–3.

## What you will implement

1. `MetricCard` renders **`title`** as `<h2>` and **`value`** as `<p>` inside `<article className="metric">`.
2. `TeamNote` renders **`author`** as `<h3>` and **`body`** as `<p>` inside `<article className="note">`.
3. In `App.jsx`, wrap the three components in **`<div className="grid">...</div>`** so the grid CSS applies.

## Constraints

- Only edit files with `TODO(Day34-task04)`.

## How to run and verify

```bash
cd "Day 34/practical-tasks/task-04-dashboard-cards-mixed"
npm install
npm run dev
```

Optional:

```bash
npm run build
```

### Manual checks

- [ ] Both metric cards show the titles and values passed from `App.jsx`.
- [ ] Team note shows Sam’s message.
- [ ] Layout: cards appear in a responsive grid (resize the window).

## `TODO` map

| File | Done means |
|------|------------|
| `MetricCard.jsx` | Uses props for title/value. |
| `TeamNote.jsx` | Uses `this.props` for author/body. |
| `App.jsx` | Adds `div.grid` wrapper around the three components. |

## Submission checklist (Git)

- [ ] `npm run build` succeeds.
