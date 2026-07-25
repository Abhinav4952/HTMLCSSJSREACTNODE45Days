# Grading results — Day 25

**Student (as shown in repo files):** Sahithi  
**Graded:** 2026-07-25  
**Scope:** Work as committed in this repository under `Day 25/practical-tasks/` (not a separate submission branch).  
**Scale:** Each task **/25**; this day **/100** (four tasks). JS tasks use the Vitest weighting (9 + 9 + 5 + 2). See [`../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`](../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md).  
**Grading policy note:** Leftover `TODO`/instructional comments are **not** penalized (guide v1.2.0). The low scores below are **not** for comments — tasks 01-03 are genuinely unimplemented stubs, so the missing behavior is scored under Requirements coverage.

## Day total: **37 / 100**

Only the memoize challenge is implemented. The HOF map/negate, fluent query builder, and curry labs are starter stubs, so their suites fail. Implementing these is the priority.

## Per-task scores

| Task | Folder | Score /25 | Primary evidence reviewed |
|------|--------|-----------|---------------------------|
| 01 | `practical-tasks/task-01-higher-order-callback-map` | **5** | `src/callbackLab.js`, `npm test` — **1/3 passed**; `mapWith` returns `null`, `negate` returns `() => false`. |
| 02 | `practical-tasks/task-02-fluent-config-chain` | **4** | `src/fluentChainLab.js`, `npm test` — **0/2 passed**; `build()` returns `"INVALID"`; `select`/`from` do not store state. |
| 03 | `practical-tasks/task-03-curry-binary-operations` | **4** | `src/curryLab.js`, `npm test` — **0/2 passed**; `curryBinary`/`makeClamp` return `null` closures. |
| 04 | `practical-tasks/task-04-memoize-stable-keys-challenge` | **24** | `src` module, `npm test` — **3/3 passed**. |

## Segment overview (Days 16–29)

[`../GRADING_RESULTS_DAYS_16-29.md`](../GRADING_RESULTS_DAYS_16-29.md)
