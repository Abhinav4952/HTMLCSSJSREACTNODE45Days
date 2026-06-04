# Day 20 — Arrays: Methods, Searching, and a Light `reduce`

**Primary theme:** Higher-order array methods as a toolkit—plus a careful introduction to `reduce`  
**Estimated study time:** 2–3 hours theory + 4–7 hours tasks  
**Related tasks:** `task-01-filter-map-pipeline`, `task-02-sort-comparator-lab`, `task-03-reduce-ledger-lite`, `task-04-array-search-and-slice`  
**Instruction alignment:** Maps to *Arrays: built-in methods including sort, filter, map, reduce (intro reduce lightly); searching* from the master topic list.

---

## Overview

Arrays are lists, stacks, queues, tables, timelines, and UI rows—often all at once. JavaScript’s array helpers encourage **expression-oriented** code: describe *what* you want (`filter`, `map`) instead of manually indexing (`for` with `i++`). The sharp edges are **mutators** (`sort`, `splice`, `reverse`) that rearrange **in place**, and **`reduce`**, which can become unreadable if you force everything through one accumulator.

Day 20 practices safe pipelines, explicit sorting rules, a small ledger `reduce`, and predictable searching.

---

## Day roadmap

1. [Non-mutating transforms: `map`, `filter`, `slice`, `concat`](#non-mutating-transforms-map-filter-slice-concat)
2. [Mutating methods: `sort`, `splice`, `reverse` (know the cost)](#mutating-methods-sort-splice-reverse-know-the-cost)
3. [Comparators and stable expectations](#comparators-and-stable-expectations)
4. [`reduce` as aggregation (use sparingly at first)](#reduce-as-aggregation-use-sparingly-at-first)
5. [Searching: `find`, `findIndex`, `includes`, `indexOf`](#searching-find-findindex-includes-indexof)
6. [Common mistakes & debugging](#common-mistakes--debugging)
7. [Further reading](#further-reading)
8. [Glossary](#glossary)
9. [Answers (self-test)](#answers-self-test)

---

## Non-mutating transforms: `map`, `filter`, `slice`, `concat`

### What it is

`map`/`filter` return **new arrays**. `slice` copies a contiguous range. `concat` combines without mutating inputs.

#### Why it exists / why it matters

Fewer shared-mutation bugs when passing arrays through React state later.

#### Quick checks

1. Does `filter` mutate the original array?

---

## Mutating methods: `sort`, `splice`, `reverse` (know the cost)

### What it is

`Array.prototype.sort` sorts **in place** and returns the same array reference.

#### Why it exists / why it matters

Sorting is easy to get subtly wrong without an explicit comparator.

#### Quick checks

1. Why is `sort()` dangerous for numbers?

---

## Comparators and stable expectations

### What it is

A comparator `(a, b) => number` returns `<0`, `0`, or `>0` to order elements.

#### Examples

```js
[10, 2, 1].sort((a, b) => a - b);
```

#### Quick checks

1. What comparator sorts ascending numerically?

---

## `reduce` as aggregation (use sparingly at first)

### What it is

`reduce` walks an array and carries an accumulator forward.

#### Why it exists / why it matters

Great for sums and grouping—terrible as a general-purpose loop replacement when readability suffers.

#### Quick checks

1. What is a good “first reduce” problem?

---

## Searching: `find`, `findIndex`, `includes`, `indexOf`

### What it is

Linear searches locate values or predicates matches; `includes` checks membership with `SameValueZero` semantics (notably for `NaN`).

#### Quick checks

1. What does `findIndex` return when nothing matches?

---

## Common mistakes & debugging

- Forgetting `return` inside `map` callbacks.
- Using `sort()` without comparator on numeric data.
- Confusing `map`/`filter` performance with algorithmic complexity (still linear passes).

---

## Further reading

- MDN: [`Array.prototype.map`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map)
- MDN: [`Array.prototype.filter`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter)
- MDN: [`Array.prototype.reduce`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce)
- MDN: [`Array.prototype.sort`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort)

---

## Glossary

| Term | Meaning |
|------|---------|
| Comparator | Function controlling sort order |
| Predicate | Function returning boolean for selection |
| Accumulator | `reduce` running state |

---

## Answers (self-test)

### Non-mutating transforms

1. No—`filter` returns a new array.

### Mutating methods

1. Default lexicographic sort treats numbers like strings (`"10"` before `"2"`-style surprises).

### Comparators

1. `(a, b) => a - b` for ascending numeric.

### reduce

1. Summing numbers or counting occurrences.

### Searching

1. `-1` for `findIndex` / `indexOf` when not found (per method docs).
