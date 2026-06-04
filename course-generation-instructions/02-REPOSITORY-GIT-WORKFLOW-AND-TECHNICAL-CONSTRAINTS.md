# 02 — Repository, Git Workflow, and Technical Constraints

**Instruction set version:** `1.0.0`

This document defines **how the repository is organized for candidates**, **what must never be committed**, **how JavaScript tasks are verified with tests**, and **baseline tooling** so multiple AI agents produce compatible output.

---

## 1. Repository layout (target end state)

The **repository root** (after all days are generated) should look conceptually like this:

```text
/
  course-generation-instructions/     # Instructor + AI agent specs (this folder)
  Day 01/
  Day 02/
  ...
  Day 45/
  .gitignore
  README.md                          # Candidate-facing: how to pull, install, run tests, submit work
```

**Naming convention for day folders:** `Day 01`, `Day 02`, … `Day 45` (two-digit zero padding, English label `Day`, space before number). **Do not** use `day-1`, `Day1`, or `day_01` unless the instructor explicitly changes this standard.

---

## 2. Git workflow for candidates (must be documented in root `README.md`)

When day folders exist, the root `README.md` (candidate-facing) must explain:

### 2.1 Clone and branch (recommended)

1. `git clone <repo-url>`
2. `cd <repo>`
3. Optional but recommended: create a personal branch `student/<name-or-id>/main` or per-day branches `student/<id>/day-07`—the instructor chooses the policy; **document the chosen policy** in the root README.

### 2.2 Daily work loop

1. `git pull` (get latest tasks or fixes from instructor).
2. Complete `TODO`s inside the task folder for that day.
3. Run verification steps in `TASK_INSTRUCTIONS.md` (tests, dev server, lint if configured).
4. `git add` only the files the candidate changed (avoid accidental `node_modules`).
5. `git commit` with a clear message, e.g. `Day 07: complete task-02 form validation`.
6. `git push` to the remote branch.

### 2.3 Instructor evaluation loop

1. `git pull` candidate branch.
2. For **JavaScript** tasks: run `npm install` (if needed) and `npm test` (or the documented command).
3. For **React** and **Node** tasks: follow `EVALUATION_CRITERIA.md` and optionally use an AI agent with that file as a rubric.

### 2.4 Conflict avoidance rules

- Candidates should **not** edit `TASK_INSTRUCTIONS.md`, `EVALUATION_CRITERIA.md`, or the autograder test files **unless** the task explicitly says they may (default: **read-only**).
- Candidates **should** edit only files containing `TODO` markers (and small glue files if the task says so).

If a task requires editing tests (rare), state it explicitly in **bold** in `TASK_INSTRUCTIONS.md`.

---

## 3. `.gitignore` (required at repository root)

Agents generating the full course must create a root `.gitignore` that includes at minimum:

```gitignore
# Dependencies
node_modules/

# Logs and caches
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
.npm
.eslintcache

# Environment files (never commit secrets)
.env
.env.*.local

# OS / editor
.DS_Store
Thumbs.db
.idea/
.vscode/*
!.vscode/extensions.json

# Build output (add more per stack if needed)
dist/
build/
coverage/
.next/
out/

# Optional: lockfiles — see Section 5
```

**Instructor note:** If you want lockfiles committed for reproducibility, remove the lockfile lines **only** after choosing `npm` vs `pnpm` vs `yarn` for the whole cohort.

---

## 4. `node_modules` policy (strict)

- **Never** commit `node_modules/`.
- Every Node/React/JavaScript task that uses npm packages must include a correct **`package.json`** at the task root (the folder that contains the candidate’s `npm install`).
- **Agents must verify** `package.json` has:

  - Correct `name`, `version`, `private: true` (recommended for learning repos)
  - `scripts` for `test`, `start` or `dev` as applicable
  - All runtime + dev dependencies needed for tests and local runs

### 4.1 After `npm install`, these commands must succeed

| Task type | Minimum success criteria |
|-----------|---------------------------|
| Vanilla JS + unit tests | `npm test` runs and fails until TODOs are correctly implemented (TDD-friendly) |
| React (Vite or CRA-style—pick one for consistency) | `npm run dev` starts; `npm run build` optional but recommended |
| Node + Express | `npm start` or `npm run dev` starts server; optional `npm test` for supertest-based checks |

---

