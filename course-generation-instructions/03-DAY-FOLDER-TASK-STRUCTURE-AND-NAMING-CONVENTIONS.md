# 03 — Day Folder, Task Structure, and Naming Conventions

**Instruction set version:** `1.0.0`

This document is the **mechanical specification** for directory trees, filenames, and the required contents of Markdown and boilerplate files. Follow it **verbatim** unless the instructor publishes an amendment.

---

## 1. Day folder name and placement

- **Path:** `/Day XX/` at repository root, where `XX` is `01`–`45`.
- **Case:** Capital `D` in `Day`, space, two-digit number.
- **Forbidden variants:** `Day-01`, `day01`, `Week1/Day1` (unless instructor changes global policy).

---

## 2. Inside each `Day XX/` folder

Each day **must** contain:

```text
Day XX/
  README.md                         # Short index for the day (see Section 3)
  DAY-XX-THEORY-AND-REFERENCE.md    # Single consolidated theory file for that day (see Section 4)
  practical-tasks/
    task-01-<short-slug>/
      TASK_INSTRUCTIONS.md
      EVALUATION_CRITERIA.md
      ... boilerplate files + TODOs ...
    task-02-<short-slug>/
      ...
    task-03-<short-slug>/
      ...
    task-04-<short-slug>/           # Optional fourth task; minimum is 3 tasks
      ...
```

### 2.1 Task count

- **Minimum:** 3 tasks per day.
- **Target:** 4 tasks per day.
- **Maximum:** 4 tasks unless the instructor approves an exception (avoid overwhelming learners).

### 2.2 Task folder naming

Pattern:

```text
task-<two-digit-index>-<kebab-case-slug>/
```

Examples:

- `task-01-semantic-page-shell`
- `task-02-form-accessibility`
- `task-03-flexbox-dashboard-layout`

**Slug rules:**

- Lowercase, kebab-case, only letters, digits, hyphens.
- No spaces, no underscores (underscores allowed only if instructor overrides).

---

## 3. `Day XX/README.md` (day index file)

Purpose: **fast orientation** for the candidate. Keep it **1–2 screens** maximum.

### Required sections

1. **Day title** (H1): e.g. `Day 07 — Flexbox and Responsive Layout`
2. **Learning objectives** (bullet list, 4–7 bullets) — must align with theory file headings.
3. **Prerequisites** (bullets) — which prior days/topics to review if shaky.
4. **How to use this folder**
   - Read `DAY-XX-THEORY-AND-REFERENCE.md` first.
   - Then complete tasks in `practical-tasks/` in order unless noted.
5. **Task list** (table)

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-...` | HTML/CSS | Open in browser / screenshot checklist |
| 2 | `task-02-...` | JavaScript | `npm install` → `npm test` |
| 3 | `task-03-...` | React | `npm install` → `npm run dev` + rubric |
| 4 | `task-04-...` | Node | `npm install` → `npm run dev` + rubric |

**Agent note:** Not every day includes all stacks; the table must reflect **actual** tasks.

---

## 4. `DAY-XX-THEORY-AND-REFERENCE.md` (single theory file per day)

### 4.1 Filename

- Pattern: `DAY-XX-THEORY-AND-REFERENCE.md` with the same `XX` as the parent folder.

### 4.2 Top matter (required)

At the top of the file, include YAML-like metadata in Markdown (not strict YAML required, but keep keys consistent):

```markdown
# Day XX — <Short Title>

**Primary theme:** <one line>  
**Estimated study time:** <e.g. 2–4 hours theory + 3–6 hours tasks>  
**Related tasks:** `task-01-...`, `task-02-...`, ...  
**Instruction alignment:** Maps to topics <list> from the master topic list.
```

### 4.3 Structure for the whole document

1. **Overview** — narrative explanation of what the learner will gain and how it connects to real projects.
2. **Day roadmap** — numbered list of sections in reading order.
3. **Sections per subtopic** — repeat the template in Section 4.4 for **each** subtopic taught that day.
4. **Common mistakes & debugging** — bullets grounded in the day’s content.
5. **Further reading** — MDN / React docs / Node docs links (official preferred).
6. **Glossary** — terms introduced that day.

### 4.4 Required template **per subtopic**

For **each** subtopic heading `### <Subtopic name>`, include **all** of the following subsections (headings can be `####`):

