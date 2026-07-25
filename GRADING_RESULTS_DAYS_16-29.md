# Grading results — Days 16–29 (index)

**Student (as shown in repo files):** Sahithi  
**Graded:** 2026-07-25  
**Scope:** Work as committed under `Day 16` … `Day 29` in this repository (not a separate submission branch).  
**Scale:** Each task **/25**; each day **/100** (four tasks). See `course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`.

**Grading policy (guide v1.2.0):** Leftover `TODO`/instructional comments are **not** penalized. Low scores on Days 20/24/25 are for **genuinely unimplemented functions** (stubs that still `return null`/`NaN`), scored under Requirements coverage — not for comments.

Per-day breakdowns (task-level scores and evidence) live **inside each day folder** as `GRADING_RESULTS.md`:

| Day | Focus | Results file | Total /100 |
|-----|-------|----------------|------------|
| Day 16 | Responsive / container queries (CSS) | [`Day 16/GRADING_RESULTS.md`](Day%2016/GRADING_RESULTS.md) | **95** |
| Day 17 | typeof / scope / template / coercion | [`Day 17/GRADING_RESULTS.md`](Day%2017/GRADING_RESULTS.md) | **96** |
| Day 18 | Control flow (if / loops / switch) | [`Day 18/GRADING_RESULTS.md`](Day%2018/GRADING_RESULTS.md) | **96** |
| Day 19 | Objects & property descriptors | [`Day 19/GRADING_RESULTS.md`](Day%2019/GRADING_RESULTS.md) | **96** |
| Day 20 | Array methods (filter/map/sort/reduce) | [`Day 20/GRADING_RESULTS.md`](Day%2020/GRADING_RESULTS.md) | **40** |
| Day 21 | Functions / defaults / hoisting | [`Day 21/GRADING_RESULTS.md`](Day%2021/GRADING_RESULTS.md) | **96** |
| Day 22 | Spread / rest / destructuring | [`Day 22/GRADING_RESULTS.md`](Day%2022/GRADING_RESULTS.md) | **96** |
| Day 23 | Equality / coercion | [`Day 23/GRADING_RESULTS.md`](Day%2023/GRADING_RESULTS.md) | **96** |
| Day 24 | this / call / apply / bind | [`Day 24/GRADING_RESULTS.md`](Day%2024/GRADING_RESULTS.md) | **36** |
| Day 25 | HOF / fluent / curry / memoize | [`Day 25/GRADING_RESULTS.md`](Day%2025/GRADING_RESULTS.md) | **37** |
| Day 26 | Closures | [`Day 26/GRADING_RESULTS.md`](Day%2026/GRADING_RESULTS.md) | **96** |
| Day 27 | Classes / #private / static | [`Day 27/GRADING_RESULTS.md`](Day%2027/GRADING_RESULTS.md) | **96** |
| Day 28 | Prototypes / delegation | [`Day 28/GRADING_RESULTS.md`](Day%2028/GRADING_RESULTS.md) | **96** |
| Day 29 | Class inheritance | [`Day 29/GRADING_RESULTS.md`](Day%2029/GRADING_RESULTS.md) | **96** |
| **Segment (Days 16–29)** | — | — | **1168 / 1400** (**≈ 83.4%**) |

## Top priorities (cross-cutting)

1. **Finish the three unimplemented labs on each of Days 20, 24, and 25.** These are the only real gaps in the segment — the functions are still starter stubs returning `null`/`NaN`, so their Vitest suites fail. Implementing them would lift each of those days from the 30s into the 90s.
2. **Pattern to notice:** on Days 20/24/25 only the *challenge* (task 04) is done while the three "core" tasks are blank — likely the core tasks were skipped. Prioritize the core tasks first; they build the foundation the challenge assumes.
3. **Minor cleanup (no points lost):** a few completed functions keep unreachable trailing `return` lines (e.g. `budgetModule.js`, `bankAccount.js`). Harmless, but removing dead code improves readability.

## How to rerun checks

- Any JS task: `cd "Day XX/practical-tasks/task-YY-..." && npm test`
- Re-run the whole segment's suites from the repo root by looping over `Day {17..29}/practical-tasks/*/` where a `package.json` exists.
- Day 16 (CSS): manual review against each folder's `TASK_INSTRUCTIONS.md` + `EVALUATION_CRITERIA.md`.

## Result

- **47 of 56 graded tasks** in this segment pass their full Vitest suites or (Day 16) meet the CSS brief (4 CSS + 43 JS).
- **9 tasks incomplete** (Day 20 ×3, Day 24 ×3, Day 25 ×3) — unimplemented stubs.

---

*Instructor-style formative grading on the repo snapshot; adjust if grading a different branch or zip submission. Days 01–15 scores were left unchanged per instruction; the no-TODO-penalty policy applies from Day 16 onward.*
