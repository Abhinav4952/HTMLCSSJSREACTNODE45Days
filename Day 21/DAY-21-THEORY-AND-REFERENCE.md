# Day 21 — Functions & Scope Basics

**Primary theme:** Function forms (declaration vs expression), arrow functions, default parameters, and the execution model behind hoisting vs TDZ  
**Estimated study time:** 2–4 hours theory + 4–7 hours tasks  
**Related tasks:** `task-01-function-declarations-and-expressions`, `task-02-arrow-functions-callbacks`, `task-03-default-parameters-lab`, `task-04-hoisting-vs-tdz-challenge`  
**Instruction alignment:** Maps to *Functions: create and invoke* and *ES2015 basics: arrow functions, default parameters* from the master topic list; reinforces *scope* before Day 24’s `this` focus.

---

## Overview

Functions are how you **name behavior**, **parameterize algorithms**, and **defer work**. JavaScript treats functions as **first-class values**: you can pass them around like numbers or objects. That power comes with two classic footguns: **different function “shapes” compile differently in your mental model** (declaration vs expression), and **bindings do not “exist” at every line** the way a beginner’s timeline suggests (`var` hoisting vs `let` TDZ).

This day makes those rules **predictable**: you will be able to explain what the engine does during **creation** vs **execution** phases at a practical level—enough to debug “why is this `undefined`?” and “why did my callback lose context?” (context deepens on Day 24).

---

## Day roadmap

