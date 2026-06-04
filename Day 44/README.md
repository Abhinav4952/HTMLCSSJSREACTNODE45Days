# Day 44 — MongoDB Persistence with Mongoose

## Learning objectives

- Connect to MongoDB with **`mongoose.connect`** using **`MONGODB_URI`** and explicit **`dbName`**.
- Define **schemas** and **models** with validation and sensible defaults.
- Implement **CRUD** HTTP routes that persist documents.

## Prerequisites

- **Days 41–43** (Node, Express, JWT).
- A MongoDB deployment: **Atlas free tier**, **Docker `mongo`**, or instructor-provided URI.

## How to use this folder

1. Read `DAY-44-THEORY-AND-REFERENCE.md`.
2. Copy **`.env.example` → `.env`**; paste **`MONGODB_URI`** from Atlas/Docker/instructor; keep **`MONGODB_DB_NAME=course-node-45`** unless a task tells you otherwise.
3. Run tasks with `npm install` then `npm test` / `npm start` as documented.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-mongoose-connect-health` | Node / Express + Mongoose | `npm install` → `npm test` |
| 2 | `task-02-schema-model-create-book` | Mongoose model | `npm install` → `npm test` |
| 3 | `task-03-books-crud-routes` | Express + Mongoose | `npm install` → `npm test` |
| 4 | `task-04-schema-validation-and-timestamps` | Mongoose validation | `npm install` → `npm test` |
