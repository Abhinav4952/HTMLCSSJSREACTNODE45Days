# Evaluation Criteria — Day 37 — Task 2 — Signup validate

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 50 | Validation rules match helper semantics; submit gating works. |
| UX / a11y | 25 | Errors visible; `role="alert"` used; labels wired. |
| Code quality | 25 | `useMemo` depends on field values; no redundant state for errors object if avoidable. |

## Pass / fail gates

- Submit enabled while errors exist.
- Build fails.

## AI grading prompt

Check `SignupForm.jsx` for controlled fields, `useMemo` validation, disabled submit logic, and submit handler.
