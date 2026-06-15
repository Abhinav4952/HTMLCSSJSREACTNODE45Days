# Instructor grading — Day 01 (1–100)

> **Learner profile:** Second-year graduate. Grade for **lab completion** and **taught concepts**, not production polish.

## Canonical methodology

Use **`course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`** for category definitions, bands, feedback tone, and AI workflow.

## Day snapshot

- **Primary focus (map):** HTML5 shell, metadata, assets, structured profile markup.
- **This file lives at:** `Day 01/INSTRUCTOR_GRADING_1-100.md` (**day-level**; not inside each `task-*` folder).

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

### Task 1 — Minimal valid HTML5 document

- **Folder:** `practical-tasks/task-01-minimal-valid-document/`
- **Type:** **HTML**
- **Candidate rubric:** `practical-tasks/task-01-minimal-valid-document/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-01-minimal-valid-document/TASK_INSTRUCTIONS.md`

#### Observable checklist

- <!DOCTYPE html> present and first; HTML5 mode implied.
- <html lang="…"> set meaningfully (e.g. en unless directed).
- Charset + viewport meta + <title> present and sensible.
- Body content renders; no broken self-inflicted console errors from markup.
- TODO markers resolved per cohort policy (no “fake done”).

**Hard concerns for this task:**

- **Hard concern:** Missing doctype or charset where required by instructions.

#### Score this task (max **25**)

Use category maxima below; **sum row must not exceed 25** for this task.

| Category | Max | Score | Notes |
|----------|----:|------:|-------|
| Requirements coverage | 10 |  |  |
| Correctness (browser / behavior) | 8 |  |  |
| Semantics, a11y, maintainability | 5 |  |  |
| Process & polish | 2 |  |  |
| **Subtotal this task** | **25** |  |  |

### Task 2 — Head metadata basics

- **Folder:** `practical-tasks/task-02-head-metadata-basics/`
- **Type:** **HTML**
- **Candidate rubric:** `practical-tasks/task-02-head-metadata-basics/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-02-head-metadata-basics/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Favicon / icon link wired as instructed; paths valid.
- Social / SEO meta only if task asked—avoid cargo-cult tags.
- Title and description (if required) match visible page intent.
- Relative asset paths resilient to opening file vs simple server.

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

### Task 3 — External assets defer/async

- **Folder:** `practical-tasks/task-03-external-assets-defer-async/`
- **Type:** **HTML**
- **Candidate rubric:** `practical-tasks/task-03-external-assets-defer-async/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-03-external-assets-defer-async/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Scripts placed per lab goals (defer/async semantics understood in markup).
- No duplicate loads unless justified; order preserves dependencies.
- CSS linked once; no flash of totally unstyled content beyond lab scope.
- Brief rationale comment acceptable; avoid essay-length comments.

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

### Task 4 — Structured profile page

- **Folder:** `practical-tasks/task-04-structured-profile-page/`
- **Type:** **HTML**
- **Candidate rubric:** `practical-tasks/task-04-structured-profile-page/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-04-structured-profile-page/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Landmarks/sections reflect outline (header/main/section/article as taught).
- Heading levels coherent (no skipped levels for decoration).
- Lists/tables only where semantically correct.
- Readable source formatting; IDs/classes meaningful.

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
Grade the full Day 01 submission (all tasks under Day 01/practical-tasks/).
Evidence: <paste diff or list files reviewed>.
For each task, fill the /25 table using the checklist in Day 01/INSTRUCTOR_GRADING_1-100.md; sum to /100.
Follow course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md for tone and output format.
Return: day total /100, per-task subscores, pass/needs-revision, 3 day-level improvement suggestions, hard concerns.
```
