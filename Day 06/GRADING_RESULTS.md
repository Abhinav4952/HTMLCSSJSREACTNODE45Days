# Day 06 — Grading results

**Branch:** `Vijay-practice`  
**Student work attribution in files:** Tejaswi (see HTML titles/author meta)  
**Scale:** Each task **/25**; day total **/100**.  
**Policy:** Leftover `TODO` comments are **not** penalized when required behavior works (guide v1.2.0).

## Day total: **39/100**

| Task | Folder | Score /25 | Rationale |
|------|--------|----------:|-----------|
| 01 | `task-01-shadow-studio-cards` | **7** | `--shadow-*` vars defined; card/btn/hero shadow rules still empty TODO blocks. |
| 02 | `task-02-fluid-type-clamp-and-viewport` | **15** | clamp() steps wired; `--pad-x` undefined while `.paper` uses it — padding broken. |
| 03 | `task-03-em-rem-compounding-trap` | **4** | Footgun rules remain; no rem stabilization or required fix commentary. |
| 04 | `task-04-css-length-math-lab` | **13** | `npm test`: 11 passed / 9 failed — happy paths work; missing validation/edge cases; `nestedEmFontPx` ReferenceError. |

## Notes

Tokens/fluid type started; shadow studio and em/rem trap incomplete. Vitest lab: **11/20** tests passed.

---

*Instructor-style formative grading on the repo snapshot for this branch.*
