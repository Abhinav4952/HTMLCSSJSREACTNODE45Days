# 05 — Instructor Grading (1–100), Graduate Learner Lens, and AI Evaluation Reference

**Instruction set version:** `1.1.0`  
**Use with:** `03-DAY-FOLDER-TASK-STRUCTURE-AND-NAMING-CONVENTIONS.md` (per-task `EVALUATION_CRITERIA.md` for candidates) and `04-AUTHORING-GUIDE-…` (task design).

This document is for **instructors** and **AI grading agents**. It standardizes how to assign **1–100** scores for **Days 01–08 style** work (mostly **static HTML/CSS**; occasional **Vitest** labs), and how to give **constructive** feedback appropriate for **second-year graduate students** who are **not** expected to ship production systems.

---

## 1. Where the numeric rubric lives (**day-level**, recommended)

For **early HTML/CSS days (reference rollout: Days 01–08)**, numeric instructor grading is consolidated in **one file per day** at the **day folder root**:

- **`Day XX/INSTRUCTOR_GRADING_1-100.md`**

That file:

- Points to each **`practical-tasks/task-NN-…/`** folder for checklists and scoring **/25 per task** (four tasks → **/100** for the day).
- Keeps **candidate-facing** rubrics in each task’s **`EVALUATION_CRITERIA.md`** (unchanged).

**Rule:** Candidates focus on `TASK_INSTRUCTIONS.md` + `EVALUATION_CRITERIA.md`. Instructors and AI agents use **`Day XX/INSTRUCTOR_GRADING_1-100.md`** + **this guide** for **numeric** day totals so learners are not distracted by `/100` in every task folder.

**Optional per-task files:** You *may* add task-local numeric sheets later for other cohorts; if present, they must not contradict the day file without an instructor note.

**Regenerate Days 01–08 day files:** `node scripts/emit-instructor-grading-days-01-08.mjs` (from repo root).

---

## 2. Graduate learner lens (non-negotiable tone)

- **Reward:** meeting the **task instructions** and **learning goals**; clear structure; sensible naming; obvious debugging effort.
- **Do not penalize heavily for:** missing “enterprise” patterns (build pipelines, design systems, exhaustive cross-browser QA, Lighthouse 100, etc.) unless the task explicitly requires them.
- **Do penalize meaningfully for:** skipping stated requirements; inaccessible or misleading markup where the task taught semantics; copying without understanding (if evidence exists); leaving `TODO` markers “completed” but non-functional.
- **Default feedback style:** “Here is what works → here is the smallest next step to level up,” citing **MDN**/**spec** links from the day’s theory where possible.

---

## 3. Default 100-point category model (HTML/CSS tasks)

Use this **within each task’s /25 slice** (see `Day XX/INSTRUCTOR_GRADING_1-100.md` tables) unless a task’s `EVALUATION_CRITERIA.md` explicitly overrides weighting.

| Category | Points | Instructor notes |
|----------|-------:|------------------|
| **Requirements coverage** | **40** | Map each bullet in `TASK_INSTRUCTIONS.md` “What you will implement” / manual checklist to yes/partial/no. |
| **Correctness in context** | **30** | For static tasks: renders as intended in a modern browser; no broken paths; forms/tables behave as described. |
| **Semantics, accessibility, maintainability** | **20** | Headings order, labels on controls, table headers/scope where taught, class names readable, CSS not overly specific “magic”. |
| **Process & polish** | **10** | Git hygiene if visible; removes stale TODOs; comments only where helpful; minor consistency (indentation, file organization). |

**Day file scaling:** For a **/25 per task** row, use **10 + 8 + 5 + 2** (sums to 25) as proportional weights of the above.

### Optional adjustment for **JavaScript (Vitest)** tasks (e.g. Day 06 `task-04`)

| Category | Points | Notes |
|----------|-------:|------|
| Requirements coverage | 35 | Include public API + edge cases from instructions. |
| **Automated tests (`npm test`)** | **35** | Primary signal where tests exist. |
| Code clarity & safety | 20 | Naming, guard clauses, no silent swallowing of errors where task forbids it. |
| Process & polish | 10 | Same as above. |

**Day file scaling for one JS task /25:** use **9 + 9 + 5 + 2** (sums to 25) as printed in `Day 06/INSTRUCTOR_GRADING_1-100.md` for Task 4.

---

## 4. Translating categories to a single **1–100** score

### Day-level (recommended for Days 01–08)

