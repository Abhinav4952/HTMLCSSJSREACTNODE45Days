# Grading results — Day 27

**Student (as shown in repo files):** Sahithi  
**Graded:** 2026-07-25  
**Scope:** Work as committed in this repository under `Day 27/practical-tasks/` (not a separate submission branch).  
**Scale:** Each task **/25**; this day **/100** (four tasks). JS tasks use the Vitest weighting (9 + 9 + 5 + 2). See [`../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`](../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md).  
**Grading policy note:** Leftover `TODO`/instructional comments are **not** penalized (guide v1.2.0); only missing/broken behavior is scored.

## Day total: **96 / 100**

Class fields, `#private` balance, static factory parser, and the bank-account challenge all pass; good use of `#private` fields and `static` members. Minor: a couple of unreachable trailing `return` lines (cosmetic).

## Per-task scores

| Task | Folder | Score /25 | Primary evidence reviewed |
|------|--------|-----------|---------------------------|
| 01 | `practical-tasks/task-01-class-counter-fields` | **24** | `src/counterClass.js`, `npm test` — **2/2 passed**. |
| 02 | `practical-tasks/task-02-private-hash-balance` | **24** | `src/vault.js`, `npm test` — **2/2 passed**; `#private` field encapsulation. |
| 03 | `practical-tasks/task-03-static-factory-parser` | **24** | `src/token.js`, `npm test` — **2/2 passed**. |
| 04 | `practical-tasks/task-04-bank-account-challenge` | **24** | `src/bankAccount.js`, `npm test` — **1/1 passed**; `#balance` + `static count`, withdraw clamps to available funds. |

## Segment overview (Days 16–29)

[`../GRADING_RESULTS_DAYS_16-29.md`](../GRADING_RESULTS_DAYS_16-29.md)
