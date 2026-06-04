# Task 4 — Schema validation + timestamps

## Summary

Tighten the **`Book`** schema with **`minlength`** and enable Mongoose **`timestamps`** so documents automatically track **`createdAt`** / **`updatedAt`**.

## Learning goals

- Encode simple string length rules at the schema layer.
- Prefer schema **`timestamps`** over manual date fields for audit basics.

## Environment variables (verbatim)

| Name | Meaning |
|------|---------|
| **`MONGODB_URI`** | Full Mongo URI. |
| **`MONGODB_DB_NAME`** | Logical DB (default **`course-node-45`**). |

## What you will implement

1. `title.minlength = 3` (after trim).
2. Schema options `{ timestamps: true }`.

## Constraints

- Only edit `TODO(Day44-task04)` markers in `src/models/Book.js`.

## How to run and verify

```bash
cd "Day 44/practical-tasks/task-04-schema-validation-and-timestamps"
npm install
npm test
```

## `TODO` map

| Location | Done means |
|----------|------------|
| `Book` schema | Short titles rejected; timestamps present on create. |

## Submission checklist (Git)

- [ ] `npm test` passes.
