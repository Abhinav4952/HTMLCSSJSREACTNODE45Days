# Task 2 — Fix failing profile fetch + rejection UX

## Summary

The starter thunk intentionally requests a **non-existent JSONPlaceholder user id (`0`)**, which **404**s. Fix the URL to load **user 1**, and implement **`extraReducers`** so the UI can show **loading**, **errors**, and the **loaded profile**.

## Learning goals

- Read **`rejectWithValue`** payloads in reducers.
- Practice debugging **HTTP errors** as first-class UI states.

## Provided files

- `src/features/profile/profileSlice.js` — **edit surface** (`TODO(Day40-task02)`).
- `src/components/ProfilePanel.jsx` — UI (read-only unless instructor allows).

## Constraints

- Only edit files with `TODO(Day40-task02)`.

## How to run and verify

```bash
cd "Day 40/practical-tasks/task-02-profile-thunk-rejection"
npm install
npm run dev
```

### Manual checks

- [ ] After your fix, **Load profile** shows **Leanne Graham** (name) and a real email string from JSONPlaceholder.

## `TODO` map

| `profileSlice.js` | Done means |
|-------------------|------------|
| Thunk URL TODO | Uses a valid user endpoint (id **1**). |
| `extraReducers` TODO | Pending/fulfilled/rejected handled. |

## Submission checklist (Git)

- [ ] `npm run build` passes.
