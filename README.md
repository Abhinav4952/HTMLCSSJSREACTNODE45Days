# 45-Day Web Foundations Course (HTML, CSS, JavaScript, React, Node)

This repository contains **45 days** of graduate-level course material: consolidated theory in each `Day XX` folder and hands-on work under `practical-tasks/`. **Current in-repo coverage:** Days **01–45** are authored here, plus **three full-stack capstone projects** after Day 45. Days **01–16** emphasize HTML and CSS; **17–33** focus on JavaScript with automated tests where noted; **34–38** introduce **React** with per-task **Vite** apps (manual/rubric grading); **39–40** add **Redux Toolkit + `react-redux`** in the same per-task Vite pattern; **41–45** cover **Node.js 18+ (ESM)**, **Express**, **JWT**, and **MongoDB via Mongoose**. Capstones combine React + Express + MongoDB Atlas into portfolio-style apps.

Day **06** includes one **Vitest** task (`Day 06/practical-tasks/task-04-css-length-math-lab/`) with a committed `package-lock.json` and a task-local `.npmrc` pointing at the public npm registry (useful if your machine defaults to a private registry mirror). **Days 11 and 17–33** use the same Vitest + `package-lock.json` + task-local `.npmrc` pattern for JavaScript exercises. **Days 34–40** use the same **`package-lock.json` + `.npmrc` per task folder** pattern for **Vite** exercises (`npm install` → `npm run dev`, optional `npm run build`). React days **34–38** are Redux-free; **39–40** add **`@reduxjs/toolkit`** and **`react-redux`**. **Days 41–45** use **`package-lock.json` + `.npmrc` per task folder** for **Node / Express / JWT / Mongoose** work (`npm install` → `npm test` and/or `npm start` / `npm run dev` as documented per task).

## How to work day by day

1. Open `Day 01`, then `Day 02`, and so on in order (unless your instructor assigns a different path).
2. In each day folder, read `README.md` for objectives and the task table.
3. Read `DAY-XX-THEORY-AND-REFERENCE.md` before starting tasks.
4. Complete tasks in `practical-tasks/task-01-...` through `task-04-...` in order unless your instructor says otherwise.
5. Edit only files marked with `TODO` comments (HTML/CSS use `<!-- TODO(DayXX-taskYY): ... -->`; JavaScript uses `// TODO(DayXX-taskYY): ...`; JSX may use `{/* TODO(DayXX-taskYY): ... */}`). Do not change `TASK_INSTRUCTIONS.md`, `EVALUATION_CRITERIA.md`, or autograder test files unless a task explicitly allows it.

## Install, run, and verify by task type

| Type | Typical verification |
|------|----------------------|
| **HTML / CSS** | Open `index.html` in a modern browser, or run `npx serve .` from the task folder and visit the URL shown in the terminal. Follow the manual checklist in `TASK_INSTRUCTIONS.md`. |
| **JavaScript (with tests)** | From the task folder: `npm install` then `npm test`. Tests are expected to fail until you complete the `TODO`s. |
| **React (Vite)** | `npm install`, then `npm run dev`. Use `EVALUATION_CRITERIA.md` for self-review before submission. Optional: `npm run build` for a compile check. |
| **Node / Express / JWT / Mongoose** | `npm install`, then `npm test` and/or `npm start` as documented in each task’s `TASK_INSTRUCTIONS.md`. Use the rubric in `EVALUATION_CRITERIA.md`. |

This cohort uses **`npm`** with a committed **`package-lock.json`** inside JavaScript/React/Node task folders. Do not commit `node_modules/`.

## Git workflow (recommended)

1. `git clone <repo-url>`
2. `cd` into the repository.
3. **Branching policy (default for this cohort):** create a personal branch such as `student/<your-id>/main`, or per-day branches like `student/<your-id>/day-07` if your instructor prefers that model—confirm with your instructor.
4. **Daily loop:** `git pull` → complete `TODO`s → run verification steps from the task instructions → `git add` only files you intentionally changed → `git commit -m "Day 07: complete task-02 …"` → `git push`.

## How evaluation works

- **JavaScript tasks:** `npm test` is a primary correctness signal; instructors may still review style and structure.
- **HTML, CSS, React, and Node tasks:** grading follows `EVALUATION_CRITERIA.md` (human or AI-assisted). Meet the pass/fail gates and observable rubric items.

## Getting help

Use your instructor’s office hours, class forum, or agreed chat channel. When stuck, consult official docs linked from each day’s theory file (MDN, React, Node.js).

## Capstone projects (after Day 45)

After finishing Days **01–45**, complete these three major full-stack projects (React + Express + MongoDB). Each folder has a runnable boilerplate, detailed instructions, a MongoDB data model guide, UI mockups, and grading criteria.

| Project | Folder | State management | Backend port |
|---------|--------|------------------|--------------|
| E-commerce Store (ShopLite) | [`Project 01 - E-commerce Store/`](Project%2001%20-%20E-commerce%20Store/) | Redux Toolkit | `5001` |
| Blog CMS (InkBoard) | [`Project 02 - Blog CMS/`](Project%2002%20-%20Blog%20CMS/) | React Context | `5002` |
| Library Management (ShelfKeep) | [`Project 03 - Library Management/`](Project%2003%20-%20Library%20Management/) | Redux Toolkit | `5003` |

**Start here for each project:** that folder’s `README.md` (set `MONGO_URI` in `backend/.env` from `.env.example`), then `PROJECT_INSTRUCTIONS.md`, `DATA_MODEL.md`, and `GRADING_CRITERIA.md`. Mockups are under `docs/mockups/`.

Quick start pattern:

```bash
cd "Project 01 - E-commerce Store/backend"
cp .env.example .env   # then paste your Atlas connection string into MONGO_URI
npm install && npm run dev

# second terminal
cd "Project 01 - E-commerce Store/frontend"
npm install && npm run dev
```

The Home page already calls `GET /api/welcome` so you can confirm FE ↔ BE integration once MongoDB connects.

## Repository layout

```text
/
  course-generation-instructions/   # Specs for authors and agents (read-only for most candidates)
  Day 01/ … Day 45/
  Project 01 - E-commerce Store/    # Capstone (React + Node + MongoDB)
  Project 02 - Blog CMS/
  Project 03 - Library Management/
  .gitignore
  README.md                         # This file
```
