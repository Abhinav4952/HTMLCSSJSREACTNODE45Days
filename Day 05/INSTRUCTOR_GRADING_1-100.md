# Instructor grading — Day 05 (1–100)

> **Learner profile:** Second-year graduate. Grade for **lab completion** and **taught concepts**, not production polish.

## Canonical methodology

Use **`course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`** for category definitions, bands, feedback tone, and AI workflow.

## Day snapshot

- **Primary focus (map):** Selectors, borders/backgrounds, text decoration/transform, card gallery.
- **This file lives at:** `Day 05/INSTRUCTOR_GRADING_1-100.md` (**day-level**; not inside each `task-*` folder).

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

### Task 1 — Selector practice board

- **Folder:** `practical-tasks/task-01-selector-practice-board/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-01-selector-practice-board/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-01-selector-practice-board/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Selectors match targets without over-broad `*` abuse unless taught.
- Combinators/pseudo-classes used as specified.

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

### Task 2 — Borders & backgrounds cards

- **Folder:** `practical-tasks/task-02-borders-backgrounds-cards/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-02-borders-backgrounds-cards/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-02-borders-backgrounds-cards/TASK_INSTRUCTIONS.md`

#### Observable checklist

- border-radius/background layering matches mock intent.
- Contrast readable on cards; borders don’t clip content unexpectedly.

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

### Task 3 — Text decoration & transform banner

- **Folder:** `practical-tasks/task-03-text-decoration-transform-banner/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-03-text-decoration-transform-banner/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-03-text-decoration-transform-banner/TASK_INSTRUCTIONS.md`

#### Observable checklist

- text-decoration / text-transform applied per spec.
- Transforms don’t harm readability; transform-origin considered if animated.

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

### Task 4 — Product card gallery

- **Folder:** `practical-tasks/task-04-product-card-gallery/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-04-product-card-gallery/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-04-product-card-gallery/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Card layout stable; images sized (object-fit if taught).
- Hover/focus states visible and not keyboard-hostile.

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
Grade the full Day 05 submission (all tasks under Day 05/practical-tasks/).
Evidence: <paste diff or list files reviewed>.
For each task, fill the /25 table using the checklist in Day 05/INSTRUCTOR_GRADING_1-100.md; sum to /100.
Follow course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md for tone and output format.
Return: day total /100, per-task subscores, pass/needs-revision, 3 day-level improvement suggestions, hard concerns.
```