## 5. Package manager and lockfiles

**Default recommendation:** `npm` with **committed** `package-lock.json` for reproducible installs in a classroom.

**Alternative:** no lockfile committed; simpler diffs but less reproducibility—if chosen, state that in the root README.

**Agent rule:** Pick **one** policy for the entire repo and **do not mix** `package-lock.json` and `yarn.lock`.

---

## 6. JavaScript unit testing standard (for autograded tasks)

To keep grading uniform across agents, use **one** primary test stack for vanilla JS / Node logic tasks:

### 6.1 Default stack

- **Test runner:** `vitest` **or** `node:test` (Node 18+) — pick **one** for the repo and reuse everywhere.
- **Assertion library:** bundled with the runner.
- **For HTTP:** `supertest` (optional; use when testing Express routes).

### 6.2 Where tests live

- Prefer `tests/` or `__tests__/` at the task root.
- **Do not** scatter tests inside `src/` unless there is a strong reason; consistency matters more.

### 6.3 What tests should assert

- **Public behavior**, not private implementation details, unless the learning goal is explicitly about an internal pattern.
- **Edge cases** called out in `TASK_INSTRUCTIONS.md`.

### 6.4 Red–green workflow

Boilerplate should **run** with tests **failing** (red) because of `TODO` stubs, then pass (green) when the candidate completes work—**unless** the pedagogical goal requires tests to pass initially (say so explicitly if so).

---

## 7. React boilerplate standard

Pick **one** toolchain for all React tasks, e.g.:

- **Vite + React** (recommended: fast, modern), **or**
- **Create React App** (only if legacy compatibility is required).

**Agent rules:**

- Use consistent folder layout across days (`src/`, `public/`, etc.).
- Keep dependencies minimal; add libraries only when taught (e.g. do not add Redux on Day 1 of React).
- Include **scripts:** `dev`, `build`, `preview` (Vite) or equivalent.

---

## 8. Node / Express boilerplate standard

- Use **ESM** (`"type": "module"`) **or** CommonJS—pick **one** for all Node tasks and stay consistent.
- Separate **app** creation from **server listen** when using `supertest` (export `app`).

**Environment variables:**

- Provide `.env.example` with dummy values, e.g. `JWT_SECRET=change-me-in-dev`
- Load with `dotenv` in dev only if used; document in instructions.

**MongoDB:**

- For local dev, document using Docker or Atlas; never require a paid tier.
- Connection string via environment variable only.

---

## 9. HTML/CSS-only tasks

Some tasks may be **static HTML + CSS** with no bundler.

**Requirements:**

- Include a `README.md` or rely on `TASK_INSTRUCTIONS.md` to say: “Open `index.html` in a browser” **or** “Run `npx serve .`”.
- If using a static server, prefer documenting `npx serve` rather than adding a `package.json`—but either is acceptable if consistent.

---

## 10. Code style and linting (optional but recommended)

If ESLint is included:

- Keep config **minimal** to avoid frustrating beginners.
- Document `npm run lint` in task instructions when present.

---

## 11. Security checklist for agents (mandatory review before merge)

- [ ] No real credentials, tokens, or connection strings in the repo.
- [ ] `.env` is gitignored; `.env.example` contains placeholders only.
- [ ] JWT tasks use **strong enough** dev secrets only in docs, not hard-coded in source.
- [ ] Dependencies are pinned reasonably; no known-critical versions without a note.

---

## 12. Root `README.md` (candidate-facing) — required sections

When the course is generated, the root `README.md` must include:

1. **Purpose of the repo** and the 45-day structure.
2. **How to work day by day** (folder navigation).
3. **Install/run/test** conventions per stack (JS vs React vs Node).
4. **Git workflow** (pull / branch / commit / push).
5. **How evaluation works** (tests vs rubric).
6. **Getting help** policy (instructor office hours, forum, etc.—placeholder text OK).

---

## 13. Handoff note for AI agents

Before generating any `Day XX` folder, re-read:

- This file (`02`) for **constraints**
- `03` for **structure**
- `04` for **templates and schedule**

If any instruction conflicts, follow this precedence:

1. Security constraints in `02`
2. Folder structure in `03`
3. Schedule in `04`
4. Pedagogical goals in `01`

If `01` and `04` disagree on scheduling, **stop** and ask the human instructor—do not silently drop topics.
