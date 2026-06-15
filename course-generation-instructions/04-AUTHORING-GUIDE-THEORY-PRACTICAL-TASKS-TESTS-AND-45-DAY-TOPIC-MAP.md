# 04 — Authoring Guide: Theory, Practical Tasks, Tests, Evaluation, and 45-Day Topic Map

**Instruction set version:** `1.0.0`

This document tells agents **how to design exercises** and provides a **default day-by-day topic allocation** for all 45 days. If an instructor publishes a revised map, follow the instructor’s map instead.

---

## Part A — Practical task design principles

### A.1 Task types mix (weekly rhythm guideline)

Across any **7-day window**, aim for **variety**:

- At least **two** HTML/CSS or layout-centric tasks (until Day 13–14 when CSS major arc completes; afterwards use CSS inside React).
- At least **two** JavaScript logic tasks with **unit tests** (once JS segment begins).
- At least **one** integration-style task in later weeks (mini feature).

**Exception:** Node-only days (41–45) will skew toward backend tasks.

### A.2 Difficulty curve within a single day

| Task slot | Purpose |
|-----------|---------|
| `task-01` | Warm-up; mostly follows examples from theory; confidence builder |
| `task-02` | Core skill for the day; independent coding |
| `task-03` | Stretch within the day; combines 1–2 prior concepts |
| `task-04` | Optional “capstone-lite” or reading-heavy + implementation mix |

If only **three** tasks are used, merge `task-04` goals into `task-03` and explicitly label difficulty.

### A.3 Anti-patterns (do not generate tasks like these)

- **Mystery tasks** — instructions that omit acceptance criteria.
- **Huge boilerplate** — candidates spend time deleting code instead of learning.
- **Brittle tests** — snapshot tests for trivial markup unless justified.
- **Hidden coupling** — task requires knowledge not yet taught unless labeled **Challenge (requires research)**.

### A.4 Academic integrity nudge

Tasks should encourage **original variable names** and **small variations** in UI copy so identical solutions across students are less likely. Still keep evaluation objective using tests/rubrics.

---

## Part B — JavaScript testing guidance (deep)

### B.1 Prefer testing **behavioral contracts**

Good:

- Exported function returns correct outputs for listed inputs.
- Pure functions for most “core JS” days.

Acceptable with care:

- Module-internal helpers tested via public API only (preferred).

Avoid:

- Asserting exact error message strings unless taught.

### B.2 File layout patterns

**Pattern 1 — single module under test**

- `src/<topic>.js` exports functions.
- `tests/<topic>.test.js` imports and tests.

**Pattern 2 — Node CLI**

- Candidate implements `src/cli.js`; tests spawn process or call exported `main(args)`—pick the simpler option.

### B.3 Starter code behavior

- Provide **stub implementations** that `throw new Error('TODO(Day..): ...')` **or** return obviously wrong values that fail tests.
- Document the expected red output in `TASK_INSTRUCTIONS.md`.

### B.4 Coverage

100% coverage is **not** required. Target **meaningful** tests for requirements.

---

## Part C — React task guidance (manual / AI evaluation)

### C.1 What to include in boilerplate

- Working dev server.
- Clear component boundaries where TODOs live.
- If using Redux, provide **store setup** skeleton and require candidates to fill reducers/actions.

### C.2 Rubric must reference UI states

Examples:

- “Empty state renders …”
- “Validation message appears when …”
- “Submit disabled until …”

### C.3 Keys and lists

Include at least one list rendering task before Day 40 where missing/wrong keys cause a measurable bug (duplicate state, lost focus) **or** explain in theory + verify via rubric.

---

## Part D — Node / Express task guidance

### D.1 Middleware ordering

Include at least one task where wrong middleware order demonstrably breaks auth or error handling.

### D.2 JWT tasks

- Use `Authorization: Bearer <token>` header pattern.
- Include rubric items for **token verification** and **401/403** distinctions where appropriate.
- Never require storing tokens in localStorage for API-only tasks unless paired with security discussion in theory; prefer header-based flows for simplicity.

### D.3 Mongo tasks

- Use in-memory or Docker instructions; avoid “install Mongo locally” without alternatives.
- Handle connection errors gracefully in rubric (candidate demonstrates basic error handling).

### D.4 Event loop tasks

Include **at least one** measurable exercise:

