# Day 27 — OOP in JavaScript: Constructors, Fields, `#`, and `static`

**Primary theme:** Object-oriented idioms in JS—constructors, instance vs private fields, static members  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Related tasks:** `task-01-class-counter-fields`, `task-02-private-hash-balance`, `task-03-static-factory-parser`, `task-04-bank-account-challenge`  
**Instruction alignment:** Maps to *OOP: constructors; public/private/static* from the master topic list.

---

## Overview

JavaScript’s OOP model is **prototypal**, but **ES2015 classes** give familiar syntax. **Private fields** (`#x`) enforce encapsulation at the language level, while `static` methods model type-level utilities (factories, parsers) without allocating instances.

---

## Day roadmap

1. Constructors and `new`
2. Instance fields vs methods
3. Private fields `#`
4. `static` members
5. Common mistakes & debugging
6. Further reading (MDN)
7. Glossary
8. Answers (self-test)

---

## Constructors and `new`

### What it is

A **constructor** initializes an object’s state. With `class`, `constructor(...)` runs on `new`.

#### Examples

```js
class Point {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
}
```

#### Quick checks

1. What does `new` return if `constructor` returns a plain object?

---

## Private fields `#`

### What it is

Fields prefixed with `#` are **lexically private** to the class body—no runtime escape hatch from outside.

#### Quick checks

1. Can subclasses access a base class’s `#field` directly?

---

## `static` members

### What it is

`static` methods/properties live on the **constructor**, not each instance.

#### Quick checks

1. Inside a static method, what does `this` refer to?

---

## Common mistakes & debugging

- Forgetting `new` (strict mode class constructors throw if mis-called).
- Trying to read private fields from tests (you should test **behavior**, not internals).

---

## Further reading

- MDN: [Classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes)
- MDN: [Private features](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Private_class_fields)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Instance** | Object created by `new`. |
| **Static** | Belongs to the class function itself. |

---

## Answers (self-test)

1. If constructor returns an object, **that object** becomes the result of `new` (rare pattern).
2. **Subclasses** cannot access base `#fields` directly.
3. **Static `this`:** typically the class constructor itself.
