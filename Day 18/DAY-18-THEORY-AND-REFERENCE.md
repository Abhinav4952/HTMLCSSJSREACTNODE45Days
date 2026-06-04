# Day 18 — Expressions, Operators, and Control Flow

**Primary theme:** Decision trees, loops, `switch`, and truthiness discipline  
**Estimated study time:** 2–3 hours theory + 4–7 hours tasks  
**Related tasks:** `task-01-conditional-branching-lab`, `task-02-loop-aggregation-lab`, `task-03-switch-http-status-router`, `task-04-truthiness-normalizer`  
**Instruction alignment:** Maps to *Expressions, operators, statements; literals; conditions; loops* from the master topic list.

---

## Overview

Control flow is where “small syntax mistakes” become “wrong invoices” and “infinite loops.” Day 18 focuses on **explicitness**: make invalid states unrepresentable where possible, prefer **`===`**, and treat `switch` as a **table lookup** with disciplined `break`/`return`.

---

## Day roadmap

1. [Conditionals: guard clauses vs nested `if`](#conditionals-guard-clauses-vs-nested-if)
2. [Loops: `for`, `while`, and collection iteration](#loops-for-while-and-collection-iteration)
3. [`switch` and fall-through hazards](#switch-and-fall-through-hazards)
4. [Truthiness vs strict checks](#truthiness-vs-strict-checks)
5. [Common mistakes & debugging](#common-mistakes--debugging)
6. [Further reading](#further-reading)
7. [Glossary](#glossary)
8. [Answers (self-test)](#answers-self-test)

---

## Conditionals: guard clauses vs nested `if`

### What it is

**Guard clauses** return early from invalid states, keeping the “happy path” unindented. Deep nesting often hides bugs.

#### Why it exists / why it matters

Readable branching reduces merge conflicts and review time.

#### Examples

```js
function divide(a, b) {
  if (b === 0) return null;
  return a / b;
}
```

#### Quick checks

1. Name one advantage of guard clauses.

---

## Loops: `for`, `while`, and collection iteration

### What it is

Loops repeat work: indexed `for`, open-ended `while`, and collection-driven `for..of` (ES2015 preview for later days).

#### Why it exists / why it matters

Choosing the wrong loop shape invites off-by-one errors and accidental quadratic work.

#### Quick checks

1. When is `while` preferable to `for`?

---

## `switch` and fall-through hazards

### What it is

`switch` compares a value against `case` labels using **strict equality** semantics (`===`) for matching.

#### What happens without it / when misused

Missing `break` causes fall-through—sometimes intentional, usually a bug.

#### Quick checks

1. Does `switch` use `===` matching?

---

## Truthiness vs strict checks

### What it is

Truthiness uses `ToBoolean` in `if`, `while`, `&&`, `||`. Strict checks compare values without coercion (`===`).

#### Why it exists / why it matters

`0` and `""` are falsy but often valid domain values.

#### Quick checks

1. Is `[]` truthy or falsy?

---

## Common mistakes & debugging

- Accidental semicolon after `return` causing `undefined` returns.
- Infinite `while` without advancing state.
- Treating `switch` like pattern matching for complex shapes—sometimes `if` or a map is clearer.

---

## Further reading

- MDN: [`if...else`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/if...else)
- MDN: [`for`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for)
- MDN: [`while`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/while)
- MDN: [`switch`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/switch)

---

## Glossary

| Term | Meaning |
|------|---------|
| Guard clause | Early return for invalid state |
| Fall-through | Continuing into the next `switch` case without `break` |
| Truthiness | Boolean coercion in boolean contexts |

---

## Answers (self-test)

### Conditionals

1. Shallower nesting; clearer happy path; easier testing.

### Loops

1. When stop condition is not inherently counting steps, or when waiting on external state (still must advance).

### switch

1. Yes—`case` matches with `===` (after special `switch` compilation rules).

### Truthiness

1. Truthy (`ToBoolean([])` is `true`).
