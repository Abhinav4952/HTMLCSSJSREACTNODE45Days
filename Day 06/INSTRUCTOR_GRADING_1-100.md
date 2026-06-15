# Instructor grading — Day 06 (1–100)

> **Learner profile:** Second-year graduate. Grade for **lab completion** and **taught concepts**, not production polish.

## Canonical methodology

Use **`course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`** for category definitions, bands, feedback tone, and AI workflow.

## Day snapshot

- **Primary focus (map):** Shadows, fluid type & units, em/rem mental model, Vitest units lab.
- **This file lives at:** `Day 06/INSTRUCTOR_GRADING_1-100.md` (**day-level**; not inside each `task-*` folder).

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

### Task 1 — Shadow studio cards

- **Folder:** `practical-tasks/task-01-shadow-studio-cards/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-01-shadow-studio-cards/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-01-shadow-studio-cards/TASK_INSTRUCTIONS.md`

#### Observable checklist

- box-shadow/text-shadow used intentionally (layered shadows if asked).
- Performance reasonable (no enormous blur chains unless instructed).

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

### Task 2 — Fluid type clamp & viewport units

- **Folder:** `practical-tasks/task-02-fluid-type-clamp-and-viewport/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-02-fluid-type-clamp-and-viewport/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-02-fluid-type-clamp-and-viewport/TASK_INSTRUCTIONS.md`

#### Observable checklist

- clamp()/min()/max() fluid type behaves across two viewport widths in manual check.
- vw/vh used without accidental overflow traps (where task warns).

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

### Task 3 — em/rem compounding trap

- **Folder:** `practical-tasks/task-03-em-rem-compounding-trap/`
- **Type:** **CSS**
- **Candidate rubric:** `practical-tasks/task-03-em-rem-compounding-trap/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-03-em-rem-compounding-trap/TASK_INSTRUCTIONS.md`

#### Observable checklist

- Demonstrates understanding of em compounding vs rem stability per brief.
- Fix avoids “magic numbers” without brief justification comments if rubric expects explanation.

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

### Task 4 — CSS length math lab (Vitest)

- **Folder:** `practical-tasks/task-04-css-length-math-lab/`
- **Type:** **JS** (Vitest)
- **Candidate rubric:** `practical-tasks/task-04-css-length-math-lab/EVALUATION_CRITERIA.md`
- **Brief:** `practical-tasks/task-04-css-length-math-lab/TASK_INSTRUCTIONS.md`

#### Observable checklist

- `npm test` passes with no edits to autograder files.
- Public functions match contracts (NaN, RangeError message exactness if specified).
- No global side effects; pure functions remain pure.
- Readable names; small helpers only if they clarify (avoid over-abstraction).

**Hard concerns for this task:**

- **Hard concern:** Tests edited against instructions; plagiarism on implementations.

#### Score this task (max **25**)

Use category maxima below; **sum row must not exceed 25** for this task.

| Category | Max | Score | Notes |
|----------|----:|------:|-------|
| Requirements (instructions + API) | 9 |  |  |
| `npm test` / correctness | 9 |  |  |
| Code clarity & safety | 5 |  |  |
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
Grade the full Day 06 submission (all tasks under Day 06/practical-tasks/).
Evidence: <paste diff or list files reviewed>.
For each task, fill the /25 table using the checklist in Day 06/INSTRUCTOR_GRADING_1-100.md; sum to /100.
Follow course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md for tone and output format.
Return: day total /100, per-task subscores, pass/needs-revision, 3 day-level improvement suggestions, hard concerns.
```
