# 01 — Course Context, Learning Outcomes, and Agent Mandate

**Instruction set version:** `1.0.0`

This document defines **who** the course is for, **what** “done” means for each topic, and **non-negotiable rules** for any AI agent (or human author) that generates day-wise folders.

---

## 1. Audience and assumed prior training

### 1.1 Learner profile

- **Level:** Graduate student who has completed **two years** of study.
- **Declared baseline:** Already trained in **HTML, CSS, JavaScript, React**, and **Node.js / Express** API development.
- **Reality check:** Treat the baseline as *exposure*, not *mastery*. The 45-day plan must **reinforce fundamentals**, **close gaps**, and **force deliberate practice** so the learner can work **without constant supervision** on typical small-to-medium tasks.

### 1.2 What this course is optimizing for

1. **Retention through spaced repetition:** Revisit core ideas (box model, closures, React state, Express middleware) on later days in new contexts.
2. **Transfer:** Every day must connect theory to **hands-on** work in `practical-tasks/`.
3. **Self-assessment where possible:** JavaScript tasks must include **automated tests** the candidate can run locally.
4. **Instructor / AI-assisted grading where needed:** React and Node tasks rely on **documented evaluation criteria** and manual review (including review by an AI agent operated by the instructor).

---

## 2. Topic inventory (authoritative list)

Agents must ensure **every bullet** below appears in **at least one day’s theory** and is **practiced** in at least one task **before** the course ends. Some bullets intentionally overlap (e.g. “Responsive design” appears under CSS intermediate and advanced); **do not treat overlap as optional**—use later days to deepen the same theme with harder exercises.

### 2.1 HTML + CSS (layout coding)

**Basics**

- Basic HTML page structure
- Document Type Definition; HTML vs XHTML (conceptual and practical differences that still matter)
- Metadata, styles, scripts (`<meta>`, `<link>`, `<script>`, defer/async at conceptual level where appropriate)
- Text formatting tags and CSS text formatting
- Tables
- Forms and input tags
- CSS rules and selectors
- CSS decoration: border, background, `text-decoration`, `text-transform`
- Box and text shadow
- CSS units

**Intermediate**

- HTML5 tags
- HTML5 input types
- CSS standards and the **box model**
- **Positioning**
- Markup layout patterns
- `display` property (block/inline/inline-block, etc.)
- Pseudo-classes (`:first-child`, `:last-child`, etc.)
- Pseudo-elements (`::before`, `::after`, etc.)
- Cascading and inheritance
- Responsive design (first pass)
- Opacity

**Advanced**

- Attribute selectors (`^=`, `$=`, `*=`, etc.)
- CSS3 **transform**, **transition**, **animation** (include `resize` where pedagogically useful)
- **Flexible Box Model** (Flexbox)
- **Media queries**
- Responsive design (second pass / advanced patterns)

### 2.2 JavaScript

**Core — Basic**

- Variables, values, types: number, string, boolean, object, `null`, `undefined`
- Expressions, operators, statements; literals; conditions; loops
- Objects: create, manage properties, built-in methods, hash/map mental model, property descriptors (introduce descriptors at least at conceptual + simple example level)
- Arrays: create, indexes, length, modification; built-in methods including sort, filter, search, iteration patterns
- Functions: create and invoke
- ES2015 basics: `const`/`let`, arrow functions, default parameters, spread, destructuring, template literals, `for..of`

**Core — Intermediate**

- Advanced expressions: hoisting, automatic type conversions, comparisons (`==` vs `===`, edge cases)
- Advanced functions: `arguments`, `this`, scope, `call`/`apply`/`bind`
- Functional patterns: IIFE, callbacks, memoization, chaining, currying, binding patterns
- Closures: nested functions, lexical environment, inner vs outer context
- OOP: constructors; public/private/static (use idiomatic JS patterns; clarify language limitations vs conventions)
- Prototypal inheritance: prototypes, constructor patterns, `instanceof`
- ES2015 classes and inheritance
- Regular expressions — basics: methods, flags, metacharacters, quantifiers
- ES2015 intermediate: `Object.keys`/`values`, computed properties, getters/setters, `Symbol`, `Set`, `Map`, `WeakSet`, `WeakMap`

**Core — Advanced**

- Strict mode: activation, limitations, practical benefits
- Regular expressions — advanced: greedy vs lazy, ranges, grouping
- Errors: `try`/`catch`/`finally`, `throw`, `Error`, custom errors
- Promises (ES2015)

### 2.3 React

**Basics**

