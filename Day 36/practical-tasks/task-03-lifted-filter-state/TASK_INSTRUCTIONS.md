# Task 3 — Lifted filter state

## Summary

Practice **lifting state** to `App`: the search string lives in the parent while **`SearchField`** and **`ProductList`** are controlled/coordinated by props.

## Learning goals

- Keep query string state in a common ancestor.
- Build a **controlled input** component.
- Derive filtered lists from props (no duplicate sources of truth).

## Provided files

- `src/App.jsx` — owns `useState` (partially wired).
- `src/components/SearchField.jsx` — controlled input TODO.
- `src/components/ProductList.jsx` — filtering + list TODO.
- `src/data/products.js` — static data (read-only).

## What you will implement

1. Typing in the search box updates **`query`** in `App` (replace the no-op `onChange` passed to `SearchField`).
2. `SearchField` renders a controlled `<input type="search">`.
3. `ProductList` shows **all** products when `query` is empty; otherwise filters by **case-insensitive substring** of `name`.

## Constraints

- Only edit files with `TODO(Day36-task03)`.

## How to run and verify

```bash
cd "Day 36/practical-tasks/task-03-lifted-filter-state"
npm install
npm run dev
```

Optional: `npm run build`.

### Manual checks

- [ ] Typing `pen` shows **Mechanical pencil** only.
- [ ] Clearing the input restores all four items.

## `TODO` map

| File | Done means |
|------|------------|
| `App.jsx` | `SearchField` receives working `onChange` wiring to `setQuery`. |
| `SearchField.jsx` | Controlled input updates parent. |
| `ProductList.jsx` | Filter + `<ul>` list with stable `key`. |

## Submission checklist (Git)

- [ ] Build passes.