#### 4.4.1 `#### What it is`

Clear definition in plain language; include a **mental model** or analogy where helpful.

#### 4.4.2 `#### Why it exists / why it matters`

Motivate with **real engineering problems** (layout bugs, state bugs, security issues, performance footguns).

#### 4.4.3 `#### Pros and cons`

- **Pros:** at least 3 bullets when meaningful (fewer OK for trivial topics if explained).
- **Cons / tradeoffs:** at least 2 bullets (e.g. complexity, browser support historically, footguns).

#### 4.4.4 `#### What happens without it / when misused**

Concrete failure modes: broken layout, inaccessible forms, memory leaks, insecure auth, race conditions, etc.

#### 4.4.5 `#### Syntax and rules`

- Show the **canonical syntax patterns**.
- Call out **gotchas** (e.g. margin collapse, `this` binding, stale closures, middleware order).

#### 4.4.6 `#### Examples`

Provide **3–5 examples** per **major** subtopic:

- At least **two** should be **tiny** (5–20 lines).
- At least **one** should be **medium** (a small cohesive snippet or multi-file reference clearly labeled).
- Examples must be **copy-paste safe** where possible, or note required context (`// assumes ...`).

#### 4.4.7 `#### Quick checks (self-test questions)`

3–5 questions **without** answers in the same subsection (answers can appear in an `#### Answers` subsection at the **end of the day doc** to encourage thinking).

---

## 5. `practical-tasks/` conventions

### 5.1 Ordering

- Prefix with `task-01`, `task-02`, … to enforce order.
- Tasks should generally **increase in difficulty** and **combine** skills toward the last task.

### 5.2 Each task folder — required files

Every task folder **must** contain:

1. `TASK_INSTRUCTIONS.md` — **detailed** brief for the candidate.
2. `EVALUATION_CRITERIA.md` — rubric for instructor or AI agent.
3. Boilerplate code with **`TODO`** markers for required work.

**Optional but welcome:**

- `README.md` inside the task (only if it adds clarity beyond `TASK_INSTRUCTIONS.md`; avoid duplication).
- `INSTRUCTOR_GRADING_1-100.md` — **optional instructor/AI-only** numeric rubric. **Recommended placement:** one file per **day** at **`Day XX/INSTRUCTOR_GRADING_1-100.md`** (not inside each `task-*` folder). See `course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md` and `scripts/emit-instructor-grading-days-01-08.mjs` for the Days **01–08** reference pattern. Keep **candidate-facing** grading in each task’s `EVALUATION_CRITERIA.md`.

---

## 6. `TASK_INSTRUCTIONS.md` template (required headings)

Use this skeleton (adapt content per task):

```markdown
# Task <index> — <Human-readable title>

## Summary
<2–4 sentences>

## Learning goals
- ...
- ...

## Provided files
List each important file and its purpose.

## Prerequisites
- ...

## What you will implement
Numbered list of **observable outcomes**.

## Constraints
- Do / Do not ...
- Browser / Node version assumptions ...

## Step-by-step guidance
1. ...
2. ...

## How to run and verify

### Install dependencies
`<exact commands>`

### Run tests (JavaScript / Node logic tasks)
`<exact commands>`

### Run the app (React / Node server tasks)
`<exact commands>`

### Manual checks (all tasks)
Checklist the candidate can follow without instructor.

## `TODO` map
Table mapping each `TODO:` comment location → what “done” means.

## Submission checklist (Git)
- [ ] Only intentional files changed
- [ ] Tests pass locally (if applicable)
- [ ] No secrets committed

## Hints (optional collapsible section)
Use `<details><summary>...</summary>...</details>` in Markdown for progressive disclosure.
```

### 6.1 `TODO` comment format in code

Use a **consistent** tag across the repo:

```text
// TODO(DayXX-taskYY): <instruction>
```

or for multi-line:

```text
/* TODO(Day07-task02):
 * Implement ...
 */
```