1. [Functions as values (first-class functions)](#functions-as-values-first-class-functions)
2. [Function declarations vs function expressions](#function-declarations-vs-function-expressions)
3. [Arrow functions](#arrow-functions)
4. [Default parameters](#default-parameters)
5. [Scope recap: `var` vs `let`/`const` and the TDZ](#scope-recap-var-vs-letconst-and-the-tdz)
6. [Hoisting: what is and is not “moved”](#hoisting-what-is-and-is-not-moved)
7. [Common mistakes & debugging](#common-mistakes--debugging)
8. [Further reading](#further-reading)
9. [Glossary](#glossary)
10. [Answers (self-test)](#answers-self-test)

---

## Functions as values (first-class functions)

### What it is

A **first-class function** can be stored in variables, passed as arguments, returned from other functions, and created at runtime like any other value.

#### Why it exists / why it matters

UI frameworks, iterators, and Node middleware are all **callback-shaped**. If functions were second-class, you could not express `array.map(x => x * 2)` or `app.use((req, res, next) => …)` cleanly.

#### Pros and cons

- **Pros:** composition, reuse, testability (pass a stub function in tests).
- **Cons:** harder call stacks; accidental creation of functions in hot loops if not careful.

#### What happens without it / when misused

You copy-paste logic instead of parameterizing it; every change becomes a merge conflict.

#### Syntax and rules

```js
function runTwice(fn) {
  fn();
  fn();
}
runTwice(() => console.log("tick"));
```

#### Examples

**Tiny — pass a behavior**

```js
function unless(cond, fn) {
  if (!cond) fn();
}
```

**Tiny — return a behavior**

```js
function makeConstant(v) {
  return () => v;
}
```

**Medium — table-driven formatting**

```js
const formatters = {
  usd: (n) => `$${n.toFixed(2)}`,
  plain: (n) => String(n),
};

function price(tag, amount) {
  return formatters[tag](amount);
}
```

#### Quick checks

1. Can a function be stored as a property of an object?
2. Is `map` a higher-order function?

---

## Function declarations vs function expressions

### What it is

- **Function declaration:** `function name() {}` — creates a binding subject to hoisting rules (see below).
- **Function expression:** any `function`/`async function`/`function*` form that appears where an expression is expected, often `const f = function() {}`.

#### Why it exists / why it matters

Declarations read well at module top-level. Expressions fit **inline assignment**, **conditional creation**, and **IIFE** patterns (Day 25).

#### Pros and cons

- **Pros (declaration):** familiar “verb” naming at file scope; historically hoisted as a whole.
- **Cons (declaration):** less convenient inside tight expressions; can surprise readers if overused inside nested blocks on older engines (historical edge cases—still know block rules).
- **Pros (expression):** pairs naturally with `const` and block scope.
- **Cons (expression):** temporal dead zone applies like `let`/`const` until initialized.

#### What happens without it / when misused

You reference a `const` function before its line and hit **TDZ** `ReferenceError`. You rely on `var fn = function(){}` hoisting of the binding but not the function body assignment—classic bug.

#### Syntax and rules

```js
function declared(x) {
  return x + 1;
}

const expressed = function namedOptional(y) {
  return y * 2;
};
```

#### Examples

**Tiny — declaration at module scope**

```js
export function clamp(n, lo, hi) {
  return Math.min(hi, Math.max(lo, n));
}
```

**Tiny — expression in object literal shorthand**

```js
const api = {
  ping() {
    return "pong";
  },
};
```

**Medium — choose implementation**

```js
function makeLogger(level) {
  if (level === "silent") return () => {};
  return function logLine(msg) {
    console.log(`[${level}] ${msg}`);
  };
}
```

#### Quick checks

1. Which form can appear anonymously as a callback without assigning to a variable first?
2. Does `const f = function(){};` hoist like `function f(){}`?

---

## Arrow functions

### What it is

Arrow functions provide concise syntax: `const add = (a, b) => a + b;` and lexically bind `this` from the surrounding scope (no dynamic `this` rebinding via call sites).

#### Why it exists / why it matters

Callbacks become readable; many React event handlers and array transforms prefer arrows to avoid `this` confusion.

#### Pros and cons

- **Pros:** brevity; lexical `this`; implicit return for single expressions.
- **Cons:** not ideal for methods that need dynamic `this`; no `arguments` object; not constructable with `new`.

#### What happens without it / when misused

You write `obj = { count: 1, inc: () => this.count++ }` and discover `this` is not `obj` (lexical outer `this` wins).

#### Syntax and rules

```js
const ids = items.map((item) => item.id);
const noop = () => {};
const returnsObject = () => ({ ok: true });
```

#### Examples

**Tiny — filter + map pipeline**

```js
const prices = [10, -3, 4.5];
const positiveRounded = prices
  .filter((n) => n > 0)
  .map((n) => Math.round(n));
```

**Tiny — defaulting parameters**

```js
const greet = (name = "friend") => `Hello, ${name}`;
```

**Medium — HOF returning arrow**

```js
function inBand(lo, hi) {
  return (n) => n >= lo && n <= hi;
}
[1, 5, 9].filter(inBand(3, 7)); // [5]
```

#### Quick checks

1. Can you use `new` with an arrow function?
2. Does an arrow function have its own `arguments` binding?

---

## Default parameters

### What it is

Default parameters assign a value when the argument is **`undefined`** (not for other “falsy” values like `0` or `""` unless you explicitly handle them).

#### Why it exists / why it matters

Cleaner signatures than `x = typeof x === "undefined" ? 1 : x` scattered everywhere.

#### Pros and cons

- **Pros:** readable; can reference earlier parameters; runs per invocation.
- **Cons:** mutable default objects are still a footgun if reused and mutated.

#### What happens without it / when misused

```js
function pushItem(item, bag = []) {
  bag.push(item);
  return bag;
}
```

If you mutate `bag` and return it, callers might share unintended state—prefer returning new arrays/objects when immutability matters.

#### Syntax and rules

```js
function fmt(n, digits = 2) {
  return n.toFixed(digits);
}
function join(first, last = "") {
  return `${first} ${last}`.trim();
}
```

#### Examples

**Tiny — undefined-only defaulting**

```js
function mul(a, b = 1) {
  return a * b;
}
mul(5); // 5
mul(5, 0); // 0 (does not replace with default)
```

**Tiny — earlier param in later default**

```js
function rect(w, h = w) {
  return { w, h };
}
```

**Medium — safe immutable default**

```js
function mergeTags(tags, defaults = { env: "dev" }) {
  return { ...defaults, ...tags };
}
```

#### Quick checks

1. Does `fn(5, undefined)` trigger a default for the second parameter?
2. Does `fn(5, null)` trigger a default for the second parameter?

---

## Scope recap: `var` vs `let`/`const` and the TDZ

### What it is

- **`var`:** function-scoped; binding exists for the whole function with **hoisting** initialization as `undefined`.
- **`let`/`const`:** block-scoped; binding exists but is **uninitialized** from block start until the declaration runs (**TDZ**). Access throws `ReferenceError`.

#### Why it exists / why it matters

TDZ catches real bugs: using a value before initialization. `var` in loops caused classic closure bugs (compare Day 17’s `let` loop example).

#### Pros and cons

- **Pros (`let`/`const`):** predictable block scope; TDZ prevents “half-initialized reads.”
- **Cons:** more errors during learning; temporal concepts are unfamiliar.

#### What happens without it / when misused

Copy-paste `var` in a loop and wonder why every closure sees the final index.

#### Syntax and rules

```js
{
  const x = 1;
  // const x = 2; // SyntaxError: redeclared
}
```

#### Examples

**Tiny — block scope**

```js
let a = 1;
{
  let a = 2;
}
// outer a is still 1
```

**Tiny — TDZ illustration (do not ship this pattern)**

```js
function demo() {
  // console.log(v); // ReferenceError for let
  let v = 1;
  return v;
}
```

**Medium — prefer `const` by default**

```js
function totals(rows) {
  const sum = rows.reduce((acc, r) => acc + r.amount, 0);
  return sum;
}
```

#### Quick checks

1. Is `let` hoisted?
2. What error do you get when accessing a `let` binding in its TDZ?

---

## Hoisting: what is and is not “moved”

### What it is

**Hoisting** describes compile-time **scope registration**: declarations create bindings early, but **initializations** still run at their original lines. Function declarations (not `const` assignments) are fully initialized early within their scope in practical terms; `var` initializes to `undefined`; `let`/`const` stay in TDZ until the declaration executes.

#### Why it exists / why it matters

Explains debugger stepping surprises and minified stack traces where names exist “too early.”

#### Pros and cons

- **Pros:** knowing the model reduces superstition; easier to read bundler output.
- **Cons:** easy to over-teach as “code is physically moved.”

#### What happens without it / when misused

You “fix” TDZ errors by switching to `var`, reintroducing subtler bugs.

#### Syntax and rules

Prefer **write code in temporal order** even when you understand hoisting—readability beats cleverness.

#### Examples

**Tiny — `var` binding exists early**

```js
function f() {
  return typeof x; // "undefined"
  var x = 1;
}
```

**Tiny — `let` does not**

```js
function g() {
  // return typeof y; // ReferenceError in TDZ
  let y = 1;
  return typeof y;
}
```

**Medium — declare-then-use discipline**

```js
const helpers = {
  clamp,
};

function clamp(n, lo, hi) {
  return Math.min(hi, Math.max(lo, n));
}

export { helpers };
```

#### Quick checks

1. Does a function declaration inside a function body hoist to the top of that body?
2. Why is `let` “hoisted” but still unsafe to read early?

---

## Common mistakes & debugging

- Using arrow functions for object methods that need `this` to refer to the object (Day 24 fixes this properly).
- Assuming default parameters trigger for `null` or `0`.
- Creating a **mutable default** array/object and mutating it across calls.
- Explaining hoisting as “JavaScript moves lines” instead of **binding lifecycle**.

---

## Further reading

- MDN: [Functions guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions)
- MDN: [Arrow functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions)
- MDN: [Default parameters](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Default_parameters)
- MDN: [`let` temporal dead zone](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let#temporal_dead_zone_tdz)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Binding** | A named reference to a value in a scope. |
| **TDZ** | Period where a `let`/`const` binding exists but must not be read. |
| **Hoisting** | Scope registration behavior for declarations (informal collective term). |
| **HOF** | Higher-order function: takes/returns functions. |
| **Lexical scope** | Inner functions see outer variables based on source text nesting. |

---

## Answers (self-test)

1. **First-class:** Yes; functions are values. **`map`:** Yes, it accepts a function argument.
2. **Anonymous callback:** Both can be used inline; expressions are common as callbacks. **`const` vs declaration:** `const` assignment is not hoisted like a function declaration; TDZ applies until the line runs.
3. **Arrow + `new`:** No. **`arguments`:** No own binding; use rest parameters `(...args)`.
4. **`undefined` default:** Yes. **`null`:** No—`null` is a value and is passed through.
5. **`let` hoisted:** Binding is registered, but uninitialized until the declaration line. **TDZ error:** `ReferenceError`.
6. **Inner function declaration:** Hoisted to top of that enclosing function body in practical terms. **`let` hoisted but unsafe:** registration ≠ initialization; reads are forbidden until the initializer runs.
