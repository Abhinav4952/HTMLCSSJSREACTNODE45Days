# Day 28 — Prototypes: `Object.create`, Chains, and `instanceof`

**Primary theme:** Prototype chain lookup and delegation  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Instruction alignment:** Maps to *Prototypal inheritance: prototypes, constructor patterns, `instanceof`*.

---

## Overview

Each object may link to a **prototype** object for property/method lookup. `Object.create(proto)` sets `[[Prototype]]` explicitly. `instanceof` asks whether `Constructor.prototype` appears in an object’s chain.

---

## Day roadmap

1. `[[Prototype]]` vs `prototype` property
2. `Object.create`
3. `instanceof`
4. Common mistakes
5. Further reading (MDN)
6. Answers

---

## `Object.create`

### What it is

Creates a new object with a specified prototype.

#### Examples

```js
const base = { hi() { return "hi"; } };
const child = Object.create(base);
```

#### Quick checks

1. Does `Object.create(null)` have a prototype?

---

## `instanceof`

### What it is

`obj instanceof C` checks the prototype chain for `C.prototype`.

#### Quick checks

1. Can `instanceof` lie if `prototype` is reassigned?

---

## Further reading

- MDN: [`Object.create`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/create)
- MDN: [`instanceof`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/instanceof)

---

## Answers (self-test)

1. **`Object.create(null)`:** no ordinary prototype (good for dictionaries).
2. **Reassigned `prototype`:** yes, `instanceof` can become inconsistent—avoid mutating `prototype` after instances exist.
