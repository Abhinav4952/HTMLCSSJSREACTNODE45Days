# Instructor grading — Day 08 (1–100)

> **Learner profile:** Second-year graduate. Grade for **lab completion** and **taught concepts**, not production polish.

## Canonical methodology

Use **`course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`** for category definitions, bands, feedback tone, and AI workflow.

## Day snapshot

- **Primary focus (map):** Positioning: static/relative, absolute, fixed/sticky, stacking contexts.
- **This file lives at:** `Day 08/INSTRUCTOR_GRADING_1-100.md` (**day-level**; not inside each `task-*` folder).

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

### Task 1 — Static/relative playground

- **Folder:** `practical-tasks/task-01-static-relative-playground/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-01-static-relative-playground/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-01-static-relative-playground/TASK_INSTRUCTIONS.md`

#### Observable checklist

- relative offsets behave as instructed; containing blocks understood.
- No accidental absolute unless task introduces it next.

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

### Task 2 — Absolute containing block challenge

- **Folder:** `practical-tasks/task-02-absolute-containing-block-challenge/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-02-absolute-containing-block-challenge/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-02-absolute-containing-block-challenge/TASK_INSTRUCTIONS.md`

#### Observable checklist

- position:absolute positioned against correct ancestor per brief.
- z-index/stacking not “random”; offsets measurable.

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

### Task 3 — Fixed header & sticky sidebar

- **Folder:** `practical-tasks/task-03-fixed-header-sticky-sidebar/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-03-fixed-header-sticky-sidebar/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-03-fixed-header-sticky-sidebar/TASK_INSTRUCTIONS.md`

#### Observable checklist

- fixed header doesn’t obscure content (padding/margin compensation if required).
- sticky behavior respects overflow ancestors (common footgun—note in feedback if hit).

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

### Task 4 — Stacking context & z-index mystery

- **Folder:** `practical-tasks/task-04-stacking-context-z-index-mystery/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-04-stacking-context-z-index-mystery/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-04-stacking-context-z-index-mystery/TASK_INSTRUCTIONS.md`

#### Observable checklist

- stacking context sources identified (opacity/transform/etc. if in brief).
- Fix uses minimal z-index changes; avoids z-index arms race where possible.

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
Grade the full Day 08 submission (all tasks under Day 08/practical-tasks/).
Evidence: <paste diff or list files reviewed>.
For each task, fill the /25 table using the checklist in Day 08/INSTRUCTOR_GRADING_1-100.md; sum to /100.
Follow course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md for tone and output format.
Return: day total /100, per-task subscores, pass/needs-revision, 3 day-level improvement suggestions, hard concerns.
```