- Component definition (ES5 and ES2015 syntax where still relevant; prefer modern patterns but **show both** class and function components at least once in the course)
- Props: PropTypes, default props
- State: initial state, `setState`, stateful vs stateless
- Lifecycle: mount/update/unmount; reacting to state/prop changes (class lifecycle **and** hooks-based equivalents must both be covered across the React days)
- Composition: `props.children`, composition vs inheritance, lifting state up, decomposition exercises
- Forms: controlled vs uncontrolled
- Virtual DOM: concept and **keys**

**Intermediate**

- Higher-Order Components (HOCs)
- Redux: three principles, actions, reducers, store, side effects (e.g. async patterns / thunks or RTK Query at introductory level—pick **one** consistent approach per task set and document it)

### 2.4 Node.js / Express ecosystem

- Node.js runtime concepts including the **event loop** (at a level sufficient to debug slow handlers and blocking code)
- Express: routing, request/response, middleware pipeline
- JWT-based auth (concepts + secure-ish defaults; never commit real secrets)
- MongoDB connection (official driver or Mongoose—**pick one** for the whole Node segment and stay consistent)

---

## 3. Proficiency model (what “learned” means)

For **each** topic taught on a given day, the learner should reach **both** levels below by the end of that day’s work (theory + tasks).

### 3.1 Level A — Theoretical + guided

- Can explain **what** it is and **why** it exists.
- Can trace **what breaks** when it is missing or misused.
- Can read and explain **small** code samples.
- Can complete **simple** exercises with hints.

### 3.2 Level B — Independent “normal” tasks

- Can implement **typical** assignments without step-by-step supervision.
- Can debug **common** mistakes (syntax, wrong selector, wrong state update, wrong middleware order, etc.).
- Knows **where to look** (MDN, React docs, Node docs) when stuck.

**Agent instruction:** Practical tasks must be designed so that **Task 1** leans Level A, **Tasks 2–3** target Level B, and **Task 4** (when present) is a **stretch** that combines the day’s topic with prior days.

---

## 4. Pedagogical rules for content generation

### 4.1 One primary theme per day (with explicit subtopics)

Each `Day XX` folder should have **one primary theme** (e.g. “Flexbox layout”) and a **bounded** list of subtopics. Avoid “kitchen sink” days unless labeled **Review / integration**.

### 4.2 Spiral curriculum

Reintroduce earlier ideas in harder tasks:

- Box model → later layout → responsive → full page mock
- Functions → closures → async → Promises → fetch in Node/React
- Express middleware → auth → DB

### 4.3 Honesty about security and production

Especially for JWT, CORS, cookies, and Mongo:

- Teach **threat awareness** (leaked secrets, token storage pitfalls) at a basic level.
- Never embed real API keys; use `.env.example` only.

### 4.4 Accessibility and semantics (minimum bar)

Even if not a separate bullet in the user’s list, agents should **mention** semantic HTML and basic accessibility (labels for inputs, button types, heading order) wherever forms and layout are taught.

### 4.5 Remove duplication in the *source requirement list* only for writing clarity

The user’s original list repeats “Basic HTML Page Structure” twice. **Deliver one consolidated treatment** in the schedule, not two identical days.

---

## 5. Agent mandate (non-negotiable deliverables)

Any agent generating `Day XX` content **must**:

1. **Create the exact folder structure** specified in `03-DAY-FOLDER-TASK-STRUCTURE-AND-NAMING-CONVENTIONS.md`.
2. **Cover every topic** in Section 2 of this document across the 45 days per the schedule in `04` (unless the instructor publishes an updated schedule).
3. **Write theory** in Markdown with the required sections per topic (see `04`).
4. **Ship 3–4 practical tasks per day** under `practical-tasks/`, each in its own subfolder.
5. **Provide runnable boilerplate** with `TODO` markers for candidate work; **no** committed `node_modules/`.
6. **JavaScript tasks:** include **unit tests** and scripts documented in `TASK_INSTRUCTIONS.md`.
7. **React / Node tasks:** include **EVALUATION_CRITERIA.md** suitable for human or AI grading.
8. **Validate locally** (when tools allow): `npm install` + `npm test` / `npm run dev` as applicable for each task before declaring the task “done.”

---

## 6. Quality bar and rejection criteria

Reject (revise) a generated day if any of the following are true:

- Theory file has **no examples** or fewer than **three** runnable/illustrative examples per major subtopic.
- Tasks **do not** reference the day’s learning objectives explicitly.
- Boilerplate **does not run** after `npm install` (for JS/React/Node tasks).
- JavaScript tasks lack tests **or** tests do not map to requirements in `TASK_INSTRUCTIONS.md`.
- Evaluation criteria are vague (“code should be good”) instead of **observable checkpoints**.
- Secrets or real credentials appear in the repo.

---

## 7. Changelog

| Version | Date | Notes |
|---------|------|-------|
| `1.0.0` | 2026-06-03 | Initial instruction set. |
