# Grading results — Day 42

**Student (as shown in repo files):** Sahithi  
**Graded:** 2026-10-10  
**Scope:** Work as committed in this repository under `Day 42/practical-tasks/` (not a separate submission branch).  
**Scale:** Each task **/25**; this day **/100** (four tasks). See [`../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`](../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md).  
**Grading policy note:** Leftover `TODO`/instructional comments are **not** penalized (guide v1.2.0); only missing/broken behavior is scored.

## Day total: **31 / 100**

Express scaffolding mostly unfinished; task 04 has handler logic but JSON middleware still runs after the router (the core footgun).

## Per-task scores

| Task | Folder | Score /25 | Primary evidence reviewed |
|------|--------|-----------|---------------------------|
| 01 | `practical-tasks/task-01-express-json-health` | **3** | `GET /health` returns 501; `npm test` **0/1**. |
| 02 | `practical-tasks/task-02-router-mount-and-request-logging` | **8** | Ping route wired; missing `X-Lab-Tag` middleware; `npm test` **0/1**. |
| 03 | `practical-tasks/task-03-post-json-body-in-memory-store` | **6** | GET todos present; POST still 501; `npm test` **0/1**. |
| 04 | `practical-tasks/task-04-middleware-order-error-handling` | **14** | Widget POST validation/201 present, but `express.json()` still mounted after `/v1` router; `npm test` **0/1**. |

## Segment overview (Days 30–45)

[`../GRADING_RESULTS_DAYS_30-45.md`](../GRADING_RESULTS_DAYS_30-45.md)
