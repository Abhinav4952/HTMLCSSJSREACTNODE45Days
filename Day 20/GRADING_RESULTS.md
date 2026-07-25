# Grading results — Day 20

**Student (as shown in repo files):** Sahithi  
**Graded:** 2026-07-25  
**Scope:** Work as committed in this repository under `Day 20/practical-tasks/` (not a separate submission branch).  
**Scale:** Each task **/25**; this day **/100** (four tasks). JS tasks use the Vitest weighting (9 + 9 + 5 + 2). See [`../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`](../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md).  
**Grading policy note:** Leftover `TODO`/instructional comments are **not** penalized (guide v1.2.0). The low scores below are **not** for comments — tasks 01-03 are genuinely unimplemented stubs (functions still `return null`), so the missing behavior is scored under Requirements coverage.

## Day total: **40 / 100**

Only the search/slice lab is implemented. `filter/map`, `sort`, and `reduce` labs are still starter stubs returning `null`, so their suites fail. Implementing the three array functions is the priority.

## Per-task scores

| Task | Folder | Score /25 | Primary evidence reviewed |
|------|--------|-----------|---------------------------|
| 01 | `practical-tasks/task-01-filter-map-pipeline` | **5** | `src/pipelineLab.js`, `npm test` — **1/3 passed**; `doublePositives` still `return null` (only the "not an array" guard passes). |
| 02 | `practical-tasks/task-02-sort-comparator-lab` | **6** | `src/sortLab.js`, `npm test` — **2/4 passed**; `sortCaseInsensitive` unimplemented (`return null`). |
| 03 | `practical-tasks/task-03-reduce-ledger-lite` | **5** | `src/reduceLab.js`, `npm test` — **1/3 passed**; `ledgerBalance` unimplemented (`return null`). |
| 04 | `practical-tasks/task-04-array-search-and-slice` | **24** | `src` module, `npm test` — **7/7 passed**. |

## Segment overview (Days 16–29)

[`../GRADING_RESULTS_DAYS_16-29.md`](../GRADING_RESULTS_DAYS_16-29.md)
