# Evaluation Criteria — Day 40 — Task 2 — Profile thunk

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | Successful fetch renders expected profile fields. |
| Rejection UX | 25 | Rejected path sets a useful `error` string. |
| Lifecycle | 20 | Pending + fulfilled handled. |

## Pass / fail gates

- Build fails.
- Successful fetch still leaves `user` null.

## AI grading prompt

Check `profileSlice.js` for thunk URL fix and `extraReducers` completeness.
