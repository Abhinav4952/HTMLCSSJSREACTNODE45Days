# Evaluation Criteria — Day 35 — Task 2 — Toggle panel

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 45 | Toggle works; body omitted when closed. |
| UX clarity | 25 | Button label communicates next/ current state clearly. |
| Code quality | 20 | `useState`; `type="button"`; readable JSX. |
| Requirements | 10 | Honors “no empty panel body” rule. |

## Pass / fail gates

- Panel body still present in DOM when “closed” (e.g. empty div remains).
- Build fails.

## AI grading prompt

Inspect `DisclosurePanel.jsx` for conditional rendering pattern and button labeling.
