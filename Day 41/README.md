# Day 41 — Node.js Runtime, Modules, and the Event Loop

## Learning objectives

- Describe how **Node.js** runs JavaScript on the server using **V8** and **libuv**.
- Use **ES modules** (`import` / `export`) with clear file URLs and `path` helpers.
- Explain **macrotasks** vs **microtasks** at a practical level (`setTimeout`, `Promise.then`, `queueMicrotask`, `process.nextTick`).
- Prefer **non-blocking** `fs.promises` APIs over synchronous disk I/O in servers.
- Recognize **blocking** work as a throughput and latency hazard for concurrent HTTP handling.

## Prerequisites

- **Days 17–33** (JavaScript fundamentals, Promises).
- Optional: skim Node.js “Overview of the Node.js block diagram” in the official docs.

## How to use this folder

1. Read `DAY-41-THEORY-AND-REFERENCE.md`.
2. Complete `practical-tasks/` in order; each task is a small **Node 18+** ESM package with **`npm test`** (Vitest).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-esm-path-and-url-basics` | Node (logic + tests) | `npm install` → `npm test` |
| 2 | `task-02-macrotask-microtask-order-lab` | Node (logic + tests) | `npm install` → `npm test` |
| 3 | `task-03-async-fs-json-summary` | Node (logic + tests) | `npm install` → `npm test` |
| 4 | `task-04-blocking-vs-async-file-read` | Node (logic + tests) | `npm install` → `npm test` |
