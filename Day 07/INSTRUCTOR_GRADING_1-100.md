# Instructor grading — Day 07 (1–100)

> **Learner profile:** Second-year graduate. Grade for **lab completion** and **taught concepts**, not production polish.

## Canonical methodology

Use **`course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`** for category definitions, bands, feedback tone, and AI workflow.

## Day snapshot

- **Primary focus (map):** Box model, margin collapse, border-box migration.
- **This file lives at:** `Day 07/INSTRUCTOR_GRADING_1-100.md` (**day-level**; not inside each `task-*` folder).

## Day scoring model (100 = full day)

| Task slot | Max points | Running total |
|-----------|------------:|---------------|
| Task 1 | 25 | 25 |
| Task 2 | 25 | 50 |
| Task 3 | 25 | 75 |
| Task 4 | 25 | **100** |

**Day total /100** = sum of the four task subtotals (each task scored out of **25**).

For **HTML/CSS tasks**, within each /25 use the scaled rows in each task’s table (10 + 8 + 5 + 2). For **Day 06 Task 4 (Vitest)**, use the JS row group (9 + 9 + 5 + 2).

---

## Tasks

### Task 1 — Box model measurement sheet

- **Folder:** `practical-tasks/task-01-box-model-measurement-sheet/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-01-box-model-measurement-sheet/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-01-box-model-measurement-sheet/TASK_INSTRUCTIONS.md`

#### Observable checklist

- padding/border/margin relationships match exercise measurements.
- box-sizing choice consistent with instructions (content-box vs border-box lesson).

**Hard concerns:** add institution-specific issues if discovered.

#### Score this task (max **25**)

Use category maxima below; **sum row must not exceed 25** for this task.

| Category | Max | Score | Notes |
|----------|----:|------:|-------|
| Requirements coverage | 10 |  |  |
| Correctness (browser / behavior) | 8 |  |  |
| Semantics, a11y, maintainability | 5 |  |  |
| Process & polish | 2 |  |  |
| **Subtotal this task** | **25** |  |  |

### Task 2 — Margin collapse detective

- **Folder:** `practical-tasks/task-02-margin-collapse-detective/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-02-margin-collapse-detective/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-02-margin-collapse-detective/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Collapse scenarios identified/fixes match taught rules.
- Demonstrations reproducible in browser (not accidental layout dependence).

**Hard concerns:** add institution-specific issues if discovered.

#### Score this task (max **25**)

Use category maxima below; **sum row must not exceed 25** for this task.

| Category | Max | Score | Notes |
|----------|----:|------:|-------|
| Requirements coverage | 10 |  |  |
| Correctness (browser / behavior) | 8 |  |  |
| Semantics, a11y, maintainability | 5 |  |  |
| Process & polish | 2 |  |  |
| **Subtotal this task** | **25** |  |  |

### Task 3 — border-box migration playground

- **Folder:** `practical-tasks/task-03-border-box-migration-playground/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-03-border-box-migration-playground/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-03-border-box-migration-playground/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Global/local border-box strategy matches brief; no double resets chaos.
- Regression checks: widths predictable after migration.

**Hard concerns:** add institution-specific issues if discovered.

#### Score this task (max **25**)

Use category maxima below; **sum row must not exceed 25** for this task.

| Category | Max | Score | Notes |
|----------|----:|------:|-------|
| Requirements coverage | 10 |  |  |
| Correctness (browser / behavior) | 8 |  |  |
| Semantics, a11y, maintainability | 5 |  |  |
| Process & polish | 2 |  |  |
| **Subtotal this task** | **25** |  |  |

### Task 4 — Triple collapse clinic

- **Folder:** `practical-tasks/task-04-triple-collapse-clinic/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-04-triple-collapse-clinic/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-04-triple-collapse-clinic/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Three collapse cases addressed distinctly (not one hack for all).
- Comments explain “why” briefly where non-obvious.

**Hard concerns:** add institution-specific issues if discovered.

#### Score this task (max **25**)

Use category maxima below; **sum row must not exceed 25** for this task.

| Category | Max | Score | Notes |
|----------|----:|------:|-------|
| Requirements coverage | 10 |  |  |
| Correctness (browser / behavior) | 8 |  |  |
| Semantics, a11y, maintainability | 5 |  |  |
| Process & polish | 2 |  |  |
| **Subtotal this task** | **25** |  |  |

---

## Day record sheet (optional)

| Task | Max | Score | Notes |
|------|----:|------:|-------|
| Task 1 | 25 |  |  |
| Task 2 | 25 |  |  |
| Task 3 | 25 |  |  |
| Task 4 | 25 |  |  |
| **Day total** | **100** |  |  |

## Day-level band (same scale as guide §5)

Map **Day total** to labels using `05-…` §5 (Excellent 90–100, Strong 80–89, …).

## AI-assisted grading prompt (paste)

```text
Grade the full Day 07 submission (all tasks under Day 07/practical-tasks/).
Evidence: <paste diff or list files reviewed>.
For each task, fill the /25 table using the checklist in Day 07/INSTRUCTOR_GRADING_1-100.md; sum to /100.
Follow course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md for tone and output format.
Return: day total /100, per-task subscores, pass/needs-revision, 3 day-level improvement suggestions, hard concerns.
```
