# Day 19 — Objects: Creation, Access, Methods, and Descriptors (Intro)

**Primary theme:** Plain objects as records, dynamic keys, methods, and a first peek at property descriptors  
**Estimated study time:** 2–3 hours theory + 4–7 hours tasks  
**Related tasks:** `task-01-object-literal-records`, `task-02-bracket-and-dynamic-keys`, `task-03-methods-on-plain-objects`, `task-04-property-descriptor-peek`  
**Instruction alignment:** Maps to *Objects: create, manage properties* and *property descriptors (intro)* from the master topic list.

---

## Overview

JavaScript objects are flexible maps from strings (and symbols) to values. That flexibility is powerful—and dangerous—when keys come from user input or network data. Day 19 practices **safe shaping**, **bracket notation**, small **method** APIs on plain objects, and **descriptor introspection** to understand what the runtime actually stores for a property.

---

## Day roadmap

1. [Object literals as records](#object-literals-as-records)
2. [Dot vs bracket notation + computed keys](#dot-vs-bracket-notation--computed-keys)
3. [Methods on plain objects (intro to `this`)](#methods-on-plain-objects-intro-to-this)
4. [Property descriptors (read-only intro)](#property-descriptors-read-only-intro)
5. [Common mistakes & debugging](#common-mistakes--debugging)
6. [Further reading](#further-reading)
7. [Glossary](#glossary)
8. [Answers (self-test)](#answers-self-test)

---

## Object literals as records

### What it is

An **object literal** `{ ... }` creates a plain object. When used as a **record**, keys are stable field names (`{ id, title }` shorthand is common).

#### Why it exists / why it matters

Most JSON becomes plain objects at runtime.

#### Quick checks

1. Are object keys always strings at lookup time?

---

## Dot vs bracket notation + computed keys

### What it is

- `obj.field` is static and readable.
- `obj[field]` supports dynamic keys and keys that are not valid identifiers.

#### Why it exists / why it matters

Dynamic keys appear in forms, query maps, and internationalization tables.

#### Examples

```js
const key = "version";
const pkg = { [key]: 2 };
```

#### Quick checks

1. When must you use bracket notation?

---

## Methods on plain objects (intro to `this`)

### What it is

A **method** is a function stored as a property. When invoked as `obj.method()`, `this` is typically `obj` (strict/sloppy nuances exist—later days).

#### Why it exists / why it matters

Small modules and “service objects” are often plain objects with methods.

#### Quick checks

1. What happens to `this` if you extract `const fn = obj.method; fn()`?

---

## Property descriptors (read-only intro)

### What it is

`Object.getOwnPropertyDescriptor(obj, key)` returns metadata: `value`, `writable`, `enumerable`, `configurable`, and optional `get`/`set`.

#### Why it exists / why it matters

Explains “why can’t I assign?” bugs and library behavior.

#### Quick checks

1. Does `writable: false` always mean the value cannot change?

---

## Common mistakes & debugging

- Using `obj.key` when `key` is a variable (wrong).
- Assuming JSON preserves `undefined` (it does not).

---

## Further reading

- MDN: [Working with objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_objects)
- MDN: [`Object.getOwnPropertyDescriptor`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertyDescriptor)

---

## Glossary

| Term | Meaning |
|------|---------|
| Record | Object used as a structured bag of fields |
| Descriptor | Metadata object describing a property |

---

## Answers (self-test)

### Records

1. Keys are strings or symbols; many non-symbol keys coerce to string.

### Bracket notation

1. When the key is dynamic, invalid as an identifier, or is a symbol.

### Methods / this

1. `this` is usually `undefined` in strict mode or the global object in sloppy mode—either way, not `obj` unless bound/called correctly.

### Descriptors

1. No—accessors or internal mechanisms can still change observed behavior; `writable:false` forbids direct assignment of a data property’s value.
