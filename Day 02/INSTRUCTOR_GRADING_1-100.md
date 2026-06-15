# Instructor grading — Day 02 (1–100)

> **Learner profile:** Second-year graduate. Grade for **lab completion** and **taught concepts**, not production polish.

## Canonical methodology

Use **`course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`** for category definitions, bands, feedback tone, and AI workflow.

## Day snapshot

- **Primary focus (map):** Semantic outline, inline semantics, typography, inheritance/cascade.
- **This file lives at:** `Day 02/INSTRUCTOR_GRADING_1-100.md` (**day-level**; not inside each `task-*` folder).

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

### Task 1 — Article outline & headings

- **Folder:** `practical-tasks/task-01-article-outline-headings/`
- **Type:** **HTML**
- **Candidate rubric:** `practical-tasks/task-01-article-outline-headings/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-01-article-outline-headings/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Single h1 (unless task explicitly allows pattern X).
- Heading order matches document outline in DevTools outline/A11y tree.
- Paragraph/sectioning supports scanning (not wall of divs).

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

### Task 2 — Inline semantics & lists

- **Folder:** `practical-tasks/task-02-inline-semantics-and-lists/`
- **Type:** **HTML**
- **Candidate rubric:** `practical-tasks/task-02-inline-semantics-and-lists/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-02-inline-semantics-and-lists/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Appropriate emphasis elements (strong/em/cite/q) vs bold italics alone.
- Lists: ol/ul choice matches meaning; nesting valid.
- Links descriptive (avoid “click here” unless task teaches contrast).

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

### Task 3 — Font stack & line-height

- **Folder:** `practical-tasks/task-03-font-stack-and-line-height/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-03-font-stack-and-line-height/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-03-font-stack-and-line-height/TASK_INSTRUCTIONS.md`

#### Observable checklist

- font-family stack plausible with fallbacks.
- line-height improves readability vs browser default where asked.
- No illegible contrast on body text (basic WCAG awareness).

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

### Task 4 — Inheritance reading page

- **Folder:** `practical-tasks/task-04-inheritance-reading-page/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-04-inheritance-reading-page/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-04-inheritance-reading-page/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Demonstrates inheritance/cascade goal from instructions (specific selectors).
- Unexpected overrides explained by source order/specificity (if rubric asks).
- CSS organized by section or component, not one giant unordered block.

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
Grade the full Day 02 submission (all tasks under Day 02/practical-tasks/).
Evidence: <paste diff or list files reviewed>.
For each task, fill the /25 table using the checklist in Day 02/INSTRUCTOR_GRADING_1-100.md; sum to /100.
Follow course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md for tone and output format.
Return: day total /100, per-task subscores, pass/needs-revision, 3 day-level improvement suggestions, hard concerns.
```
