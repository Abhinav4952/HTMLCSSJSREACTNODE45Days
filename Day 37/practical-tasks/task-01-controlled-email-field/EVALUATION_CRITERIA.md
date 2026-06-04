# Evaluation Criteria — Day 37 — Task 1 — Controlled email

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | Controlled field updates hint live. |
| Forms hygiene | 25 | `label` associated via `htmlFor`/`id`; `type="email"`. |
| Code quality | 20 | `useState` + clean handler. |

## Pass / fail gates

- Build fails.
- Input not controlled (no `value` binding).

## AI grading prompt

Verify `EmailField.jsx` uses `useState` and controlled input pattern.
