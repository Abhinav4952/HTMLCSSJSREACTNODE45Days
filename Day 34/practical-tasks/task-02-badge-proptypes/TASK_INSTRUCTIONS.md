# Task 2 — Badge styling + PropTypes

## Summary

Implement a reusable **`Badge`** function component that reflects **`variant`** styling, supports an optional **`icon`**, and documents its contract with **`prop-types`**. The CSS for `badge--info|warn|success` is already provided in `src/index.css`.

## Learning goals

- Use **`prop-types`** for development-time validation.
- Map a discrete **`variant`** prop to CSS class names safely.
- Keep decorative icons accessible (`aria-hidden` on the icon span).

## Provided files

- `src/components/Badge.jsx` — primary edit surface.
- `src/index.css` — prewritten variant styles.
- `src/App.jsx` — example usage (reference).

## Prerequisites

- Task 1 and Day 34 theory sections on PropTypes.

## What you will implement

1. `Badge` accepts `label` (string), `variant` (`'info' | 'warn' | 'success'`, default **`info`**), and optional `icon` (string, e.g. an emoji).
2. Rendered element is a `<span>` with classes: **`badge`** and **`badge--<variant>`**.
3. If `icon` exists, render `<span className="badge__icon" aria-hidden>...</span>` before the label text.
4. Define **`Badge.propTypes`** matching the above (label required; variant oneOf; icon optional string).

## Constraints

- Edit only files with `TODO(Day34-task02)` unless instructor allows more.
- No Redux/Router/UI kits.

## Step-by-step guidance

1. Add destructured parameters to `Badge` including a default for `variant`.
2. Build the `className` string (template literal or array `.filter` join—your choice).
3. Implement conditional icon markup.
4. Add `Badge.propTypes` using `PropTypes` imports already in the file.
5. Run dev build; open the console—intentionally pass a wrong prop in a scratch change (then revert) to see PropTypes warnings.

## How to run and verify

### Install dependencies

From the repository root:

```bash
cd "Day 34/practical-tasks/task-02-badge-proptypes"
npm install
```

### Run the app

```bash
npm run dev
```

### Optional bundle check

```bash
npm run build
```

### Manual checks

- [ ] Three badges in `App.jsx` visually differ (success green-ish, warn yellow-ish, info blue-ish).
- [ ] The first badge shows the **✓** icon before the label.
- [ ] The second badge has **no** empty icon spacing artifact (no stray blank icon region).
- [ ] `npm run build` succeeds.

## `TODO` map

| Location | Done means |
|----------|------------|
| `Badge.jsx` function body | Correct classes, label text, optional icon. |
| `Badge.jsx` bottom | Complete `Badge.propTypes`. |

## Submission checklist (Git)

- [ ] Only intentional files changed.
- [ ] No `node_modules` committed.
