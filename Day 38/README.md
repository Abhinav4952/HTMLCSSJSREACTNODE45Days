# Day 38 — Virtual DOM, Reconciliation, List Keys, and HOC Motivation

## Learning objectives

- Explain **reconciliation** at a high level: React matches old vs new element trees to update the DOM efficiently.
- Choose **stable, unique keys** for list items to preserve component identity across reorders and edits.
- Recognize **index keys** as a recurring footgun when list order changes.
- Describe **higher-order components (HOCs)** as **function wrappers** that reuse cross-cutting UI logic (modern alternatives exist, but the pattern is still worth reading).

## Prerequisites

- **Days 34–37** (components, state, composition, forms).

## How to use this folder

1. Read `DAY-38-THEORY-AND-REFERENCE.md` (this day intentionally revisits **lifecycle framing** alongside keys, per course map note F.1).
2. Complete tasks in order; each is a standalone Vite app.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-stable-key-grocery-list` | React | `npm install` → `npm run dev` (and `npm run build` where documented) |
| 2 | `task-02-reorder-keys-regression-fix` | React | `npm install` → `npm run dev` (and `npm run build` where documented) |
| 3 | `task-03-keyed-inline-edit-rows` | React | `npm install` → `npm run dev` (and `npm run build` where documented) |
| 4 | `task-04-with-prefix-title-hoc` | React | `npm install` → `npm run dev` (and `npm run build` where documented) |
