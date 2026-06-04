# Evaluation Criteria — Day 12 — Task 04 — Constraint Validation UX Patterns

## Scope

Graded: `index.html` copy + `styles/main.css` UX states.  
Out of scope: server-side validation.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 45 | Help text matches constraints; CSS states work in stated demo browser |
| Requirements coverage | 35 | TODOs completed; no JS added |
| UX / accessibility | 20 | `aria-describedby` preserved; focus-visible |

## Pass / fail gates

- Any `TODO(Day12-task04)` remaining.
- Removing `aria-describedby`.

## Evidence the grader should collect

- Name the browser used to verify `:user-invalid` behavior + 2 screenshots (invalid + valid).

## AI-assisted grading prompt (optional)

```markdown
## AI grading prompt (paste into your grader)
You are evaluating a graduate-level assignment. Use only observable criteria below.
Repository context: `Day 12/practical-tasks/task-04-constraint-validation-ux-patterns`.
Rubric: confirm TODOs removed; confirm help text matches regex; confirm error message exists; confirm CSS uses `:user-invalid` strategy with documented fallback comment; confirm focus-visible styles exist.
Return: Pass/Fail, score table, blocking issues, non-blocking suggestions.
```
