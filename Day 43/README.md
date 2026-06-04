# Day 43 — JWT Authentication with Express

## Learning objectives

- **Sign** and **verify** JSON Web Tokens with a server-side secret.
- Send tokens using the **`Authorization: Bearer <token>`** header.
- Differentiate **`401 Unauthorized`** (missing/invalid token) from **`403 Forbidden`** (valid token, insufficient scope).

## Prerequisites

- **Day 42** (Express middleware ordering, JSON bodies).

## How to use this folder

1. Read `DAY-43-THEORY-AND-REFERENCE.md`.
2. Complete tasks in order; copy **`.env.example` → `.env`** for local secrets (never commit `.env`).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-jwt-sign-verify-helpers` | Node + tests | `npm install` → `npm test` |
| 2 | `task-02-login-route-bearer-auth` | Node / Express | `npm install` → `npm test` |
| 3 | `task-03-roles-401-vs-403` | Node / Express | `npm install` → `npm test` |
| 4 | `task-04-refresh-free-token-claims` | Node / Express | `npm install` → `npm test` |
