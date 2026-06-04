# Day 41 — Node Runtime, Modules, and the Event Loop

**Primary theme:** Node.js as a JavaScript runtime on the server — modules, timers, and event-loop ordering.  
**Estimated study time:** 1.5–3 hours theory + 3–5 hours tasks  
**Related tasks:** `task-01-esm-path-and-url-basics`, `task-02-macrotask-microtask-order-lab`, `task-03-async-fs-json-summary`, `task-04-blocking-vs-async-file-read`  
**Instruction alignment:** Maps to **Node.js / Express ecosystem → Node.js runtime concepts including the event loop** from the master topic list.

---

## Overview

Today you stop thinking of JavaScript only inside a browser tab. **Node.js** executes the same language on a machine that may serve thousands of short requests. That shift makes **the event loop** and **non-blocking I/O** first-class engineering concerns: one accidentally synchronous file read can stall every concurrent client.

You will reinforce **ES modules** (the modern default in new Node projects), practice **path and URL** hygiene (surprisingly common sources of “works on my machine” bugs), and run **measurable** experiments with **timers and microtasks**. The practical tasks use **Vitest** so you get immediate feedback while staying inside Node-only tooling.

---

## Day roadmap

1. Node.js, V8, and libuv (mental model)
2. ES modules in Node (`"type": "module"`, file URLs)
3. Event loop: timers, microtasks, and honest limits
4. File system APIs: sync vs async
5. Common mistakes & debugging
6. Further reading & glossary

---

## 1. Node.js, V8, and libuv

### What it is

**Node.js** is a runtime that bundles **Google’s V8** JavaScript engine with a **platform abstraction layer** (historically centered on **libuv**) to provide **networking**, **file I/O**, **timers**, and **worker threads** outside the browser.

#### Why it exists / why it matters

Browsers optimize for **interactive rendering** and **same-origin networking**. Servers optimize for **high connection counts**, **streaming**, and **integration** with databases and queues. Node gives one language across client tooling and services, which speeds teams up — if engineers respect I/O boundaries.

#### Pros and cons

- **Pros**
  - One language for front-end and small/medium services.
  - Huge **npm** ecosystem for integrations.
  - Excellent for **I/O-bound** APIs when code stays non-blocking.
- **Cons / tradeoffs**
  - **CPU-heavy** tasks need care (Worker threads, external services, or another runtime).
  - **Implicit concurrency** makes shared mutable in-memory state risky without discipline.

#### What happens without it / when misused

Treating Node like a thread-per-request Java server without measuring blocking leads to **mysterious latency spikes** under load: everything queues behind one synchronous disk read.

#### Syntax and rules

- Prefer **LTS** Node versions (18+ or 20+ for this cohort).
- Declare **`"type": "module"`** when using `import`/`export` in `.js` files.

#### Examples

**Tiny — check Node version**

```bash
node -v
```

**Tiny — run an ESM file**

```json
{ "type": "module" }
```

```js
// hello.mjs or package.json with type module
console.log('Hello from', import.meta.url);
```

**Medium — conceptual diagram (mental model)**

```text
Your JS runs on one thread by default
  ↓
When you await / register callbacks, libuv may do work in the thread pool
  ↓
When ready, callbacks re-enter the JS thread via the event loop
```

#### Quick checks (self-test questions)

1. Name two responsibilities V8 handles vs what libuv typically handles.
2. Why is “single-threaded JavaScript” a simplification?
3. When is Worker threads a better fit than trying to speed up JS on the main thread?

---

## 2. ES modules in Node

### What it is

**ES modules** are the standardized `import` / `export` syntax. Node resolves them using **URLs** (especially `file:` URLs) and **package boundaries**.

#### Why it exists / why it matters

Classic CommonJS (`require`) is still widespread, but **ESM** aligns with browsers and modern bundlers, and enables **top-level `await`** in modules.

#### Pros and cons

- **Pros:** Static structure, better tree-shaking in bundlers, matches browser modules.
- **Cons:** Occasional friction with older packages, explicit file extensions sometimes required.

#### What happens without it / when misused

Mixing `require` and `import` incorrectly, or wrong **`import.meta.url`** assumptions, breaks cross-platform paths (Windows vs POSIX).

#### Syntax and rules

- In Node ESM, use **`import.meta.url`** as the canonical “where am I?” string.
- Convert with **`path.dirname(fileURLToPath(import.meta.url))`**.

#### Examples

**Tiny — dirname pattern**

```js
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
```

**Tiny — JSON import (Node 18+)**

```js
import pkg from '../package.json' assert { type: 'json' };
```

(If your Node version deprecates `assert`, follow current Node docs for import attributes.)

**Medium — absolute import helper**

```js
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export function resolveFromHere(...segments) {
  const here = path.dirname(fileURLToPath(import.meta.url));
  return path.join(here, ...segments);
}
```

#### Quick checks

1. Why is `__dirname` not defined automatically in ESM?
2. What does `import.meta.url` represent on Windows?

---

