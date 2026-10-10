# Grading results — Day 44

**Student (as shown in repo files):** Sahithi  
**Graded:** 2026-10-10  
**Scope:** Work as committed in this repository under `Day 44/practical-tasks/` (not a separate submission branch).  
**Scale:** Each task **/25**; this day **/100** (four tasks). See [`../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`](../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md).  
**Grading policy note:** Leftover `TODO`/instructional comments are **not** penalized (guide v1.2.0); only missing/broken behavior is scored.

## Day total: **32 / 100**

Mongoose connect/CRUD mostly stubs; Book schema partially filled on tasks 02 and 04.

## Per-task scores

| Task | Folder | Score /25 | Primary evidence reviewed |
|------|--------|-----------|---------------------------|
| 01 | `practical-tasks/task-01-mongoose-connect-health` | **3** | `connectMongo` throws; health stays disconnected; tests skipped/failed. |
| 02 | `practical-tasks/task-02-schema-model-create-book` | **18** | Title `required: true` present; missing `trim: true`; `npm test` **0/1**. |
| 03 | `practical-tasks/task-03-books-crud-routes` | **3** | All CRUD routes return 501; `npm test` **0/1**. |
| 04 | `practical-tasks/task-04-schema-validation-and-timestamps` | **8** | `trim` on title; missing `minlength: 3` and `{ timestamps: true }`; `npm test` **0/2**. |

## Segment overview (Days 30–45)

[`../GRADING_RESULTS_DAYS_30-45.md`](../GRADING_RESULTS_DAYS_30-45.md)