**Rules:**

- `TODO` text must be **actionable** (“Implement validation for email field”) not vague (“Finish function”).
- Prefer **one TODO per missing behavior** when practical (easier grading).

---

## 7. `EVALUATION_CRITERIA.md` template (required headings)

```markdown
# Evaluation Criteria — Day XX — Task YY — <title>

## Scope
What is being graded vs explicitly out of scope.

## Weighting (100 points unless instructor overrides)
| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 40 | ... |
| Code quality | 20 | ... |
| Requirements coverage | 25 | ... |
| Docs / readability | 15 | ... |

## Pass / fail gates (automatic fail if violated)
- e.g. “Tests must pass”, “No hard-coded secrets”, “Must use flexbox not tables for layout” ...

## Detailed rubric
### Correctness
- ...

### Edge cases
- ...

### Security / privacy (if applicable)
- ...

### UX / accessibility (if applicable)
- ...

## Evidence the grader should collect
- Commands run + output snippets
- Screenshots required (if any)

## AI-assisted grading prompt (optional)
Short block of text the instructor can paste into an AI grader with the candidate’s diff.
```

### 7.1 JavaScript tasks with tests

- Rubric should reference **`npm test`** as a primary correctness signal.
- Still include **manual** criteria (readability, structure) because tests can be gamed.

### 7.2 React / Node tasks without autograder

- Rubric must be **observable** and **file-scoped** (“`src/components/Header.jsx` exports …”).
- Avoid subjective-only criteria; pair them with concrete indicators.

---

## 8. Boilerplate code rules (all tasks)

1. **Runs after install** — no missing files, no broken imports.
2. **Failing tests allowed** — expected red state for JS until TODOs are done; document this in instructions.
3. **No secrets** — use `.env.example` only.
4. **Minimal surface** — do not dump unrelated starter features.
5. **Cross-platform paths** — avoid OS-specific assumptions in scripts when possible.

---

## 9. Asset and binary files

- Prefer **SVG** or small PNGs if images are needed.
- If large binaries are unavoidable, document them and consider Git LFS policy in instructor README (outside scope of per-day tasks unless requested).

---

## 10. Consistency checklist (agents run before declaring a day “complete”)

- [ ] Folder name matches `DAY-XX-THEORY-AND-REFERENCE.md` number
- [ ] Day `README.md` lists all tasks correctly
- [ ] Each task has **both** MD files
- [ ] Each `TODO` appears in the `TODO map` in `TASK_INSTRUCTIONS.md`
- [ ] `package.json` exists for JS/React/Node tasks and scripts are correct
- [ ] `.gitignore` at repo root covers `node_modules` (do not add nested `node_modules` to Git)

---

## 11. Example minimal tree (HTML/CSS only task)

```text
task-01-markup-wireframe/
  TASK_INSTRUCTIONS.md
  EVALUATION_CRITERIA.md
  index.html
  styles/
    main.css
  assets/
    README.md        # optional note about images
```

---

## 12. Example minimal tree (JavaScript with tests)

```text
task-02-array-transforms/
  TASK_INSTRUCTIONS.md
  EVALUATION_CRITERIA.md
  package.json
  src/
    arraysLab.js     # contains TODOs
  tests/
    arraysLab.test.js
```

---

## 13. Example minimal tree (React)

```text
task-03-controlled-form/
  TASK_INSTRUCTIONS.md
  EVALUATION_CRITERIA.md
  package.json
  vite.config.js
  index.html
  src/
    main.jsx
    App.jsx          # TODOs here or in components/
    components/
      Form.jsx       # TODOs
```

---

## 14. Example minimal tree (Express + Mongo + JWT)

```text
task-04-auth-middleware/
  TASK_INSTRUCTIONS.md
  EVALUATION_CRITERIA.md
  package.json
  src/
    app.js
    server.js
    routes/
      auth.js        # TODOs
    middleware/
      auth.js        # TODOs
  .env.example
```

---

## 15. Handoff note for AI agents

Treat this file as a **lintable spec**. If something is unclear, prefer **more explicit** `TASK_INSTRUCTIONS.md` text over assumptions.
