# Grading results — Days 30–45 (index)

**Student (as shown in repo files):** Sahithi  
**Graded:** 2026-10-10  
**Scope:** Work as committed under `Day 30` … `Day 45` in this repository (not a separate submission branch).  
**Scale:** Each task **/25**; each day **/100** (four tasks). See `course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`.

**Grading policy (guide v1.2.0):** Leftover `TODO`/instructional comments are **not** penalized. Low scores reflect **missing/broken behavior** (stubs returning 501, empty reducers, unimplemented components), not comments.

**Course audit note:** All **45** day folders exist with 4 practical tasks each. Days **01–29** were already graded earlier. This segment covers the remaining Days **30–45**.

Per-day breakdowns live inside each day folder as `GRADING_RESULTS.md`:

| Day | Results file | Total /100 | Snapshot |
|-----|----------------|------------|----------|
| Day 30 | [`Day 30/GRADING_RESULTS.md`](Day%2030/GRADING_RESULTS.md) | **96** | All four regex labs pass Vitest; flags, character classes, quantifiers, and YAML-ish key extraction are solid. |
| Day 31 | [`Day 31/GRADING_RESULTS.md`](Day%2031/GRADING_RESULTS.md) | **96** | Map/Set/Symbol/WeakMap labs all pass; frequency count and metadata WeakMap are clean. |
| Day 32 | [`Day 32/GRADING_RESULTS.md`](Day%2032/GRADING_RESULTS.md) | **96** | Strict-this, safe JSON parse, custom ValidationError, and Result-type challenge all pass. |
| Day 33 | [`Day 33/GRADING_RESULTS.md`](Day%2033/GRADING_RESULTS.md) | **96** | Non-greedy match, capture-group replace, Promise constructor, and promise-chain challenge all pass. |
| Day 34 | [`Day 34/GRADING_RESULTS.md`](Day%2034/GRADING_RESULTS.md) | **95** | Strong first React day: props, PropTypes badge, class banner, and mixed dashboard cards are complete. |
| Day 35 | [`Day 35/GRADING_RESULTS.md`](Day%2035/GRADING_RESULTS.md) | **86** | Counter, disclosure, and class timer are solid; theme persistence has a typo that breaks dark reload (`'right'` vs `'dark'`). |
| Day 36 | [`Day 36/GRADING_RESULTS.md`](Day%2036/GRADING_RESULTS.md) | **15** | Composition/lifting labs are still starter stubs — components ignore props/children and use placeholders. |
| Day 37 | [`Day 37/GRADING_RESULTS.md`](Day%2037/GRADING_RESULTS.md) | **28** | Controlled form labs largely unfinished; only thin partial wiring on signup validation / checkbox `checked` binding. |
| Day 38 | [`Day 38/GRADING_RESULTS.md`](Day%2038/GRADING_RESULTS.md) | **22** | Keys/HOC labs unfinished; only the starter stable-key list remains from task 01. |
| Day 39 | [`Day 39/GRADING_RESULTS.md`](Day%2039/GRADING_RESULTS.md) | **20** | Redux slice/selector edit surfaces are still empty stubs (actions do not update state). |
| Day 40 | [`Day 40/GRADING_RESULTS.md`](Day%2040/GRADING_RESULTS.md) | **20** | Async thunk `extraReducers` not wired across all four tasks; profile URL still points at `users/0`. |
| Day 41 | [`Day 41/GRADING_RESULTS.md`](Day%2041/GRADING_RESULTS.md) | **14** | Node ESM/event-loop/fs labs are mostly unimplemented stubs; all Vitest suites fail. |
| Day 42 | [`Day 42/GRADING_RESULTS.md`](Day%2042/GRADING_RESULTS.md) | **31** | Express scaffolding mostly unfinished; task 04 has handler logic but JSON middleware still runs after the router (the core footgun). |
| Day 43 | [`Day 43/GRADING_RESULTS.md`](Day%2043/GRADING_RESULTS.md) | **12** | JWT labs are stubs — helpers throw and routes return 501; all suites fail. |
| Day 44 | [`Day 44/GRADING_RESULTS.md`](Day%2044/GRADING_RESULTS.md) | **32** | Mongoose connect/CRUD mostly stubs; Book schema partially filled on tasks 02 and 04. |
| Day 45 | [`Day 45/GRADING_RESULTS.md`](Day%2045/GRADING_RESULTS.md) | **22** | Capstone mostly unfinished; task 04 implements notes create/list but PATCH/DELETE and error middleware remain open. |
| **Segment (Days 30–45)** | — | **781 / 1600** (**≈ 48.8%**) | — |

## Completion pattern (important)

| Range | Status |
|-------|--------|
| Days **30–33** (JS: regex → promises) | **Complete** — Vitest all pass (~96 each) |
| Days **34–35** (React intro) | **Mostly complete** (theme reload typo on Day 35 task 04) |
| Days **36–40** (React composition → Redux thunks) | **Mostly incomplete / stubs** |
| Days **41–45** (Node → capstone) | **Mostly incomplete / stubs** (all Vitest fail) |

Your impression that work is “only till ~35” matches the evidence: **Days 30–35 are the last consistently finished block**; after that, most tasks are still starter scaffolds.

## Top priorities

1. **Day 35 task 04:** change `'right'` → `'dark'` in `ThemeShell.jsx` so dark theme restores on reload.  
2. **Days 36–37:** implement composition (`children`/slots) and controlled form state — these unlock later React weeks.  
3. **Days 38–40:** finish keys/HOC, Redux reducers, and thunk `extraReducers`.  
4. **Days 41–45:** replace throw/501 stubs with real Node/Express/JWT/Mongoose handlers; run `npm test` per task.

## How to rerun checks

- Days 30–33, 41–45: `cd "Day XX/practical-tasks/task-YY-..." && npm test`  
- Days 34–40 (React Vite apps): no `test` script — manual review against `TASK_INSTRUCTIONS.md` / `EVALUATION_CRITERIA.md` (or `npm run build` if you want a compile check).

---

*Instructor-style formative grading on the repo snapshot.*
