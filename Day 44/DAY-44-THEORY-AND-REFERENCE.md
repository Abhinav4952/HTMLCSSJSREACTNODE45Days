# Day 44 — MongoDB + Mongoose (Connection, Models, CRUD)

**Primary theme:** Persist structured data with **Mongoose** models backed by MongoDB.  
**Estimated study time:** 2–4 hours theory + 4–7 hours tasks  
**Related tasks:** `task-01-mongoose-connect-health`, `task-02-schema-model-create-book`, `task-03-books-crud-routes`, `task-04-schema-validation-and-timestamps`  
**Instruction alignment:** Maps to **MongoDB connection (Mongoose)** from the master topic list.

---

## Overview

**MongoDB** stores BSON documents in collections. **Mongoose** adds **schemas**, **validation**, **defaults**, and **middleware** on top of the official driver—this cohort standardizes on **Mongoose only** for Mongo work (Days **44–45**).

You will connect with **`mongoose.connect(uri, { dbName })`**, define a **Book** model, expose **CRUD** routes, and tighten validation. Always keep secrets in **`.env`**, never committed.

---

## Day roadmap

1. Connections, `dbName`, and Atlas/Docker options
2. Schemas, models, and CRUD operations
3. Validation rules and error shapes
4. Common mistakes & debugging
5. Further reading & glossary

---

## 1. Connections and `dbName`

### What it is

`mongoose.connect` establishes a default connection. Passing **`dbName`** selects the logical database inside a cluster URI.

#### Why it exists / why it matters

Atlas URIs often omit the database path; explicit **`dbName`** avoids accidentally writing to **`test`**.

#### Pros and cons

- **Pros:** One URI for cluster; separate DB per app/environment.
- **Cons:** Wrong `dbName` sends data to an unexpected database.

#### Syntax and rules

```js
await mongoose.connect(process.env.MONGODB_URI, {
  dbName: process.env.MONGODB_DB_NAME || 'course-node-45',
});
```

#### Examples

**Tiny — `.env`**

```bash
MONGODB_URI="mongodb+srv://USER:PASS@cluster.example.mongodb.net"
MONGODB_DB_NAME="course-node-45"
```

**Tiny — Docker (illustrative)**

```bash
docker run --name mongo -p 27017:27017 -d mongo:7
# MONGODB_URI=mongodb://127.0.0.1:27017
```

**Medium — startup order**

`await connect()` **before** listening on HTTP so routes do not race a half-ready connection (unless you intentionally defer).

#### Quick checks

1. Why keep **`MONGODB_URI`** out of Git?
2. What breaks if you connect **after** accepting traffic that queries the DB?

---

## 2. Schemas and models

### What it is

A **Schema** declares fields and types; a **Model** is a constructor for documents in a collection.

#### Syntax and rules

```js
const bookSchema = new mongoose.Schema({
  title: { type: String, required: true },
});
export const Book = mongoose.model('Book', bookSchema);
```

#### Quick checks

1. What collection name does Mongoose default to for `model('Book', ...)`?

---

## 3. Validation and timestamps

### What it is

Schema options like **`minlength`**, **`max`**, and **`timestamps: true`** centralize rules.

#### Why it exists / why it matters

Reject bad data **before** it reaches business logic; audit **`createdAt`**.

#### Examples

```js
new mongoose.Schema(
  { title: { type: String, required: true, minlength: 2 } },
  { timestamps: true },
);
```

#### Quick checks

1. Name one benefit of **`timestamps: true`** vs manually setting dates.

---

## Common mistakes & debugging

- Connecting once per request (slow) vs **once per process** in small labs.
- Forgetting **`await`** on queries returning thenables.
- Returning raw Mongo errors to clients (leaks internals)—map to safe messages in HTTP layers.

---

## Further reading

- [Mongoose — Getting started](https://mongoosejs.com/docs/index.html)
- [MongoDB Atlas — Getting started](https://www.mongodb.com/docs/atlas/getting-started/)

---

## Glossary

| Term | Meaning |
|------|---------|
| **BSON** | Binary JSON-like serialization used by MongoDB. |
| **ODM** | Object Document Mapper (Mongoose). |

---

## Answers

**§1:**  
1. It is a secret credential; public repos get scanned.  
2. Early requests error or race partially connected drivers.

**§2:**  
1. Plural lower-case `books` by convention.

**§3:**  
1. Automatic consistency for `createdAt`/`updatedAt` fields.
