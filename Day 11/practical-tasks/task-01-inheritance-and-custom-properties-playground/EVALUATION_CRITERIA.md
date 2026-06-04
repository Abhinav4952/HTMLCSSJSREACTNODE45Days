# Evaluation Criteria — Day 11 — Task 01 — Inheritance &amp; Custom Properties Playground

## Scope

Graded: completed `TODO(Day11-task01)` markers in `index.html` and `styles/main.css`.  
Out of scope: redesigning unrelated layout, adding frameworks.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 40 | Tokens resolve; nested text inherits region color |
| Requirements coverage | 35 | All TODOs completed; marketing vs ops palettes differ |
| Code quality | 15 | CSS stays readable; no `!important` |
| Docs / readability | 10 | HTML copy is coherent and professional |

## Pass / fail gates

- Any `TODO(Day11-task01)` left incomplete in shipped files.
- Using `opacity` on `.card` or `.panel` to create the tint (violates constraints).

## Detailed rubric

### Correctness

- [ ] `--region-fg` and `--region-accent` exist at root/body defaults.
- [ ] Both `data-region` sections override both variables.
- [ ] `.panel` text color is driven by `var(--region-fg)` (or equivalent inherited chain).

### Edge cases

- [ ] Nested card paragraph inherits without redundant per-tag `color`.

### UX / accessibility

- [ ] Text/background contrast remains readable in both regions.

## Evidence the grader should collect

- Short note listing the two region palettes (hex values).
- Screenshot showing different accent bars + readable nested text.

## AI-assisted grading prompt (optional)

```markdown
## AI grading prompt (paste into your grader)
You are evaluating a graduate-level assignment. Use only observable criteria below.
Repository context: HTML/CSS course task `Day 11/practical-tasks/task-01-inheritance-and-custom-properties-playground`.
Candidate changed files: `index.html`, `styles/main.css`.
Rubric: confirm all `TODO(Day11-task01)` are gone; verify custom properties exist on root/body; verify both `data-region` blocks override tokens; verify nested paragraphs inherit region text color without redundant `p` color rules; verify no `opacity` tinting on `.card`/`.panel`; confirm readable contrast.
Return: Pass/Fail, score table, blocking issues, non-blocking suggestions.
```
