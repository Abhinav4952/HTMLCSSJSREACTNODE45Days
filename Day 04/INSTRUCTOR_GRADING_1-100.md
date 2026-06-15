# Instructor grading — Day 04 (1–100)

> **Learner profile:** Second-year graduate. Grade for **lab completion** and **taught concepts**, not production polish.

## Canonical methodology

Use **`course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`** for category definitions, bands, feedback tone, and AI workflow.

## Day snapshot

- **Primary focus (map):** Forms: labels, HTML5 inputs, controls, GET vs POST.
- **This file lives at:** `Day 04/INSTRUCTOR_GRADING_1-100.md` (**day-level**; not inside each `task-*` folder).

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

### Task 1 — Labeled fieldset form

- **Folder:** `practical-tasks/task-01-labeled-fieldset-form/`
- **Type:** **HTML**
- **Candidate rubric:** `practical-tasks/task-01-labeled-fieldset-form/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-01-labeled-fieldset-form/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Every input has label (explicit for/id or wrapping pattern per task).
- fieldset/legend used correctly if required.
- Button types intentional (submit vs button).

**Hard concerns for this task:**

- **Hard concern:** Clickable label not associated with control (if task requires labels).

#### Score this task (max **25**)

Use category maxima below; **sum row must not exceed 25** for this task.

| Category | Max | Score | Notes |
|----------|----:|------:|-------|
| Requirements coverage | 10 |  |  |
| Correctness (browser / behavior) | 8 |  |  |
| Semantics, a11y, maintainability | 5 |  |  |
| Process & polish | 2 |  |  |
| **Subtotal this task** | **25** |  |  |

### Task 2 — HTML5 inputs & validation

- **Folder:** `practical-tasks/task-02-html5-inputs-validation/`
- **Type:** **HTML**
- **Candidate rubric:** `practical-tasks/task-02-html5-inputs-validation/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-02-html5-inputs-validation/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Appropriate input types (email/url/number/date…) per brief.
- Validation attributes used as taught (required, min/max, pattern) without fighting UX.
- Error affordances match instructions (native vs custom if specified).

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

### Task 3 — Textarea, select, buttons

- **Folder:** `practical-tasks/task-03-textarea-select-buttons/`
- **Type:** **HTML**
- **Candidate rubric:** `practical-tasks/task-03-textarea-select-buttons/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-03-textarea-select-buttons/TASK_INSTRUCTIONS.md`

#### Observable checklist

- select options meaningful; optgroup if specified.
- textarea sizing/resize rules per CSS brief.
- Keyboard operable controls (no trapped focus in simple pages).

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

### Task 4 — GET/POST method lab

- **Folder:** `practical-tasks/task-04-get-post-method-lab/`
- **Type:** **HTML**
- **Candidate rubric:** `practical-tasks/task-04-get-post-method-lab/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-04-get-post-method-lab/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Forms use correct method/action targets per instructions.
- Control names produce expected query/body shape in devtools network preview.
- Security hygiene: no secrets in GET URLs for passwords (if applicable to scenario).

**Hard concerns for this task:**

- **Hard concern:** Password or sensitive data placed in GET form (redo + teach).

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
Grade the full Day 04 submission (all tasks under Day 04/practical-tasks/).
Evidence: <paste diff or list files reviewed>.
For each task, fill the /25 table using the checklist in Day 04/INSTRUCTOR_GRADING_1-100.md; sum to /100.
Follow course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md for tone and output format.
Return: day total /100, per-task subscores, pass/needs-revision, 3 day-level improvement suggestions, hard concerns.
```
