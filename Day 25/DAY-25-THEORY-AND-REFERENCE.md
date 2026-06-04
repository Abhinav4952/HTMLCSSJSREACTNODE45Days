# Day 25 — Functional Patterns: Callbacks, Chaining, Currying, Memoization

**Primary theme:** IIFE (concept), callbacks, memoization, chaining, currying  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Related tasks:** `task-01-higher-order-callback-map`, `task-02-fluent-config-chain`, `task-03-curry-binary-operations`, `task-04-memoize-stable-keys-challenge`  
**Instruction alignment:** Maps to *Functional patterns: IIFE, callbacks, memoization, chaining, currying* from the master topic list.

---

## Overview

“Functional patterns” in day-to-day JavaScript rarely means category theory—it means **small, composable units**: pass behavior as values, return configured functions, and **remember expensive work** when inputs repeat. You will still balance purity with pragmatics: IIFEs scope variables; memoization trades memory for CPU; currying improves reuse but can obscure arity.

---

## Day roadmap

1. [Callbacks and higher-order functions](#callbacks-and-higher-order-functions)
2. [IIFE: scope isolation](#iife-scope-isolation)
3. [Method chaining](#method-chaining)
4. [Currying](#currying)
5. [Memoization](#memoization)
6. [Common mistakes & debugging](#common-mistakes--debugging)
7. [Further reading](#further-reading)
8. [Glossary](#glossary)
9. [Answers (self-test)](#answers-self-test)

---

## Callbacks and higher-order functions

### What it is

A **callback** is a function passed to another function to run later. A **higher-order function (HOF)** takes or returns functions (`map`, `setTimeout`, Express middleware).

#### Why it exists / why it matters

This is the default composition style for async JS and UI frameworks.

#### Examples

```js
function withTiming(fn) {
  return (...args) => {
    const t0 = performance.now();
    const out = fn(...args);
    const t1 = performance.now();
    console.log(`took ${t1 - t0}ms`);
    return out;
  };
}
```

#### Quick checks

1. Is `Array.prototype.map` a HOF?

---

## IIFE: scope isolation

### What it is

An **IIFE** is invoked immediately: `(function () { /* private */ })();` (or `(() => {})()`).

#### Why it exists / why it matters

Before modules were universal, IIFEs avoided global leaks.

#### Quick checks

1. Do ES modules reduce the need for IIFEs?

---

## Method chaining

### What it is

Methods return **`this`** (or another fluent object) so calls chain: `qb.select().from().where()`.

#### Examples

```js
function createBuilder() {
  return {
    parts: [],
    add(chunk) {
      this.parts.push(chunk);
      return this;
    },
    build() {
      return this.parts.join(" ");
    },
  };
}
```

#### Quick checks

1. What must each chaining method typically return?

---

## Currying

### What it is

**Currying** transforms `f(a, b)` into `f'(a)(b)`.

#### Examples

```js
const add = (a) => (b) => a + b;
add(1)(2);
```

#### Quick checks

1. Does currying change the fundamental computation?

---

## Memoization

### What it is

**Memoization** caches results keyed by inputs to avoid recomputation.

#### Pros and cons

- **Pros:** big wins for expensive pure functions with repeated args.
- **Cons:** memory growth; keying objects by reference vs value; stale caches if function not pure.

#### Examples

```js
function memoizeUnary(fn) {
  const cache = new Map();
  return (x) => {
    if (cache.has(x)) return cache.get(x);
    const y = fn(x);
    cache.set(x, y);
    return y;
  };
}
```

#### Quick checks

1. Why is `JSON.stringify` risky for cache keys?

---

## Common mistakes & debugging

- Memoizing functions with hidden non-determinism (time, randomness, I/O).
- Using object arguments as keys without a stable serialization policy.
- Chains that mutate shared state unexpectedly.

---

## Further reading

- MDN: [Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures)
- MDN: [`Map`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map)

---

## Glossary

| Term | Meaning |
|------|---------|
| **HOF** | Higher-order function. |
| **IIFE** | Immediately invoked function expression. |

---

## Answers (self-test)

1. **`map`:** yes, it is a HOF.
2. **Modules vs IIFE:** modules provide file scope; IIFE less common for isolation now.
3. **Chaining:** usually `return this` (or a new immutable snapshot in advanced APIs).
4. **Currying:** same computation, different call shape.
5. **`JSON.stringify` keys:** key order for plain objects is insertion-dependent; stringify may change; functions/`undefined` omitted.
