# Grading results — Day 35

**Student (as shown in repo files):** Sahithi  
**Graded:** 2026-10-10  
**Scope:** Work as committed in this repository under `Day 35/practical-tasks/` (not a separate submission branch).  
**Scale:** Each task **/25**; this day **/100** (four tasks). See [`../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`](../course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md).  
**Grading policy note:** Leftover `TODO`/instructional comments are **not** penalized (guide v1.2.0); only missing/broken behavior is scored.

## Day total: **86 / 100**

Counter, disclosure, and class timer are solid; theme persistence has a typo that breaks dark reload (`'right'` vs `'dark'`).

## Per-task scores

| Task | Folder | Score /25 | Primary evidence reviewed |
|------|--------|-----------|---------------------------|
| 01 | `practical-tasks/task-01-hooks-counter-usestate` | **22** | `Counter.jsx` — `useState(0)`, +1/-1/Reset, live output; updaters work but slightly non-idiomatic. |
| 02 | `practical-tasks/task-02-toggle-panel-usestate` | **24** | `DisclosurePanel.jsx` — starts collapsed; toggles body visibility. |
| 03 | `practical-tasks/task-03-class-timer-lifecycle` | **24** | `TicketTimer.jsx` — interval in `componentDidMount`, cleared on unmount. |
| 04 | `practical-tasks/task-04-effect-theme-localstorage` | **16** | `ThemeShell.jsx` — writes theme to localStorage, but init checks `storedTheme==='right'` instead of `'dark'`, so dark mode does not restore on reload. |

## Segment overview (Days 30–45)

[`../GRADING_RESULTS_DAYS_30-45.md`](../GRADING_RESULTS_DAYS_30-45.md)
