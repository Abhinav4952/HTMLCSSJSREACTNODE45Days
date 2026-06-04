# Evaluation Criteria — Day 36 — Task 4 — Three-slot layout

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | All three slots render correct content from `App.jsx`. |
| Layout | 25 | Uses `.layout` grid; semantic structure reasonable (`aside`/`section`/`aside`). |
| Code quality | 20 | No hard-coded slot content inside layout component. |

## Pass / fail gates

- Build fails.
- Slot props ignored.

## AI grading prompt

Verify `DashboardLayout.jsx` reads three props and renders them in distinct grid areas.
