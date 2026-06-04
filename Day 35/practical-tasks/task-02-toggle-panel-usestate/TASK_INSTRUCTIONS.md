# Task 2 — Disclosure panel with `useState`

## Summary

Build a small **expand/collapse** panel driven by local boolean state. This pattern shows up everywhere: FAQs, advanced filters, debug drawers.

## Learning goals

- Toggle boolean state on click.
- **Conditionally render** a subtree (not merely `display: none`—omit the node when closed per instructions).

## Provided files

- `src/components/DisclosurePanel.jsx` — edit surface.
- `src/App.jsx` — supplies `title` and `children`.

## What you will implement

1. Panel starts **collapsed** (content hidden).
2. Button toggles open/closed with **`type="button"`**.
3. Button label reflects state (e.g. **Show** / **Hide**).
4. When collapsed, **do not render** the `<div className="panel__body">` at all.

## How to run and verify

```bash
cd "Day 35/practical-tasks/task-02-toggle-panel-usestate"
npm install
npm run dev
```

Optional: `npm run build`.

### Manual checks

- [ ] Fresh load: body absent in Elements tree.
- [ ] Open: children visible; button label updates.
- [ ] Close: body removed again (not `hidden` attribute only—check instructions).

## `TODO` map

| `DisclosurePanel.jsx` | Done means |
|-----------------------|------------|
| All Day35-task02 TODO lines | State + conditional children + button label rules satisfied. |

## Submission checklist (Git)

- [ ] Only TODO-marked files changed.
