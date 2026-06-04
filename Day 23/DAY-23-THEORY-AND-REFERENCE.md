# Day 23 — Advanced Expressions: Hoisting, Comparisons, Coercion

**Primary theme:** Equality (`==`, `===`, `Object.is`), truthiness, relational comparisons, and coercion-aware utilities  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Related tasks:** `task-01-equality-and-samevalue-lab`, `task-02-truthiness-and-nullish-defaults`, `task-03-comparison-and-relationals`, `task-04-coercion-safety-kit-challenge`  
**Instruction alignment:** Maps to *Advanced expressions: hoisting, automatic type conversions, comparisons (`==` vs `===`, edge cases)* from the master topic list.

---

## Overview

JavaScript comparisons are not “one operator fits all.” **`===`** checks types first; **`==`** applies a set of coercion rules many teams ban outright; **`Object.is`** fixes two `===` oddities (`NaN` and signed zero). Day 23 makes these distinctions **mechanical**: you should be able to predict edge cases, justify defaults with **`??`**, and write helpers that stop accidental string/number mixing.

---

## Day roadmap

1. [Strict equality `===`](#strict-equality-)
2. [Loose equality `==` (know the rules, still avoid in app code)](#loose-equality--know-the-rules-still-avoid-in-app-code)
3. [`Object.is` and `SameValue`](#objectis-and-samevalue)
4. [Truthiness and nullish coalescing `??`](#truthiness-and-nullish-coalescing-)
5. [Numeric coercion and `+` surprises](#numeric-coercion-and--surprises)
6. [Relational comparisons with strings](#relational-comparisons-with-strings)
7. [Common mistakes & debugging](#common-mistakes--debugging)
8. [Further reading](#further-reading)
9. [Glossary](#glossary)
10. [Answers (self-test)](#answers-self-test)

---

## Strict equality `===`

### What it is

**Strict equality** returns `true` only when types match and values match per language rules (with the usual `NaN` never equal to itself under `===`).

#### Why it exists / why it matters

Most production codebases standardize on `===` to avoid coercion-driven bugs.

#### Pros and cons

- **Pros:** predictable; easy to reason about in reviews.
- **Cons:** still has `NaN` and `+0`/`-0` quirks compared to `Object.is`.

#### Syntax and rules

```js
1 === "1"; // false
Number.isNaN(x); // preferred NaN check
```

#### Examples

```js
function isDefined(v) {
  return v !== undefined && v !== null;
}
```

#### Quick checks

1. What is `undefined === null`?

---

## Loose equality `==` (know the rules, still avoid in app code)

### What it is

**Loose equality** allows coercion across types following ECMAScript’s abstract operation rules.

#### Why it exists / why it matters

You still read it in older snippets and some minified code; interviews may probe it.

#### Pros and cons

- **Pros:** occasionally convenient for `null`/`undefined` collapsing with `x == null` (checks both).
- **Cons:** hard to review; easy to introduce subtle bugs.

#### Examples

```js
null == undefined; // true
"" == 0; // true
```

#### Quick checks

1. Is `[] == false` true?

---

## `Object.is` and `SameValue`

### What it is

`Object.is(a, b)` compares with **SameValue** semantics: like `===` but treats `NaN` as equal to `NaN`, and distinguishes `+0` vs `-0`.

#### Why it exists / why it matters

Useful for memoization keys and geometry kernels where signed zero matters.

#### Examples

```js
Object.is(NaN, NaN); // true
Object.is(0, -0); // false
```

#### Quick checks

1. Does `===` treat `-0` and `0` as equal?

---

## Truthiness and nullish coalescing `??`

### What it is

**Truthy/falsy** values drive `if`/`&&`/`||`. **`??`** defaults only for `null` or `undefined`.

#### Why it exists / why it matters

`||` defaults incorrectly when `0`, `""`, or `false` are valid values.

#### Examples

```js
const port = cfg.port ?? 8080;
const name = input || "anon"; // beware: "" becomes anon
```

#### Quick checks

1. What is `0 ?? 1`?

---

## Numeric coercion and `+` surprises

### What it is

The binary `+` operator prefers string concatenation if either operand is a string; otherwise numeric addition.

#### Examples

```js
1 + "2"; // "12"
1 + Number("2"); // 3
```

#### Quick checks

1. What is `[] + []`?

---

## Relational comparisons with strings

### What it is

`<`/`>` compare strings lexicographically **as strings**, not numerically, unless both convert to numbers successfully in the given expression form—relational comparisons can coerce mixed operands.

#### Examples

```js
"2" > "12"; // true (string compare)
```

#### Quick checks

1. How do you safely compare numeric strings as numbers?

---

## Common mistakes & debugging

- Using `==` “just this once.”
- Using `||` to default when `0`/`false`/`""` are meaningful.
- Comparing decimal fractions with `===` after math without rounding strategy.

---

## Further reading

- MDN: [Equality comparisons](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness)
- MDN: [`Object.is`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is)
- MDN: [Nullish coalescing](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing)

---

## Glossary

| Term | Meaning |
|------|---------|
| **SameValue** | Spec-defined equality used by `Object.is`. |
| **Falsy** | Values treated as false in boolean contexts (`0`, `""`, `NaN`, etc.). |

---

## Answers (self-test)

1. `undefined === null` → `false`.
2. `[] == false` → `true` (`[]` coerces to `0`).
3. `===` treats `0` and `-0` as equal (`true`).
4. `0 ?? 1` → `0`.
5. `[] + []` → `""` (both become `""`).
6. Use `Number(x)` / `parseInt` with radix / `BigInt` as appropriate—never rely on chained relational coercion for business logic.
