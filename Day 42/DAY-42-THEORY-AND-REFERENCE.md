# Day 42 — Express Foundations: Routing, Middleware, and Errors

**Primary theme:** Build HTTP APIs with **Express** using a disciplined **middleware pipeline**.  
**Estimated study time:** 1.5–3 hours theory + 3–6 hours tasks  
**Related tasks:** `task-01-express-json-health`, `task-02-router-mount-and-request-logging`, `task-03-post-json-body-in-memory-store`, `task-04-middleware-order-error-handling`  
**Instruction alignment:** Maps to **Express: routing, request/response, middleware pipeline** from the master topic list.

---

## Overview

**Express** is a minimal web framework that orchestrates **functions** (`(req, res, next) => { ... }`) in order. Everything—from JSON parsing to authentication to your business routes—is **middleware**. Mis-ordering middleware is not a syntax error; it is a **silent logic bug** (empty bodies, missing users, swallowed errors).

Today’s tasks isolate **routing**, **mount paths**, **request logging**, **JSON bodies**, and a deliberate **ordering bug** you must fix with tests as guardrails.

---

## Day roadmap

1. Express mental model: `app`, `Router`, `req`/`res`
2. Middleware pipeline and `next`
3. Error-handling middleware conventions
4. JSON, status codes, and testing with Supertest
5. Common mistakes & debugging
6. Further reading & glossary

---

## 1. Express application shape

### What it is

An **Express app** is a callable request handler function with a `.use`/`.get` registry that dispatches to matching middleware in registration order.

#### Why it exists / why it matters

You need predictable structure for **HTTP concerns** (parsing, auth, logging) separate from **domain logic**.

#### Pros and cons

- **Pros:** Tiny surface area, huge ecosystem, easy to test when `app` is exported without listening.
- **Cons:** Unopinionated—discipline is required (structure, validation, security defaults).

#### What happens without it / when misused

Everything becomes one giant callback file; ordering bugs multiply.

#### Syntax and rules

```js
import express from 'express';

export function createApp() {
  const app = express();
  app.get('/health', (req, res) => {
    res.json({ status: 'ok' });
  });
  return app;
}
```

#### Examples

**Tiny — JSON response**

```js
res.status(201).json({ id: 'abc' });
```

**Tiny — route params**

```js
app.get('/users/:id', (req, res) => {
  res.send(req.params.id);
});
```

**Medium — modular router**

```js
import { Router } from 'express';
const api = Router();
api.get('/ping', (_req, res) => res.json({ pong: true }));
app.use('/api/v1', api);
```

#### Quick checks

1. Why export `createApp` separately from `server.listen`?
2. What is the difference between `app.use('/api', router)` and `router.get('/ping', ...)` when combined?

---

## 2. Middleware ordering

### What it is

Each middleware either **ends** the response (`res.send`, `res.json`) or calls **`next()`** to continue the chain.

#### Why it exists / why it matters

**`express.json()`** must run **before** handlers that read `req.body`. Auth must run **before** protected routes.

#### Pros and cons

- **Pros:** Composable cross-cutting behavior.
- **Cons:** Order is implicit—easy to break under time pressure.

#### What happens without it / when misused

`req.body` is `undefined`, custom headers never logged, errors never reach centralized handlers.

#### Syntax and rules

```js
app.use(express.json());
app.post('/items', (req, res) => {
  console.log(req.body);
  res.sendStatus(204);
});
```

#### Examples

**Tiny — logging middleware**

```js
app.use((req, _res, next) => {
  console.info(req.method, req.url);
  next();
});
```

**Medium — conditional `next()`**

```js
app.use((req, res, next) => {
  if (!req.get('x-lab')) return res.status(400).json({ error: 'missing header' });
  next();
});
```

#### Quick checks

1. Name one symptom of registering `express.json()` after a POST handler that reads `req.body`.
2. When should an error-handling middleware `(err, req, res, next)` appear?

---

## 3. Error middleware

### What it is

Express recognizes **four-argument** functions as error handlers. They run when `next(err)` is invoked or errors are thrown inside `async` route handlers **if** wrapped correctly.

#### Why it exists / why it matters

Centralizes logging, consistent JSON error bodies, and safe status mapping.

#### Pros and cons

- **Pros:** One place to map `ZodError`, DB failures, etc.
- **Cons:** Forgotten `next(err)` leads to hanging requests.

#### Syntax and rules

```js
app.use((err, _req, res, _next) => {
  console.error(err);
  res.status(500).json({ error: 'internal_error' });
});
```

#### Examples

**Tiny — propagate**

```js
app.get('/boom', (_req, _res, next) => {
  next(new Error('boom'));
});
```

#### Quick checks

1. Why must error middleware usually be registered **after** routes?

---

## Common mistakes & debugging

- **`req.body` undefined** → JSON parser not installed / wrong order.
- **404 for mounted router** → forgot prefix or mismatched leading slash.
- **Tests hang** → missing `res.end` / forgot to call `next`.

---

## Further reading

- [Express — Routing](https://expressjs.com/en/guide/routing.html)
- [Express — Writing middleware](https://expressjs.com/en/guide/writing-middleware.html)
- [Express — Error handling](https://expressjs.com/en/guide/error-handling.html)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Middleware** | `function (req, res, next)` participating in the pipeline. |
| **Router** | Mini-app mounted at a sub-path. |
| **Supertest** | HTTP assertion helper wrapping `app` without a real network port (in-process). |

---

## Answers

**Section 1:**  
1. Supertest needs the app without binding a port; listening belongs to production entry.  
2. `app.use('/api', router)` prefixes every `router` path with `/api`.

**Section 2:**  
1. Body never parses; handler sees `undefined`.  
2. After routes (and other middleware) so it catches forwarded errors.

**Section 3:**  
1. So normal handlers run first and can call `next(err)`; error handler catches late.
