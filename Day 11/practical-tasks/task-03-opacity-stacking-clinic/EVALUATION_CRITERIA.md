# Evaluation Criteria — Day 11 — Task 03 — Opacity Stacking Clinic

## Scope

Graded: completed `TODO(Day11-task03)` markers in `index.html` and `styles/main.css`.  
Out of scope: JavaScript, frameworks.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 45 | Observable opacity-vs-alpha distinction |
| Requirements coverage | 35 | All TODOs complete; constraints respected |
| UX / accessibility | 20 | Text remains readable enough in Stack B; Stack A intentionally faded but not illegible |

## Pass / fail gates

- Any `TODO(Day11-task03)` left in submitted files.
- Changing HTML structure (adding wrapper elements) beyond completing existing TODO comment slots.

## Detailed rubric

### Correctness

- [ ] Stack A uses `opacity` such that paragraph text is faded vs body baseline.
- [ ] Stack B uses alpha `background-color` (or equivalent) rather than subtree `opacity` for the tint.

### Edge cases

- [ ] Stripes remain partially visible through Stack B overlay.

## Evidence the grader should collect

- Screenshot showing both stacks side-by-side highlighting text contrast difference.

## AI-assisted grading prompt (optional)

```markdown
## AI grading prompt (paste into your grader)
You are evaluating a graduate-level assignment. Use only observable criteria below.
Repository context: `Day 11/practical-tasks/task-03-opacity-stacking-clinic`.
Candidate changed files: `index.html`, `styles/main.css`.
Rubric: confirm TODOs removed; confirm no wrapper elements added; confirm Stack A paragraph is visually more faded than Stack B while Stack B keeps stronger text; confirm checklist includes a code snippet about opacity grouping/multiplication.
Return: Pass/Fail, score table, blocking issues, non-blocking suggestions.
```
