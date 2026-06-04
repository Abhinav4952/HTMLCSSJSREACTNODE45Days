# Evaluation Criteria — Day 34 — Task 3 — Class welcome banner

## Scope

Graded: `src/components/WelcomeBanner.jsx`.  
Out of scope: redesigning `App.jsx` props.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 50 | Title always shown; subtitle conditional logic correct. |
| Class usage | 20 | Proper `Component` subclass; uses `this.props`. |
| Code quality | 20 | No prop mutation; clean conditional rendering. |
| Requirements coverage | 10 | Works for both `App.jsx` instances without further edits. |

## Pass / fail gates

- Converts `WelcomeBanner` to a function component against instructions (unless instructor override).
- `npm run build` fails after changes.

## Evidence

- Screenshot or Elements panel snippet showing no empty `<p>` for the second banner.

## AI grading prompt (paste into your grader)

Verify class-based `WelcomeBanner`, `this.props` usage, conditional subtitle rendering, and build success. Return Pass/Fail + notes.
