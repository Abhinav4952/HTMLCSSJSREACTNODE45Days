# Day 40 — Redux Side Effects & Integration (`createAsyncThunk`)

## Learning objectives

- Use **`createAsyncThunk`** for async workflows (network, timers) with **`pending` / `fulfilled` / `rejected`** lifecycle handling.
- Surface **loading** and **error** state in UI in a predictable way.
- Combine **multiple reads** (integration) into one cohesive feature slice.

## Prerequisites

- **Day 39** (store + slices + selectors).
- Basic **Promises** / `async`/`await` from Days 17–33.

## How to use this folder

1. Read `DAY-40-THEORY-AND-REFERENCE.md`.
2. Each task is a standalone **Vite + React + Redux Toolkit** app. Async uses **`createAsyncThunk`** (repo-wide standard for Days 39–40).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-fetch-posts-thunk` | React + Redux | `npm install` → `npm run dev` (and `npm run build` where documented) |
| 2 | `task-02-profile-thunk-rejection` | React + Redux | `npm install` → `npm run dev` (and `npm run build` where documented) |
| 3 | `task-03-delayed-submit-order-thunk` | React + Redux | `npm install` → `npm run dev` (and `npm run build` where documented) |
| 4 | `task-04-post-detail-integration` | React + Redux | `npm install` → `npm run dev` (and `npm run build` where documented) |
