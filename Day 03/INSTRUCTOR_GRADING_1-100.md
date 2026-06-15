# Instructor grading — Day 03 (1–100)

> **Learner profile:** Second-year graduate. Grade for **lab completion** and **taught concepts**, not production polish.

## Canonical methodology

Use **`course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`** for category definitions, bands, feedback tone, and AI workflow.

## Day snapshot

- **Primary focus (map):** Accessible tables: structure, scope, spanning, presentation styling.
- **This file lives at:** `Day 03/INSTRUCTOR_GRADING_1-100.md` (**day-level**; not inside each `task-*` folder).

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

### Task 1 — Simple data table

- **Folder:** `practical-tasks/task-01-simple-data-table/`
- **Type:** **HTML**
- **Candidate rubric:** `practical-tasks/task-01-simple-data-table/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-01-simple-data-table/TASK_INSTRUCTIONS.md`

#### Observable checklist

- table/thead/tbody structure where required; tr/td/th valid.
- Captions or headings if specified; no layout tables for data.

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

### Task 2 — Scope headers & thead/tbody

- **Folder:** `practical-tasks/task-02-thead-tbody-scope-headers/`
- **Type:** **HTML**
- **Candidate rubric:** `practical-tasks/task-02-thead-tbody-scope-headers/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-02-thead-tbody-scope-headers/TASK_INSTRUCTIONS.md`

#### Observable checklist

- th scope values correct for reading axis (col/row as taught).
- Header cells align with data cells visually and structurally.

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

### Task 3 — Colspan/rowspan timetable

- **Folder:** `practical-tasks/task-03-colspan-rowspan-timetable/`
- **Type:** **HTML**
- **Candidate rubric:** `practical-tasks/task-03-colspan-rowspan-timetable/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-03-colspan-rowspan-timetable/TASK_INSTRUCTIONS.md`

#### Observable checklist

- colspan/rowspan grid mathematically consistent (no ragged holes).
- Screen reader sanity: headers still discoverable where required.

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

### Task 4 — Styled pricing table

- **Folder:** `practical-tasks/task-04-styled-pricing-table/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-04-styled-pricing-table/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-04-styled-pricing-table/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Table remains semantic after styling (no display:table hacks that destroy semantics).
- Zebra/hover/borders readable; responsive shrink doesn’t destroy alignment beyond lab scope.

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
Grade the full Day 03 submission (all tasks under Day 03/practical-tasks/).
Evidence: <paste diff or list files reviewed>.
For each task, fill the /25 table using the checklist in Day 03/INSTRUCTOR_GRADING_1-100.md; sum to /100.
Follow course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md for tone and output format.
Return: day total /100, per-task subscores, pass/needs-revision, 3 day-level improvement suggestions, hard concerns.
```