## 3. Event loop: timers, microtasks, and honest limits

### What it is

The **event loop** schedules when your callbacks run after I/O, timers, and promises settle. **Macrotasks** include timers like `setTimeout`. **Microtasks** include promise reactions and `queueMicrotask`. **`process.nextTick`** runs before the normal microtask checkpoint in Node (a sharp edge — teach it as “even sooner, but don’t build deep logic on subtle ordering”).

#### Why it exists / why it matters

Understanding ordering helps debug **logging surprises**, **flaky tests**, and **partially initialized objects** visible to callbacks.

#### Pros and cons

- **Pros:** Efficient multiplexing of I/O without threads everywhere.
- **Cons:** Easy to starve the loop with **CPU** or **sync I/O**.

#### What happens without it / when misused

Over-using `process.nextTick` recursively can **starve** I/O; blocking the loop makes **health checks fail**.

#### Syntax and rules

- Prefer **`setImmediate`** for “run after I/O” in some Node APIs — but learn your actual ordering with tests.
- Teach microtasks as: **promise reactions run before the next macrotask timer** (high level).

#### Examples

**Tiny — microtask before timer**

```js
console.log('A');
setTimeout(() => console.log('B'), 0);
queueMicrotask(() => console.log('C'));
Promise.resolve().then(() => console.log('D'));
console.log('E');
```

**Tiny — await boundary**

```js
async function main() {
  console.log(1);
  await Promise.resolve();
  console.log(2);
}
console.log(0);
main();
console.log(3);
```

**Medium — don’t overclaim**

Node’s exact phases are documented; for this course, **verify behavior with small experiments** instead of memorizing every internal queue name.

#### Quick checks

1. Why can `setTimeout(fn, 0)` run after a `Promise.resolve().then(fn)`?
2. Name one symptom of blocking the event loop in an HTTP server.

---

## 4. File system APIs: sync vs async

### What it is

Node exposes **`fs`** in synchronous and callback/promise forms. Prefer **`fs.promises`** in servers.

#### Why it exists / why it matters

Disk reads look “fast” locally but **block the loop** — under concurrency they dominate tail latency.

#### Pros and cons

- **Pros:** `readFileSync` is simple for tiny CLI tools and one-off scripts.
- **Cons:** `*Sync` in hot server paths is a scalability footgun.

#### What happens without it / when misused

Upload spikes + synchronous logging to disk = **cascading timeouts**.

#### Syntax and rules

```js
import fs from 'node:fs/promises';

const buf = await fs.readFile('data.json', 'utf8');
const json = JSON.parse(buf);
```

#### Examples

**Tiny — async read**

```js
import fs from 'node:fs/promises';
await fs.readFile('./note.txt', 'utf8');
```

**Tiny — sync read (CLI only warning)**

```js
import fs from 'node:fs';
const buf = fs.readFileSync('./note.txt', 'utf8');
```

**Medium — safe JSON parse wrapper**

```js
export async function readJsonFile(absPath) {
  const text = await fs.readFile(absPath, 'utf8');
  return JSON.parse(text);
}
```

#### Quick checks

1. When is synchronous FS acceptable?
2. What breaks if you `readFileSync` per request in Express?

---

## Common mistakes & debugging

- Forgetting **`"type": "module"`** and getting `Cannot use import statement outside a module`.
- Assuming **timer order** across nested `setTimeout` without measuring.
- Using **relative paths** from `process.cwd()` when you meant **relative to the module file**.
- Swallowing FS errors — always log **`error.code`** (`ENOENT`, `EACCES`).

---

## Further reading

- [Node.js — About this documentation](https://nodejs.org/en/docs/)
- [Node.js — File system](https://nodejs.org/api/fs.html)
- [Node.js — ES modules](https://nodejs.org/api/esm.html)
- [MDN — JavaScript modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Runtime** | Program that executes your JS (Node + V8 here). |
| **libuv** | Library Node uses for async I/O and the default event loop implementation details. |
| **Macrotask** | Roughly: timer/task queue work like `setTimeout` callbacks. |
| **Microtask** | Promise reactions, `queueMicrotask` callbacks (ordering vs macrotasks matters). |

---

## Answers (quick checks)

**Section 1:**  
1. V8 parses and runs JS; libuv handles many async OS operations and the default event loop.  
2. Because libuv thread pool and workers exist; “single-threaded” refers to your JS execution on the main thread by default.  
3. CPU-bound numerical work that would block the loop for milliseconds+.

**Section 2:**  
1. ESM does not inject CommonJS `__dirname` / `__filename`; derive from `import.meta.url`.  
2. A `file:` URL string pointing at the current module’s location.

**Section 3:**  
1. Promise microtasks are drained before the timer phase runs the `setTimeout` callback (classic ordering demo).  
2. Requests stall, latency grows, timeouts multiply.

**Section 4:**  
1. Boot scripts, build tools, tiny CLIs with negligible concurrency.  
2. Each request blocks others; throughput collapses under parallel load.
