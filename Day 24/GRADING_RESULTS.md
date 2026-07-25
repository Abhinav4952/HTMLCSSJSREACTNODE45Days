# Grading results — Day 24

**Student (as shown in repo files):** Sahithi  
**Graded:** 2026-07-25  
**Scope:** Work as committed in this repository under `Day 24/practical-tasks/` (not a separate submission branch).  
**Scale:** Each task **/25**; this day **/100** (four tasks). JS tasks use the Vitest weighting (9 + 9 + 5 + 2). See [`../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`](../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md).  
**Grading policy note:** Leftover `TODO`/instructional comments are **not** penalized (guide v1.2.0). The low scores below are **not** for comments — tasks 01-03 are genuinely unimplemented stubs, so the missing behavior is scored under Requirements coverage.

## Day total: **36 / 100**

Only the strict-`this` footgun challenge is implemented. The `this` basics, call/apply, and bind labs are starter stubs (return `NaN`/`null`/unbound), so their suites fail. Implementing these three `this`-binding functions is the priority.

## Per-task scores

| Task | Folder | Score /25 | Primary evidence reviewed |
|------|--------|-----------|---------------------------|
| 01 | `practical-tasks/task-01-method-calls-and-this` | **4** | `src/thisBasicsLab.js`, `npm test` — **0/2 passed**; `createCounter` still seeds `total: NaN` and `inc()` never writes. |
| 02 | `practical-tasks/task-02-call-and-apply-borrowing` | **4** | `src/callApplyLab.js`, `npm test` — **0/2 passed**; `renderWithHost`/`maxWithApply` unimplemented. |
| 03 | `practical-tasks/task-03-bind-partial-application` | **4** | `src/bindLab.js`, `npm test` — **0/2 passed**; `bindFirstArg` returns `fn` unbound; `bindMethod` returns `() => null`. |
| 04 | `practical-tasks/task-04-strict-this-footgun-challenge` | **24** | `src` module, `npm test` — **2/2 passed**. |

## Segment overview (Days 16–29)

[`../GRADING_RESULTS_DAYS_16-29.md`](../GRADING_RESULTS_DAYS_16-29.md)
