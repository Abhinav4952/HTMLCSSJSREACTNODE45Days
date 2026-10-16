# Day 14 — Collections I: List, ArrayList, LinkedList, Iterator, Comparable and Comparator

## Learning objectives

- Explain the `Collection` / `List` contract and the cost model of `ArrayList` versus `LinkedList`
- Use `Iterator` and `ListIterator` to remove or insert while traversing, and explain fail-fast `ConcurrentModificationException`
- Avoid the `List.remove(int)` vs `remove(Object)` overload trap
- Implement `Comparable` consistently with `equals` and `hashCode`
- Build multi-key sort orders with `Comparator.comparing(...).thenComparing(...)`, `reversed`, and `nullsLast`
- Distinguish unmodifiable views, `Arrays.asList`, and `List.of`

## Prerequisites

- Day 13 — generics (collections are generic types)
- Day 08–09 — `equals`/`hashCode` and interfaces

## How to use this folder

1. Read [`DAY-14-THEORY-AND-REFERENCE.md`](DAY-14-THEORY-AND-REFERENCE.md) first.
2. Open each task folder under `practical-tasks/` as its own Maven project in IntelliJ.
3. Run `mvn test` (**red**), implement the `TODO(Day14-taskYY)` stubs, run `mvn test` again until **green**.
4. Do not edit tests, `TASK_INSTRUCTIONS.md`, or `EVALUATION_CRITERIA.md`.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-list-ops` | Plain Java | `mvn test` |
| 2 | `task-02-iterator-remove` | Plain Java | `mvn test` |
| 3 | `task-03-comparable-product` | Plain Java | `mvn test` |
| 4 | `task-04-comparator-chain` | Plain Java | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Core Java
