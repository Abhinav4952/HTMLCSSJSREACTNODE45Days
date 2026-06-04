# Day 24 — Dynamic `this`, `call`, `apply`, and `bind`

**Primary theme:** Receiver (`this`) resolution, explicit binding, and partial application  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Related tasks:** `task-01-method-calls-and-this`, `task-02-call-and-apply-borrowing`, `task-03-bind-partial-application`, `task-04-strict-this-footgun-challenge`  
**Instruction alignment:** Maps to *Advanced functions: `this`, scope, `call`/`apply`/`bind`* from the master topic list.

---

## Overview

In JavaScript, **`this` is not lexical** (unlike many other languages): it is generally **determined by how a function is called**, with exceptions (arrow functions, strict undefined, `bind`). That design enables **method calls** on objects and **borrowing** utilities (`Array.prototype.slice.call(arguments)` patterns), but it also creates **lost context** bugs when passing `obj.method` as a callback.

This day connects the mental model to **tooling**: `call`/`apply` set the receiver for one invocation; `bind` returns a new function with a fixed receiver and optionally fixed leading arguments.

---

## Day roadmap

1. [Dynamic `this` in method vs plain calls](#dynamic-this-in-method-vs-plain-calls)
2. [Arrow functions vs methods (preview from Day 21)](#arrow-functions-vs-methods-preview-from-day-21)
3. [`Function.prototype.call`](#functionprototypecall)
4. [`Function.prototype.apply`](#functionprototypeapply)
5. [`Function.prototype.bind`](#functionprototypebind)
6. [Strict mode and `this`](#strict-mode-and-this)
7. [Common mistakes & debugging](#common-mistakes--debugging)
8. [Further reading](#further-reading)
9. [Glossary](#glossary)
10. [Answers (self-test)](#answers-self-test)

---

## Dynamic `this` in method vs plain calls

### What it is

For typical object methods, **`this` refers to the base object** in a call like `obj.method()`. If you extract `const f = obj.method; f()`, the base is lost unless you bind.

#### Why it exists / why it matters

Event handlers and timers often lose the intended receiver unless you bind or wrap.

#### Pros and cons

- **Pros:** flexible borrowing; composable OOP-ish patterns in a prototypal language.
- **Cons:** easy to lose context; harder for newcomers than lexical models.

#### Examples

```js
const counter = {
  n: 0,
  inc() {
    this.n += 1;
    return this.n;
  },
};
counter.inc(); // this === counter
```

#### Quick checks

1. In `obj.method()`, what does `this` usually refer to?

---

## Arrow functions vs methods (preview from Day 21)

### What it is

Arrow functions **do not** introduce their own `this`; they close over the outer `this`.

#### Examples

```js
function makeTimer(label) {
  return {
    label,
    tick() {
      setTimeout(() => console.log(this.label), 0);
    },
  };
}
```

#### Quick checks

1. Should you make every object method an arrow property by default?

---

## `Function.prototype.call`

### What it is

`fn.call(thisArg, arg1, arg2)` invokes `fn` with `this === thisArg` and positional args.

#### Examples

```js
Math.max.call(null, 1, 2, 3);
```

#### Quick checks

1. How many argument lists does `call` accept after `thisArg`?

---

## `Function.prototype.apply`

### What it is

`fn.apply(thisArg, argsArray)` invokes `fn` with `this === thisArg` and args taken from an array-like.

#### Examples

```js
const nums = [1, 5, 2];
Math.max.apply(null, nums);
```

#### Quick checks

1. When is `apply` nicer than spread for very old environments?

---

## `Function.prototype.bind`

### What it is

`fn.bind(thisArg, ...presetArgs)` returns a **new function** permanently bound to `thisArg` (unless further bound with `call`/`apply` on the bound function—advanced edge).

#### Examples

```js
const twice = (x) => x * 2;
const addTwo = twice.bind(null); // rarely needed for pure arrows
```

Better:

```js
function greet(greeting, name) {
  return `${greeting}, ${name}!`;
}
const sayHi = greet.bind(null, "Hi");
sayHi("Ada"); // "Hi, Ada!"
```

#### Quick checks

1. Does `bind` invoke the function immediately?

---

## Strict mode and `this`

### What it is

In **strict** functions, a plain `function () {}` call sets `this` to `undefined` (not the global object).

#### Why it exists / why it matters

Prevents accidental globals and makes lost-context bugs obvious.

#### Quick checks

1. What is `this` inside a strict standalone function call?

---

## Common mistakes & debugging

- Passing `this.method` as a callback without binding.
- Confusing `bind`’s partial-args order with partial application libraries.
- Using `call`/`apply` on arrow functions to “set `this`” (does not work as intended).

---

## Further reading

- MDN: [`this`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this)
- MDN: [`call`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/call)
- MDN: [`apply`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/apply)
- MDN: [`bind`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/bind)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Receiver** | The `this` value for a function invocation. |
| **Hard bind** | `bind` fixes receiver for the returned function. |

---

## Answers (self-test)

1. **`obj.method()`:** `this` is typically `obj`.
2. **Arrow methods default:** usually no—methods needing dynamic `this` should be concise methods or `function` fields.
3. **`call` args:** variadic list after `thisArg`.
4. **`apply`:** array-like arg list; historically useful pre-spread.
5. **`bind` immediate:** no—it returns a function.
6. **Strict standalone `this`:** `undefined`.
