# Course Material Generation — Instructions Index

This folder contains **authoritative specifications** for generating a **45-day**, graduate-level, hands-on course in **HTML, CSS, JavaScript, React**, and **Node.js / Express** (including APIs, middleware, JWT, and MongoDB).

These documents are written for **human instructors** and for **AI coding agents** that will create `Day 01` … `Day 45` folders in a later phase.

## How to use this folder

1. Read the files **in numerical order** (`01` → `04`).
2. Do **not** skip `02` (Git and technical constraints) or `03` (folder structure); agents that skip them produce inconsistent repositories.
3. When generating day content, treat **`04`’s topic map as the default schedule** unless the instructor explicitly overrides it.

## Files in this set

| File | Purpose |
|------|---------|
| [`01-COURSE-CONTEXT-LEARNING-OUTCOMES-AND-AGENT-MANDATE.md`](./01-COURSE-CONTEXT-LEARNING-OUTCOMES-AND-AGENT-MANDATE.md) | Audience, proficiency targets, pedagogical rules, duplication cleanup, quality bar, and what every agent must guarantee. |
| [`02-REPOSITORY-GIT-WORKFLOW-AND-TECHNICAL-CONSTRAINTS.md`](./02-REPOSITORY-GIT-WORKFLOW-AND-TECHNICAL-CONSTRAINTS.md) | Git workflow for candidates, `.gitignore`, `package.json` rules, **no `node_modules`**, testing stack for JS tasks, and runtime expectations. |
| [`03-DAY-FOLDER-TASK-STRUCTURE-AND-NAMING-CONVENTIONS.md`](./03-DAY-FOLDER-TASK-STRUCTURE-AND-NAMING-CONVENTIONS.md) | Exact directory tree, file names, templates for theory MD, task MDs, boilerplate + `TODO` conventions. |
| [`04-AUTHORING-GUIDE-THEORY-PRACTICAL-TASKS-TESTS-AND-45-DAY-TOPIC-MAP.md`](./04-AUTHORING-GUIDE-THEORY-PRACTICAL-TASKS-TESTS-AND-45-DAY-TOPIC-MAP.md) | Per-topic theory outline, practical-task design rules, unit-test expectations for JavaScript, evaluation criteria for React/Node, and a **reference 45-day topic schedule**. |

## Out of scope for this folder

- The actual `Day XX` folders and task implementations are **not** created here; they will be generated in a follow-up session using these specs.
- No `node_modules` or lockfile policy beyond what is specified in `02` (candidates run `npm install` locally).

## Versioning

When these instructions change, bump the **“Instruction set version”** line at the top of `01` and add a short **changelog** section at the bottom of `01` so agents know which rules apply.

**Instruction set version:** `1.0.0` (initial)