- blocking code vs non-blocking,
- `setTimeout` ordering,
- microtasks vs macrotasks at a **pedagogically honest** depth (do not overclaim).

---

## Part E — Mapping topics to theory sections (agent checklist)

When writing `DAY-XX-THEORY-AND-REFERENCE.md`, agents should ensure:

- Every **primary theme** for the day appears as an `##` or `###` heading.
- Every **subtopic** uses the per-subtopic template from file `03` (What / Why / Pros-cons / Without / Syntax / 3–5 examples / Self-test).
- Examples are runnable or clearly marked as partial.
- **Cross-links** to prior days when reusing concepts (“Review Day 07 box model…”).

---

## Part F — Reference 45-day topic map (default schedule)

**Legend for “Suggested tasks” column:**

- **H** = HTML/CSS static or minimal tooling
- **J** = JavaScript with `npm test`
- **R** = React (manual + rubric)
- **N** = Node/Express/Mongo/JWT (manual + rubric)

Agents: adapt exact slugs, but keep **topic coverage**.

| Day | Primary focus | Subtopics (non-exhaustive) | Suggested task mix |
|----:|---------------|----------------------------|--------------------|
| 01 | Basic page structure & metadata | Doctype; HTML vs XHTML (practical); `<html>`, `<head>`, `<body>`; metadata; linking CSS/JS; defer/async basics | H,H,H,H |
| 02 | Text semantics & formatting | Semantic text tags; CSS typography; font stacks; line-height; inheritance preview | H,H,H,H |
| 03 | Tables | `table`, `thead/tbody`, `tr/td/th`, colspan/rowspan; basic styling; accessibility cautions | H,H,H,H |
| 04 | Forms foundation | `form`, `label`, `input`, `textarea`, `select`, `button`; GET vs POST conceptually | H,H,H,H |
| 05 | CSS selectors & decoration | Simple/combinator selectors; border/background; `text-decoration`, `text-transform` | H,H,H,H |
| 06 | Shadows & CSS units | Box shadow, text shadow; px/rem/em/vw/vh; when to use which | H,H,H,J |
| 07 | Box model | Content/padding/border/margin; `box-sizing`; margin collapse | H,H,H,H |
| 08 | Positioning | `static/relative/absolute/fixed/sticky`; stacking context intro | H,H,H,H |
| 09 | Display & layout patterns | `block/inline/inline-block`; common layout patterns (holy grail intro without grid requirement) | H,H,H,H |
| 10 | Pseudo-classes & pseudo-elements | `:first-child`, `:nth-child`, `:focus-visible`; `::before/::after` (content, counters light) | H,H,H,H |
| 11 | Cascade & inheritance + opacity | Specificity; source order; `!important` caution; opacity vs rgba | H,H,H,J |
| 12 | HTML5 semantics & inputs | Semantic containers; new input types; validation attributes | H,H,H,H |
| 13 | Responsive design (first pass) | Fluid layouts; min/max widths; basic media queries | H,H,H,H |
| 14 | Flexbox | Axes, justify/align, wrap, grow/shrink, common dashboards | H,H,H,H |
| 15 | Advanced selectors & transitions | Attribute selectors; transform/transition; `animation` keyframes; `resize` where useful | H,H,H,H |
| 16 | Advanced responsive | Media-query strategies; responsive typography; practical page revision | H,H,H,H |
| 17 | JS values & variables | Types; `var/let/const`; coercion preview; template literals | J,J,J,J |
| 18 | Expressions, operators, control flow | Loops, conditionals; truthiness; switch | J,J,J,J |
| 19 | Objects deepened | Creation; property access; methods; descriptors (intro) | J,J,J,J |
| 20 | Arrays & collection methods | sort/filter/map/reduce (intro reduce lightly); searching | J,J,J,J |
| 21 | Functions & scope basics | Declarations vs expressions; arrow functions; default params | J,J,J,J |
| 22 | ES2015 toolkit | Spread/rest; destructuring; `for..of` | J,J,J,J |
| 23 | Advanced expressions | Hoisting; comparisons; implicit conversions; tricky edge cases | J,J,J,J |
| 24 | `this`, `call`, `apply`, `bind` | Dynamic `this`; borrowing; binding patterns | J,J,J,J |
| 25 | Functional patterns | IIFE; callbacks; memoization; chaining; currying | J,J,J,J |
| 26 | Closures | Lexical scope; loops + closures pitfall; module pattern intro | J,J,J,J |
| 27 | OOP in JS | Constructors; fields; private `#`; static | J,J,J,J |
| 28 | Prototypes | `Object.create`; prototype chain; `instanceof` | J,J,J,J |
| 29 | Classes & inheritance | ES2015 classes; `extends`; `super` | J,J,J,J |
| 30 | Regex basics | Flags; literals; common classes; quantifiers | J,J,J,J |
| 31 | ES2015 collections & objects | `Object.keys/values`; computed props; getters/setters; `Symbol`; `Set/Map/WeakSet/WeakMap` | J,J,J,J |
| 32 | Strict mode & errors | `'use strict'` effects; try/catch/finally; custom errors | J,J,J,J |
| 33 | Regex advanced + Promises | Greedy/lazy; groups; Promise creation; chaining; basic error propagation | J,J,J,J |
| 34 | React components & props | Function vs class components (both shown); PropTypes; default props | R,R,R,R |
| 35 | State & lifecycle | `setState` / hooks equivalents; mount/update/unmount mental model; effects at high level | R,R,R,R |
| 36 | Composition & children | `props.children`; lifting state; decomposition exercise | R,R,R,R |
| 37 | Forms in React | Controlled vs uncontrolled; validation UX | R,R,R,R |
| 38 | Virtual DOM & keys + HOC intro | Reconciliation concept; list keys; HOC pattern motivation | R,R,R,R |
| 39 | Redux core | Actions, reducers, store; immutability; DevTools optional | R,R,R,R |
| 40 | Redux side effects + integration | Async action patterns (thunk or RTK slice async—pick one repo-wide); small feature integration | R,R,R,R |
| 41 | Node runtime & event loop | Modules; `fs`/`path` light; event loop blocking demo; timers | N,N,N,N |
| 42 | Express foundation | Routing; request/response; middleware pipeline; error middleware | N,N,N,N |
| 43 | JWT authentication | Sign/verify; middleware protecting routes; 401 handling | N,N,N,N |
| 44 | MongoDB connection & persistence | Official driver or Mongoose (consistent); CRUD; validation | N,N,N,N |
| 45 | Capstone API | Combines Express + auth + DB; practical “feature slice” | N,N,N,N |

