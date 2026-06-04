# Day 39 — Redux Core: Store, Actions, Reducers, and Immutability

## Learning objectives

- Explain the **single global store** mental model and when it helps vs local React state.
- Use **Redux Toolkit (`createSlice`)** to define **actions**, **reducers**, and **immutable updates** (via Immer under the hood).
- **Compose** multiple slices in `configureStore`.
- **Select** state in components with **`useSelector`** and dispatch with **`useDispatch`** (typed hooks optional beyond this course).

## Prerequisites

- **Days 34–38** (React components, state, composition, forms, keys).
- Solid **JavaScript objects/arrays** and **immutability habits** from Days 17–33.

## How to use this folder

1. Read `DAY-39-THEORY-AND-REFERENCE.md`.
2. Each task is a standalone **Vite + React + Redux Toolkit** app: from the task folder run `npm install`, then `npm run dev`. Use `npm run build` as an optional compile check.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-counter-slice-actions` | React + Redux | `npm install` → `npm run dev` (and `npm run build` where documented) |
| 2 | `task-02-theme-and-counter-combined` | React + Redux | `npm install` → `npm run dev` (and `npm run build` where documented) |
| 3 | `task-03-todo-list-redux` | React + Redux | `npm install` → `npm run dev` (and `npm run build` where documented) |
| 4 | `task-04-cart-selectors-total` | React + Redux | `npm install` → `npm run dev` (and `npm run build` where documented) |
