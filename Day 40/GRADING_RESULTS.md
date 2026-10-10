# Grading results — Day 40

**Student (as shown in repo files):** Sahithi  
**Graded:** 2026-10-10  
**Scope:** Work as committed in this repository under `Day 40/practical-tasks/` (not a separate submission branch).  
**Scale:** Each task **/25**; this day **/100** (four tasks). See [`../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`](../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md).  
**Grading policy note:** Leftover `TODO`/instructional comments are **not** penalized (guide v1.2.0); only missing/broken behavior is scored.

## Day total: **20 / 100**

Async thunk `extraReducers` not wired across all four tasks; profile URL still points at `users/0`.

## Per-task scores

| Task | Folder | Score /25 | Primary evidence reviewed |
|------|--------|-----------|---------------------------|
| 01 | `practical-tasks/task-01-fetch-posts-thunk` | **5** | `extraReducers` empty; pending/fulfilled/rejected not handled. |
| 02 | `practical-tasks/task-02-profile-thunk-rejection` | **5** | Still fetches `users/0`; no rejection handling. |
| 03 | `practical-tasks/task-03-delayed-submit-order-thunk` | **5** | `submitOrder` cases missing (only `resetCheckout` works). |
| 04 | `practical-tasks/task-04-post-detail-integration` | **5** | `fetchPostBundle` `extraReducers` not wired. |

## Segment overview (Days 30–45)

[`../GRADING_RESULTS_DAYS_30-45.md`](../GRADING_RESULTS_DAYS_30-45.md)
