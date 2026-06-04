# Day 26 — Closures: Lexical Scope, Loops, and the Module Pattern

**Primary theme:** Closures as captured environments—useful for privacy, hazardous when misunderstood in loops  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Related tasks:** `task-01-counter-factory`, `task-02-lexical-multiplier`, `task-03-loop-closure-handlers`, `task-04-module-pattern-budget-challenge`  
**Instruction alignment:** Maps to *Closures: nested functions, lexical environment, inner vs outer context* and *Functional patterns: IIFE; module pattern intro* from the master topic list.

---

## Overview

A **closure** is the combination of a function plus the **lexical environment** it was created in. That means inner functions keep access to outer bindings even after the outer function returns—powerful for **factories**, **private state**, and **callbacks**, but also the root cause of the classic **`for` loop + `var`** bug where every callback shares one binding.

This day practices **predictable closure design**: factories that return controlled APIs, loop handlers that capture the right index, and a small **module pattern** budget object with hidden balance.

---

## Day roadmap

1. [Lexical environment (mental model)](#lexical-environment-mental-model)
2. [What a closure captures](#what-a-closure-captures)
3. [Factories: functions that return configured functions](#factories-functions-that-return-configured-functions)
4. [Loop closures: `var` pitfall vs `let` fix](#loop-closures-var-pitfall-vs-let-fix)
5. [Module pattern (IIFE-style privacy, modern module equivalent)](#module-pattern-iife-style-privacy-modern-module-equivalent)
6. [Memory and “stale closure” cautions](#memory-and-stale-closure-cautions)
7. [Common mistakes & debugging](#common-mistakes--debugging)
8. [Further reading](#further-reading)
9. [Glossary](#glossary)
10. [Answers (self-test)](#answers-self-test)

---

## Lexical environment (mental model)

### What it is

**Lexical** means “defined by source text nesting”: an inner function’s free variables resolve outward through nested blocks/functions, not by whoever calls it later.

#### Why it exists / why it matters

It is what makes modules, factories, and React hooks (later) possible—stable access to outer variables without threading everything through parameters.

#### Pros and cons

- **Pros:** encapsulation; fewer globals; composable APIs.
- **Cons:** retained references can keep large objects alive; debugging can feel “time travel”-y.

#### Syntax and rules

```js
function outer(x) {
  return function inner(y) {
    return x + y;
  };
}
```

#### Examples

**Tiny — capture a constant**

```js
const add10 = outer(10);
add10(5); // 15
```

**Tiny — each call gets a fresh environment**

```js
const a = outer(1);
const b = outer(2);
```

**Medium — private counter**

```js
function createCounter() {
  let n = 0;
  return {
    inc() {
      n += 1;
      return n;
    },
  };
}
```

#### Quick checks

1. Can an inner function read variables declared in its outer function after the outer returns?

---

## What a closure captures

### What it is

Closures capture **bindings** (variables), not just values at one instant—unless you create a new binding per iteration (`let`) or per call (parameter).

#### What happens without it / when misused

You assume each callback in a loop has its own `i`, but they share one mutable `i`.

#### Examples

```js
function makePrinter(msg) {
  return () => console.log(msg);
}
```

#### Quick checks

1. If ten closures share one `var i`, what value do they typically observe when invoked later?

---

## Factories: functions that return configured functions

### What it is

A **factory** returns objects or functions specialized by outer parameters (multipliers, validators, fetchers).

#### Examples

```js
function makePrefixer(prefix) {
  return (name) => `${prefix}: ${name}`;
}
```

#### Quick checks

1. Why is a factory preferable to a global `currentPrefix` variable?

---

## Loop closures: `var` pitfall vs `let` fix

### What it is

`var` in a loop header creates **one** binding updated each iteration; `let` creates a **per-iteration** binding.

#### Examples

**Problem (`var`)**

```js
const fns = [];
for (var i = 0; i < 3; i += 1) {
  fns.push(() => i);
}
fns.map((f) => f()); // [3,3,3]
```

**Fix (`let`)**

```js
const fns = [];
for (let i = 0; i < 3; i += 1) {
  fns.push(() => i);
}
fns.map((f) => f()); // [0,1,2]
```

#### Quick checks

1. Name two fixes other than `let` (hint: IIFE per iteration, `forEach` callback parameter).

---

## Module pattern (IIFE-style privacy, modern module equivalent)

### What it is

Historically, an **IIFE** returned an object with methods closing over private variables. ES modules give file scope privacy with `export` controlling the public surface.

#### Examples

```js
const counter = (() => {
  let n = 0;
  return { inc: () => (n += 1) };
})();
```

#### Quick checks

1. What is the public API surface of a module pattern object?

---

## Memory and “stale closure” cautions

### What it is

Closures keep outer variables reachable. In UI code, a long-lived listener may capture **stale props/state** unless dependencies are managed (preview: React effects later).

#### Quick checks

1. Does a closure always copy the *current* value of an outer `let` into the inner function at creation time?

---

## Common mistakes & debugging

- Using `var` in async loops producing surprising shared state.
- Creating huge closures accidentally (capturing `this` or big objects when only a field is needed).
- Forgetting that **each factory call** should create **fresh** private state.

---

## Further reading

- MDN: [Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures)
- MDN: [`let` in loops](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for#using_let_in_loops)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Free variable** | Variable used inside a function but declared outside. |
| **Factory** | Function that returns configured objects/functions. |

---

## Answers (self-test)

1. **After outer returns:** yes—bindings remain reachable via the inner function.
2. **`var i` later:** typically the final value after loop ends (e.g. `3` in the snippet).
3. **Global prefix:** avoids hidden coupling and race conditions in concurrent/async code.
4. **Other fixes:** IIFE `(function(i){ ... })(i)`; `forEach((_, i) => ...)`.
5. **Public API:** only returned object’s properties/methods; other bindings stay private.
6. **Outer `let`:** closures see the **binding** across time—reads see updated values unless you snapshot into a new parameter per iteration.
