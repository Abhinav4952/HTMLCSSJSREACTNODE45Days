# Task 1 — `mongoose.connect` + `/health`

## Summary

Finish **`connectMongo`** in `src/db/mongoose.js` using your cohort’s standard environment variables, then confirm **`GET /health`** reports **`mongo: "connected"`** once the driver is ready.

## Learning goals

- Call **`mongoose.connect(MONGODB_URI, { dbName })`** exactly as Mongoose documents for modern drivers.
- Keep **connection configuration** in **`.env`** / **`.env.example`** and optional `src/config/env.js`.

## Provided files (Mongo standard layout)

| File | Purpose |
|------|---------|
| `.env.example` | Lists **`MONGODB_URI`** and **`MONGODB_DB_NAME`** (committed; **no real passwords**). |
| `.env` (you create) | Paste real **`MONGODB_URI`**; set **`MONGODB_DB_NAME`** (default **`course-node-45`**). |
| `src/config/env.js` | Loads **`dotenv`** and validates **`MONGODB_URI`** is present for `npm start`. |
| `src/db/mongoose.js` | **Primary connection file** — contains `TODO(Day44-task01)`. |
| `src/app.js` | Express app + `/health` using `mongoState()`. |
| `src/server.js` | **Startup order:** `await connectMongo()` **before** `app.listen` (already wired). |

## Environment variables (verbatim)

Use exactly these names across Days **44–45**:

| Name | Meaning |
|------|---------|
| **`MONGODB_URI`** | Full SRV or local URI (paste from instructor/Atlas/Docker). |
| **`MONGODB_DB_NAME`** | Logical database name for this cohort — default **`course-node-45`**. |

Never commit **`.env`**; rubrics should **fail** if secrets appear in git.

## Prerequisites

- Node **18+**.
- MongoDB reachable from your machine (Atlas network access / Docker port mapping).

## What you will implement

1. **`connectMongo`**: read config via **`getMongoConfig()`**, **`await mongoose.connect`**, pass **`dbName`**. If connect fails, surface a helpful error (rethrow is fine in this lab).

## Constraints

- Only edit files containing **`TODO(Day44-task01)`** (the connection helper).
- Do **not** commit **`.env`**.

## How to run and verify

### Install dependencies

```bash
cd "Day 44/practical-tasks/task-01-mongoose-connect-health"
npm install
```

### Automated tests (in-memory Mongo)

```bash
npm test
```

Vitest boots **`mongodb-memory-server`**, exports an in-memory URI into `process.env`, dynamically imports your modules, and expects `/health` to report **`connected`**.

### Manual server (real Atlas/Docker)

```bash
cp .env.example .env   # then paste MONGODB_URI
npm start
# GET http://localhost:4401/health
```

## `TODO` map

| File | Done means |
|------|------------|
| `src/db/mongoose.js` | `connectMongo` establishes default Mongoose connection with `dbName`. |

## Submission checklist (Git)

- [ ] `npm test` passes.
- [ ] `.env` not committed.
