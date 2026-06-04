# Day 17 — JavaScript Values, Types, and Variables

**Primary theme:** Primitives vs objects, variable declarations, template literals, and coercion awareness  
**Estimated study time:** 2–3 hours theory + 4–7 hours tasks  
**Related tasks:** `task-01-typeof-and-primitive-lab`, `task-02-let-const-scope-lab`, `task-03-template-literal-builder`, `task-04-coercion-safety-guards`  
**Instruction alignment:** Maps to *Variables, values, types* and *ES2015 basics* (`const`/`let`, template literals) from the master topic list.

---

## Overview

JavaScript variables are not “boxes that hold types.” They are **bindings** to values, and values carry their own type at runtime. That model enables fast iteration, but it also makes **coercion** and **typeof surprises** expensive in production if you do not build small guardrails early.

This day is intentionally “small but sharp”: you will write **pure functions** with Vitest contracts—mirroring how real codebases validate inputs before formatting strings, logging, or rendering UI.

---

## Day roadmap

1. [What is a value? Primitives vs objects](#what-is-a-value-primitives-vs-objects)
2. [`typeof` and the `null` quirk](#typeof-and-the-null-quirk)
3. [`const`, `let`, and `var` (scoping + reassignment)](#const-let-and-var-scoping--reassignment)
4. [Template literals and tagged templates (intro)](#template-literals-and-tagged-templates-intro)
5. [Coercion preview: why `==` scares maintainers](#coercion-preview-why--scares-maintainers)
6. [Common mistakes & debugging](#common-mistakes--debugging)
7. [Further reading](#further-reading)
8. [Glossary](#glossary)
9. [Answers (self-test)](#answers-self-test)

---

## What is a value? Primitives vs objects

### What it is

**Primitives** include `undefined`, `null`, booleans, numbers, bigints, strings, and symbols. Most are **immutable** (a string “change” creates a new string). **Objects** (including arrays, functions, dates) are mutable by default through their properties.

#### Why it exists / why it matters

UI state, JSON payloads, and caches are mostly objects holding primitives. Misunderstanding mutability causes shared-reference bugs.

#### Pros and cons

- **Pros:** primitives are cheap to compare by value (with caveats for `NaN`), easy to serialize.
- **Cons:** object identity surprises (`{}` !== `{}`).

#### What happens without it / when misused

- You “copy” an array by assignment and mutate both references.

#### Syntax and rules

```js
const name = "Ada"; // primitive string binding
const row = { id: 1, name }; // object binding
```

#### Examples

**Tiny — typeof distinguishes broad categories**

```js
typeof 2026; // "number"
typeof null; // "object" (legacy)
```

#### Quick checks

1. Is the string `"hello"` mutable character-by-character in JS?
2. Does `typeof []` return `"array"`?

---

## `typeof` and the `null` quirk

### What it is

`typeof` returns a string label for a value’s broad type category. **`typeof null === "object"`** is a long-standing language wart; real code often special-cases `null`.

#### Why it exists / why it matters

Defensive formatting and logging need stable rules (`null` vs real objects).

#### Syntax and rules

```js
function typeTag(v) {
  if (v === null) return "null";
  return typeof v;
}
```

#### Quick checks

1. What does `typeof NaN` return?
2. Why is `typeof null` misleading?

---

## `const`, `let`, and `var` (scoping + reassignment)

### What it is

- **`const`**: bind once; cannot reassign the binding (object contents can still mutate).
- **`let`**: block-scoped mutable binding.
- **`var`**: function-scoped (legacy); still appears in older codebases.

#### Why it exists / why it matters

Block scoping makes loops and `if` branches safer; `const` defaults communicate intent.

#### Pros and cons

- **Pros:** fewer accidental globals; TDZ catches some “use before declare” bugs.
- **Cons:** TDZ surprises newcomers; `const` objects still mutable.

#### What happens without it / when misused

- `var` inside loops creates one shared binding for all closures (classic interview trap).

#### Examples

**Tiny — loop closures**

```js
const fns = [];
for (let i = 0; i < 3; i += 1) {
  fns.push(() => i);
}
fns.map((fn) => fn()); // [0, 1, 2]
```

#### Quick checks

1. Does `const` freeze objects deeply?
2. What scope does `var` use inside a function?

---

## Template literals and tagged templates (intro)

### What it is

Template literals use backticks and `${expr}` interpolation. **Tagged templates** pass cooked/raw segments to a function—optional advanced topic; Day 17 only needs interpolation + multiline strings.

#### Why it exists / why it matters

Readable multi-line strings reduce concatenation bugs in logs, emails, and CLI output.

#### Syntax and rules

```js
const who = "team";
const msg = `Ship it, ${who}!
Next: monitor canaries.`;
```

#### Quick checks

1. Can template literals span multiple lines without `\n` escapes?
2. What delimiter defines a template literal?

---

## Coercion preview: why `==` scares maintainers

### What it is

JavaScript can implicitly convert values when operators expect another type. **`===`** avoids most surprises; still learn what `Number()`, `String()`, and edge cases like `""` do.

#### Why it exists / why it matters

Bugs from coercion show up in form validation, query parsing, and analytics counters.

#### Syntax and rules

Prefer:

```js
if (x === 0) {
}
```

over loose comparisons unless you have a documented reason.

#### Quick checks

1. What is `Number("")`?
2. What is `String(null)`?

---

## Common mistakes & debugging

- Treating `typeof` as a full runtime type system.
- Assuming `const` implies deep immutability.
- Concatenating numbers and strings accidentally in UI (`"Count: " + count` vs template).

---

## Further reading

- MDN: [JavaScript data types](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures)
- MDN: [`typeof`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/typeof)
- MDN: [`let`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let)
- MDN: [`const`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/const)
- MDN: [Template literals](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals)

---

## Glossary

| Term | Meaning |
|------|---------|
| Binding | Name→value association in a scope |
| Primitive | Non-object value type category |
| TDZ | Temporal dead zone before `let`/`const` init |
| Coercion | Implicit type conversion |

---

## Answers (self-test)

### Primitives vs objects

1. No—strings are immutable; operations return new strings.
2. No—arrays are objects; `typeof []` is `"object"`.

### typeof

1. `"number"` (`NaN` is still a number value in JS).
2. It suggests `null` is an object even though it is not a normal object instance.

### const/let/var

1. No—only the binding is constant; object properties can change unless frozen separately.
2. Function-scoped (not block-scoped like `let`).

### Templates

1. Yes—newlines in the template become newline characters in the string.
2. Backticks `` ` ``.

### Coercion

1. `0`
2. `"null"`
