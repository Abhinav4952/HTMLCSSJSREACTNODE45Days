# Grading results — Day 06

**Student (as shown in repo files):** Sahithi  
**Graded:** 2026-06-04  
**Scope:** Work as committed in this repository under `Day 06/practical-tasks/` (not a separate submission branch).  
**Scale:** Each task **/25**; this day **/100** (four tasks). See [`../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`](../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md).

## Day total: **83 / 100**

Task 04 tests pass (**Vitest 20/20**). Fix the `--step-1` clamp in task 02 so the max is a sensible `rem` cap, not `320px`.

## Per-task scores

| Task | Folder | Score /25 | Primary evidence reviewed |
|------|--------|-----------|---------------------------|
| 01 | `practical-tasks/task-01-shadow-studio-cards` | **23** | `styles/main.css` — tokens + elevation + focus; minor polish (`TODO` lines, text-shadow choice). |
| 02 | `practical-tasks/task-02-fluid-type-clamp-and-viewport` | **16** | `styles/main.css` — `--step-1` max clamped to **320px** (not a usable font-size cap). |
| 03 | `practical-tasks/task-03-em-rem-compounding-trap` | **20** | `styles/main.css` — explanatory comment added; nested module/chip rules largely stabilized in file but `TODO` still present (verify in browser if any depth still shrinks). |
| 04 | `practical-tasks/task-04-css-length-math-lab` | **24** | `src/unitsLab.js`, `npm test` — **20/20 tests passed**; leave `// TODO` cleanup for submission hygiene. |

## Segment overview (Days 01–08)

[`../GRADING_RESULTS_DAYS_01-08.md`](../GRADING_RESULTS_DAYS_01-08.md)