### F.1 Notes on the map (read before deviating)

- **React lifecycle:** split across Days **35** and **38** intentionally (class + hooks framing).
- **Redux:** concentrated Days **39–40**; earlier React days stay Redux-free to reduce cognitive load.
- **Node segment** is compressed; Days **41–45** should use **progressive** tasks where later tasks extend the same small codebase where possible.
- If a cohort needs **more** Node time, the instructor may swap **Day 40** partial review or compress **Day 16**—but must preserve topic coverage somewhere.

---

## Part G — “AI agent grader” prompt fragments (optional but recommended)

In `EVALUATION_CRITERIA.md`, include a boxed section:

```markdown
## AI grading prompt (paste into your grader)
You are evaluating a graduate-level assignment. Use only observable criteria below.
Repository context: ...
Candidate changed files: ...
Rubric: ...
Return: Pass/Fail, score table, blocking issues, non-blocking suggestions.
```

Keep it **short**; the rubric remains authoritative.

---

## Part H — Final completeness checklist (course-wide)

Before declaring the **entire** 45-day generation complete:

- [ ] Every topic in `01` Section 2 appears in **some** day’s theory headings (grep-able).
- [ ] Each day has **theory + 3–4 tasks**.
- [ ] Each JS task has **tests** + documented commands.
- [ ] Each React/Node task has **EVALUATION_CRITERIA.md** with weighted rubric.
- [ ] (Optional) Instructor numeric grading uses **`Day XX/INSTRUCTOR_GRADING_1-100.md`** (day-level) plus **`05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md`** (see Days **01–08** reference rollout).
- [ ] Root `.gitignore` + root `README.md` exist per `02`.
- [ ] No `node_modules` committed.

---

## Part I — Changelog

| Version | Date | Notes |
|---------|------|-------|
| `1.0.2` | 2026-06-04 | Day-level `Day XX/INSTRUCTOR_GRADING_1-100.md` (not per-task). |
| `1.0.1` | 2026-06-04 | Reference optional `INSTRUCTOR_GRADING_1-100.md` + guide `05-…` for instructor/AI numeric rubrics. |
| `1.0.0` | 2026-06-03 | Initial map + authoring guide. |
