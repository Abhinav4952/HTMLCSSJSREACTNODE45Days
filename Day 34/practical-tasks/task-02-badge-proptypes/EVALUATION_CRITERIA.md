# Evaluation Criteria — Day 34 — Task 2 — Badge + PropTypes

## Scope

Graded: `src/components/Badge.jsx` (rendering + `prop-types`).  
Out of scope: changing global CSS tokens beyond minor tweaks (avoid unless needed).

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 45 | Variants map to correct `badge--*` classes; label/icon rules satisfied. |
| Prop contracts | 25 | `prop-types` definitions match the stated API; no nonsense types. |
| Code quality | 20 | No prop mutation; readable `className` construction. |
| Requirements coverage | 10 | Matches all `App.jsx` usages without further edits to `App.jsx`. |

## Pass / fail gates

- `npm run build` fails after candidate work.
- `Badge.propTypes` missing or clearly unrelated to the component API.
- `variant` values outside the three allowed strings render without a sensible defaulting strategy (should default to `info`).

## Detailed rubric

### Correctness

- **Full credit:** All three variants visibly distinct using provided CSS; icon only when provided; default variant behavior works if `variant` omitted (the third badge).
- **Partial:** Styling works but PropTypes incomplete or icon spacing slightly off.
- **No credit:** Hard-coded badge list ignoring props.

### Evidence

- Screenshot of the three badges.
- Console screenshot optional if demonstrating PropTypes warning on a deliberate scratch test.

## AI grading prompt (paste into your grader)

Evaluate `Badge.jsx` only. Check: class list includes `badge` + `badge--variant`, label rendered, optional icon with `aria-hidden`, and `Badge.propTypes` correctness. Return Pass/Fail + brief rationale.
