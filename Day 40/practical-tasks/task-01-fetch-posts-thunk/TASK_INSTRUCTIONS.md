# Task 1 — Fetch posts with `createAsyncThunk`

## Summary

Wire **`extraReducers`** for a **`fetchPosts`** thunk that reads a small list from **JSONPlaceholder**. The thunk itself is already implemented.

## Learning goals

- Handle **`pending` / `fulfilled` / `rejected`** for an async thunk.
- Keep **loading** and **error** UX explicit.

## Provided files

- `src/features/posts/postsSlice.js` — **edit surface** (`TODO(Day40-task01)`).
- `src/components/PostsList.jsx` — dispatches `fetchPosts` (read-only unless instructor allows).

## Constraints

- Only edit files with `TODO(Day40-task01)`.
- Requires network access to `jsonplaceholder.typicode.com` for manual verification.

## How to run and verify

```bash
cd "Day 40/practical-tasks/task-01-fetch-posts-thunk"
npm install
npm run dev
```

Optional:

```bash
npm run build
```

### Manual checks

- [ ] Clicking **Load posts** shows **Loading…** briefly, then 5 titles.
- [ ] If you simulate offline (DevTools), you should see a non-empty error path after rejection handling.

## `TODO` map

| `postsSlice.js` | Done means |
|-----------------|------------|
| `extraReducers` | Correct lifecycle handling for `fetchPosts`. |

## Submission checklist (Git)

- [ ] No secrets committed.
