# Day 22 — ES2015 Toolkit: Spread, Rest, Destructuring, `for..of`

**Primary theme:** Modern collection ergonomics—copy/merge with spread, aggregate with rest, unpack with destructuring, iterate with `for..of`  
**Estimated study time:** 2–4 hours theory + 4–7 hours tasks  
**Related tasks:** `task-01-spread-arrays-and-objects`, `task-02-rest-parameters-aggregator`, `task-03-destructuring-user-records`, `task-04-for-of-and-entries-pipeline`  
**Instruction alignment:** Maps to *ES2015 basics: spread, destructuring, `for..of`* from the master topic list.

---

## Overview

ES2015 gave JavaScript **syntax sugar that scales**: spread/rest reduce boilerplate, destructuring documents intent at call sites, and `for..of` replaces many index-heavy loops when you only care about values. These tools show up everywhere—from React props merging to Express middleware composition.

The sharp edges are **shallow copies** (nested objects still alias), **rest position rules** (rest must be last), and **iterating plain objects** (not iterable by default—use `Object.entries`).

---

## Day roadmap

1. [Spread in arrays and argument forwarding](#spread-in-arrays-and-argument-forwarding)
2. [Spread and copies in objects](#spread-and-copies-in-objects)
3. [Rest parameters vs the `arguments` object](#rest-parameters-vs-the-arguments-object)
4. [Destructuring assignment and parameters](#destructuring-assignment-and-parameters)
5. [`for..of` and iterables](#forof-and-iterables)
6. [Common mistakes & debugging](#common-mistakes--debugging)
7. [Further reading](#further-reading)
8. [Glossary](#glossary)
9. [Answers (self-test)](#answers-self-test)

---

## Spread in arrays and argument forwarding

### What it is

**Spread** (`...iterable`) expands an iterable into individual elements in **array literals** or **function calls**.

#### Why it exists / why it matters

Copying arrays, concatenating without `concat`, and calling variadic APIs (`Math.max(...nums)`) becomes explicit.

#### Pros and cons

- **Pros:** readable; works with any iterable (arrays, strings, `Set`, etc.).
- **Cons:** creates new arrays—watch allocations in hot paths.

#### What happens without it / when misused

You mutate shared arrays with `push`/`splice` when you meant to derive a new list.

#### Syntax and rules

```js
const base = [1, 2];
const extended = [0, ...base, 3];
const max = Math.max(...scores);
```

#### Examples

**Tiny — copy**

```js
const draft = [...published];
```

**Tiny — prepend**

```js
const nextQueue = [urgent, ...queue];
```

**Medium — immutable update**

```js
function toggleId(ids, id) {
  return ids.includes(id) ? ids.filter((x) => x !== id) : [...ids, id];
}
```

#### Quick checks

1. Does `[...obj]` work for arbitrary plain objects?
2. Does spread copy nested arrays deeply?

---

## Spread and copies in objects

### What it is

Object spread `{ ...src, ...patch }` builds a new object with enumerable own properties from `src` overlaid by `patch`.

#### Why it exists / why it matters

React state updates and API payload shaping often need shallow merges.

#### Pros and cons

- **Pros:** concise; order expresses precedence (later wins).
- **Cons:** shallow merge only; getters/setters/prototype chain nuances exist but rare in beginner tasks.

#### What happens without it / when misused

You mutate a shared config object and break imports across modules.

#### Syntax and rules

```js
const theme = { color: "black", size: 12 };
const darkLarge = { ...theme, size: 18 };
```

#### Examples

**Tiny — defaults + overrides**

```js
const req = { method: "GET", timeoutMs: 500 };
const tuned = { ...req, timeoutMs: 1500 };
```

**Tiny — drop undefined keys when building**

```js
function buildQuery({ q, tag }) {
  return { ...(q ? { q } : {}), ...(tag ? { tag } : {}) };
}
```

**Medium — nested caution**

```js
const a = { x: { n: 1 } };
const b = { ...a, x: { ...a.x, n: 2 } };
```

#### Quick checks

1. If two spreads set the same key, which wins?
2. Is `{ ...null }` valid?

---

## Rest parameters vs the `arguments` object

### What it is

**Rest** collects “the rest” of arguments into a real array parameter: `function f(a, ...rest) {}`.

#### Why it exists / why it matters

`arguments` is not an array, is quirky in arrow functions, and is harder to optimize mentally.

#### Pros and cons

- **Pros:** always a true `Array`; plays nicely with `.map`.
- **Cons:** must be **last** in the parameter list; cannot duplicate.

#### What happens without it / when misused

You place `...rest` before a normal parameter—syntax error.

#### Syntax and rules

```js
function headTail(head, ...tail) {
  return { head, tail };
}
```

#### Examples

**Tiny — forwarding**

```js
function logged(method, ...args) {
  console.log("call", method.name);
  return method(...args);
}
```

**Tiny — ignore first, sum rest**

```js
function dropFirstSum(_ignored, ...nums) {
  return nums.reduce((a, b) => a + b, 0);
}
```

**Medium — normalize call shape**

```js
function emit(event, ...payload) {
  bus.dispatch(event, payload);
}
```

#### Quick checks

1. Can you have two rest parameters in one function?
2. Is `arguments` an array?

---

## Destructuring assignment and parameters

### What it is

**Destructuring** unpacks arrays/objects into bindings: `const { id, name = "anon" } = user`.

#### Why it exists / why it matters

Function signatures become self-documenting; nullish checks cluster less.

#### Pros and cons

- **Pros:** concise defaults at the boundary; great for options objects.
- **Cons:** deep destructuring can obscure missing-field bugs.

#### What happens without it / when misused

Default only triggers for `undefined`, not `null`—surprises in API normalization.

#### Syntax and rules

```js
const [first, second = 0] = coords;
function route({ path, method = "GET" }) {
  return `${method} ${path}`;
}
```

#### Examples

**Tiny — swap without temp**

```js
let a = 1;
let b = 2;
[a, b] = [b, a];
```

**Tiny — rename**

```js
const { id: userId } = row;
```

**Medium — nested with guard**

```js
function readPort(cfg) {
  const { server: { port = 8080 } = {} } = cfg;
  return port;
}
```

#### Quick checks

1. Does `{ a = 1 } = { a: null }` use the default?
2. What does `const [, second] = list` mean?

---

## `for..of` and iterables

### What it is

`for (const value of iterable)` loops values using the iterable protocol (`Symbol.iterator`).

#### Why it exists / why it matters

Clearer than manual indexes for many collections; works with `Map`, `Set`, arrays, strings.

#### Pros and cons

- **Pros:** fewer off-by-one errors; can `break`/`continue`.
- **Cons:** plain objects are not iterable—use `Object.entries` / `keys` / `values`.

#### What happens without it / when misused

You iterate object properties with `for..in` and accidentally walk the prototype chain unless guarded.

#### Syntax and rules

```js
for (const ch of "abc") {
  // "a", "b", "c"
}
```

#### Examples

**Tiny — sum array**

```js
function sum(nums) {
  let total = 0;
  for (const n of nums) total += n;
  return total;
}
```

**Tiny — map entries**

```js
for (const [k, v] of counts) {
  console.log(k, v);
}
```

**Medium — object as iterable via entries**

```js
function sumNumericProps(obj) {
  let total = 0;
  for (const [, v] of Object.entries(obj)) {
    if (typeof v === "number" && Number.isFinite(v)) total += v;
  }
  return total;
}
```

#### Quick checks

1. Can you `for..of` a plain `{a:1}` object directly?
2. Does `for..in` iterate array indexes or values?

---

## Common mistakes & debugging

- Assuming **deep** copies with object/array spread.
- Using `for..in` on arrays when you want values (indexes are strings).
- Expecting destructuring defaults to replace `null`.

---

## Further reading

- MDN: [Spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax)
- MDN: [Rest parameters](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/rest_parameters)
- MDN: [Destructuring assignment](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment)
- MDN: [`for...of`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...of)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Iterable** | Value exposing `Symbol.iterator` consumed by `for..of`. |
| **Shallow copy** | Copy top-level properties; nested objects shared by reference. |
| **Rest** | Collect remaining args/properties into an array/object pattern. |

---

## Answers (self-test)

1. Plain objects are not iterable for `[...obj]` unless custom iterator—use `Object.values`/`entries`. **Nested:** spread is shallow.
2. **Later spread wins** on duplicate keys. **`{ ...null }`:** valid in modern engines; spreads skip `null`/`undefined` sources.
3. **Two rests:** no (syntax error). **`arguments`:** not a real array.
4. **`null` default:** no—`null` is an explicit value; default only for `undefined`. **Comma skip:** `second` is second element.
5. **Plain object `for..of`:** not without iterator. **`for..in`:** enumerable string keys (indexes for arrays), not values directly.
