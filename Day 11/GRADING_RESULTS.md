# Grading results — Day 11

**Student (as shown in repo files):** Sahithi  
**Graded:** 2026-06-23  
**Scope:** Work as committed in this repository under `Day 11/practical-tasks/` (not a separate submission branch).  
**Scale:** Each task **/25**; this day **/100** (four tasks). See [`../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`](../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md).

## Day total: **83 / 100**

Specificity duel and Vitest lab are strong; finish the custom-properties playground (Ops nested card + accent-derived card tint) and remove debug `console.log` from `cascadeLab.js`.

## Per-task scores

| Task | Folder | Score /25 | Primary evidence reviewed |
|------|--------|-----------|---------------------------|
| 01 | `practical-tasks/task-01-inheritance-and-custom-properties-playground` | **17** | `index.html`, `styles/main.css` — region tokens + inherited `color` work; Ops region lacks nested `.card`; card background is fixed `rgba(...)` not derived from `--region-accent`. |
| 02 | `practical-tasks/task-02-specificity-duel-scoreboard` | **24** | `styles/main.css`, `index.html` — champion colors match targets (#7c3aed, #0ea5e9, #f97316). |
| 03 | `practical-tasks/task-03-opacity-stacking-clinic` | **20** | `index.html`, `styles/main.css` — both opacity vs rgba stacks; checklist explanation thin and cites `0.5` while CSS uses `0.8`. |
| 04 | `practical-tasks/task-04-cascade-specificity-lab` | **22** | `src/cascadeLab.js`, `npm test` — **15/15 tests passed**; stray debug `console.log` blocks left in module. |

## Segment overview (Days 09–15)

[`../GRADING_RESULTS_DAYS_09-15.md`](../GRADING_RESULTS_DAYS_09-15.md)
