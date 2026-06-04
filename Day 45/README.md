# Day 45 — Capstone API (Express + JWT + Mongoose)

## Learning objectives

- Combine **Express routing**, **JWT authentication**, and **Mongoose persistence** in a cohesive “feature slice.”
- Model **ownership** (`userId` references) and enforce it on mutating routes.
- Keep **secrets** in **`.env`**, **never** in Git.

## Prerequisites

- **Days 41–44** (Node, Express, JWT, Mongoose).

## How to use this folder

1. Read `DAY-45-THEORY-AND-REFERENCE.md`.
2. Each task builds on the same architectural ideas; later tasks assume you understand earlier ones, but **each folder is self-contained** with its own `package.json`.
3. Use **Atlas/Docker** Mongo + `.env` for manual runs; automated tests use **`mongodb-memory-server`**.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-capstone-users-register` | Express + Mongoose | `npm install` → `npm test` |
| 2 | `task-02-capstone-login-jwt-profile` | Express + JWT + Mongoose | `npm install` → `npm test` |
| 3 | `task-03-capstone-notes-crud` | Authenticated CRUD | `npm install` → `npm test` |
| 4 | `task-04-capstone-notes-ownership-and-errors` | Ownership + errors | `npm install` → `npm test` |
