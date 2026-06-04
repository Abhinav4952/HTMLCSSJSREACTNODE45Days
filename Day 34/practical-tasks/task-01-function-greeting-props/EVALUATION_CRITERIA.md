# Evaluation Criteria — Day 34 — Task 1 — Function greeting with props

## Scope

Graded: `src/components/UserGreeting.jsx` behavior against props as used in `App.jsx`.  
Out of scope: visual polish, extra components, routing, global state.

## Weighting (100 points unless instructor overrides)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 45 | Greeting strings match prop contracts and defaults. |
| Code quality | 25 | Clear destructuring; no prop mutation; readable JSX. |
| Requirements coverage | 20 | Both `App.jsx` usages behave as specified. |
| Docs / readability | 10 | Small comments only if needed; no dead code. |

## Pass / fail gates (automatic fail if violated)

- App fails to compile (`npm run build` errors) after candidate changes.
- Props are mutated in place (e.g. assigning to `name` on the props object).
- Required behavior is implemented outside `UserGreeting.jsx` in a way that violates the task constraints.

## Detailed rubric

### Correctness

- **Full credit:** `Avery` + `student` shows name and role in parentheses; `Jordan` without `role` shows name only; missing `name` path shows **Hello, guest** rules as documented in instructions.
- **Partial:** Correct for one case but wrong defaulting or stray punctuation such as `()` when `role` absent.
- **No credit:** Hard-coded strings ignoring props.

### Edge cases

- Undefined `role` must not render empty parentheses.

### UX / accessibility

- A single `<p>` or heading is fine; no need for ARIA roles here beyond reasonable text.

## Evidence the grader should collect

- Output of `npm run build` (success).
- Screenshot or copied text from the running page for both greeting rows.

## AI grading prompt (paste into your grader)

You are evaluating a graduate-level assignment. Use only observable criteria below.  
Repository context: Vite + React 18 (JSX, automatic runtime).  
Candidate changed files: focus on `src/components/UserGreeting.jsx`.  
Rubric: Day 34 Task 1 evaluation doc in-repo.  
Return: Pass/Fail, score table, blocking issues, non-blocking suggestions.
