# Evaluation Criteria — Day 40 — Task 1 — Fetch posts thunk

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 60 | Items populate; status/error fields behave sensibly. |
| Thunk lifecycle | 30 | Handles pending + fulfilled + rejected. |
| Code quality | 10 | Uses `builder.addCase` (or equivalent) clearly. |

## Pass / fail gates

- `npm run build` fails.
- Successful fetch still leaves `items` empty.

## AI grading prompt

Review `postsSlice.js` `extraReducers` for `fetchPosts` lifecycle coverage.
