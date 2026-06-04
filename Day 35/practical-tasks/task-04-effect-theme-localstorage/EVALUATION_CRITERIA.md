# Evaluation Criteria — Day 35 — Task 4 — Theme + localStorage

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 50 | Restore + persist works across reloads. |
| Effects discipline | 30 | No runaway re-render loops; sensible deps. |
| Robustness | 20 | Invalid stored values ignored. |

## Pass / fail gates

- Page freezes / max update depth exceeded.
- Build fails.

## Evidence

- Describe manual test: set dark → reload → still dark; corrupt key → resets safely.

## AI grading prompt

Review `ThemeShell.jsx` for storage read rules, persistence on theme changes, and dependency correctness.
