# Evaluation Criteria — Day 06 — Task 02 — Fluid Type & Viewport Units

## Scope

Graded: `styles/main.css` fluid system; `index.html` unchanged unless instructor modified.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 45 | Valid CSS; readable minima; uses clamp + vw as required |
| Requirements coverage | 30 | TODO map satisfied |
| Code quality | 15 | Variables coherent; comments explain slope |
| UX / a11y | 10 | No microscopic body text at 320px |

## Pass / fail gates

- Body computed font-size under 15px at 320px viewport width.
- No `clamp()` used for the step variables (task requirement).

## AI grading prompt

Verify CSS variables --step-* use clamp with vw in preferred, article padding uses clamp, pullquote uses vw term, and responsive readability rationale is visible in comments if present.
