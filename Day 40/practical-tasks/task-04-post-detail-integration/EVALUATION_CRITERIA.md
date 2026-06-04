# Evaluation Criteria — Day 40 — Task 4 — Post detail integration

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | Post + comments populate; count matches loaded array length. |
| Async lifecycle | 35 | Pending + fulfilled + rejected handled cleanly. |
| Code quality | 10 | No redundant fetches introduced in reducers. |

## Pass / fail gates

- Build fails.
- `post` remains null after a successful fetch.

## AI grading prompt

Inspect `detailSlice.js` `extraReducers` for `fetchPostBundle` lifecycle and state fields used by `PostExplorer.jsx`.
