# Evaluation Criteria — Day 11 — Task 02 — Specificity Duel Scoreboard

## Scope

Graded: `styles/main.css` selector strategy + computed colors on the three champion lines; subtitle text TODO in `index.html`.  
Out of scope: redesigning the whole arena layout.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | Computed hex colors match exactly |
| Requirements coverage | 25 | Rule-count constraints respected; no forbidden techniques |
| Code quality | 20 | Selectors are minimal-ish and readable |

## Pass / fail gates

- Any use of `!important` or inline styles on champion lines.
- Changing HTML structure beyond the allowed subtitle TODO.
- Match 1: more than **one** newly added winning rule (count added non-empty rule blocks you introduce).

## Detailed rubric

### Correctness

- [ ] Match 1: `#7c3aed`
- [ ] Match 2: `#0ea5e9`
- [ ] Match 3: `#f97316`

### Edge cases

- [ ] Match 2 uses **at most two** added rules (document in a short HTML comment near your rules if you need clarity).

## Evidence the grader should collect

- DevTools computed color screenshots for each match (3 total) **or** paste computed values from DevTools.

## AI-assisted grading prompt (optional)

```markdown
## AI grading prompt (paste into your grader)
You are evaluating a graduate-level assignment. Use only observable criteria below.
Repository context: `Day 11/practical-tasks/task-02-specificity-duel-scoreboard`.
Candidate changed files: likely `styles/main.css` + small `index.html` text.
Rubric: verify no `!important` and no inline styles; verify HTML structure unchanged except subtitle text; verify computed colors for the three `.champion-line` targets; verify Match 1 adds only one new rule block; verify Match 2 adds at most two new rule blocks beyond starter file (instructor may count blocks manually).
Return: Pass/Fail, score table, blocking issues, non-blocking suggestions.
```