1. Score **each of four tasks** out of **25** using that task’s table in **`Day XX/INSTRUCTOR_GRADING_1-100.md`**.
2. **Sum** → **Day total /100**.
3. Round to nearest integer for reporting.

### Task-only (if you ever split reporting)

1. Score each category **out of its max** within that task’s slice.
2. Sum → total out of 25 (or out of 100 if you use full-day weights on a single task).

**Do not** invent sub-points outside the table without documenting them in the “Notes” column of the record sheet.

---

## 5. Suggested banding (cohort-adjustable)

These bands communicate progress; **your program** sets official pass marks. Apply to **Day total /100** (or to per-task /25 if you report separately).

| Total | Label | Typical meaning |
|------:|-------|-------------------|
| **90–100** | **Excellent** | All requirements met; few nits; demonstrates understanding beyond checklist (still not “production audit”). |
| **80–89** | **Strong** | Requirements met; minor gaps in polish or one partial requirement well explained. |
| **70–79** | **Satisfactory** | Core requirements met; several small issues or one moderate gap. |
| **60–69** | **Needs revision** | Important requirement missing or incorrect pattern (e.g. wrong table semantics) but salvageable with targeted fixes. |
| **< 60** | **Incomplete / redo** | Multiple requirements missing, fundamentally broken deliverable, or academic integrity concerns. |

---

## 6. Pass / fail gates (instructor discretion)

Even with a numeric score, retain **hard stops** where ethics/safety matter:

- **Academic dishonesty** evidence → follow institutional policy (separate from numeric rubric).
- **Dangerous content** in student-hosted examples (rare) → escalate, do not “grade around” it.

For **HTML/CSS** days, common **automatic redo** triggers:

- Task explicitly requires labels/associations and none exist.
- Form controls unusable (no `name` where GET/POST lab requires it; etc.) *when that was the learning goal*.

---

## 7. Giving feedback candidates will actually use

Use this **order**:

1. **Recognition** — what clearly meets the brief (be specific: file + behavior).
2. **Priority fixes** — max **3** items, ordered by impact on users/learners.
3. **Stretch (optional)** — one “level up” tied to employability: accessibility, responsive edge, cleaner CSS structure.

**Phrases to prefer**

- “For the next iteration, try …”
- “This meets the lab; in a portfolio piece you might also …”

**Phrases to avoid**

- “This is trivially wrong” / “obviously bad” (demotivates; not aligned with grad training stage).

---

## 8. AI-assisted grading workflow (recommended)

1. For the day: open **`Day XX/INSTRUCTOR_GRADING_1-100.md`** and each task’s **`TASK_INSTRUCTIONS.md`** + **`EVALUATION_CRITERIA.md`** as needed.
2. Collect **evidence**: candidate diff or files; for HTML/CSS, optionally screenshots or short screen recording if policy allows.
3. Produce:
   - **Day total /100** (sum of four **/25** tasks) + optional per-task subscores
   - **3 prioritized suggestions** (day-level or per-task, as your template asks)
   - **Pass/needs revision** recommendation per cohort rules

### Paste-ready AI prompt fragment

```text
You are grading a second-year graduate web foundations lab (HTML/CSS/JS intro).
Use ONLY observable evidence from the submitted files. Do not assume unstated tooling.
Use Day XX/INSTRUCTOR_GRADING_1-100.md for per-task /25 tables and checklists; sum to a day total /100.
Follow category philosophy in course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md.
Output:
1) Day total /100 with per-task /25 subscores
2) Pass/needs-revision recommendation using the band table (guide §5)
3) Three concrete improvements (best-practice nudges), each <= 2 sentences
4) List any hard-fail issues separately
```

---

## 9. Extending to later days (React, Node, etc.)

- **React / Node tasks:** keep the same **1–100 sum model** at **day** or **milestone** granularity; shift weight toward **rubric items** and **automated tests** where present (see `02` and `04`).
- Prefer **one instructor file per day** (or per “grading unit”) to match this pattern.
- Always keep **candidate-facing** `EVALUATION_CRITERIA.md` aligned with what you grade numerically.

---

## 10. Changelog

| Version | Date | Notes |
|---------|------|-------|
| `1.1.0` | 2026-06-04 | Day-level `Day XX/INSTRUCTOR_GRADING_1-100.md`; remove per-task default; script emits day files. |
| `1.0.0` | 2026-06-04 | Initial instructor numeric rubric + AI reference. |
