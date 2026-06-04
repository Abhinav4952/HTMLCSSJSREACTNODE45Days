# Evaluation Criteria — Day 40 — Task 3 — Submit order thunk

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 60 | Confirmation appears after fulfilled; reset works. |
| Lifecycle | 30 | Pending + fulfilled (+ rejected optional but recommended). |
| Code quality | 10 | Clear state transitions. |

## Pass / fail gates

- Build fails.
- No confirmation after successful submit.

## AI grading prompt

Evaluate `orderSlice.js` thunk handling and compatibility with `CheckoutPanel.jsx` status checks.
