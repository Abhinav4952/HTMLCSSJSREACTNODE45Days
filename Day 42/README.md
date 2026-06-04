# Day 42 — Express Foundations (Routing, Middleware, Errors)

## Learning objectives

- Create an **Express** application with **routers** and **JSON** responses.
- Explain the **middleware pipeline** order: built-ins → routers → error handlers.
- Use **`supertest`** (or equivalent) mentally even when the grader runs it for you.
- Return appropriate **HTTP status codes** for happy and sad paths.

## Prerequisites

- **Day 41** (Node ESM, async I/O mental model).

## How to use this folder

1. Read `DAY-42-THEORY-AND-REFERENCE.md`.
2. Each task folder is a standalone Express package: `npm install` → `npm test` (Vitest + Supertest) and/or `npm start` as documented per task.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-express-json-health` | Node / Express | `npm install` → `npm test` |
| 2 | `task-02-router-mount-and-request-logging` | Node / Express | `npm install` → `npm test` |
| 3 | `task-03-post-json-body-in-memory-store` | Node / Express | `npm install` → `npm test` |
| 4 | `task-04-middleware-order-error-handling` | Node / Express | `npm install` → `npm test` |
