# Task 4 — Integration: post + comments in one thunk

## Summary

One **`fetchPostBundle`** thunk performs **two parallel fetches** (post + comments). Wire **`extraReducers`** so the UI can render the post body and a **comments count**.

## Learning goals

- Coordinate **multi-resource reads** behind a single user intent (load bundle).
- Keep error strings actionable when either fetch fails.

## Provided files

- `src/features/detail/detailSlice.js` — **edit surface** (`TODO(Day40-task04)`).
- `src/components/PostExplorer.jsx` — UI controls (read-only unless instructor allows).

## Constraints

- Only edit files with `TODO(Day40-task04)`.
- Requires network access to JSONPlaceholder.

## How to run and verify

```bash
cd "Day 40/practical-tasks/task-04-post-detail-integration"
npm install
npm run dev
```

### Manual checks

- [ ] Pick post id **3**, click **Load** → title/body render and **Comments loaded** is a positive integer.

## `TODO` map

| `detailSlice.js` | Done means |
|------------------|------------|
| `extraReducers` | Pending/fulfilled/rejected update `post`, `comments`, `status`, `error`. |

## Submission checklist (Git)

- [ ] `npm run build` passes.
