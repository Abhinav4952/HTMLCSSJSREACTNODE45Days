# Day 15 — Collections II: Set, Map, HashMap Internals, Queue/Deque/PriorityQueue, and Immutable Collections

## Learning objectives

- Choose between `HashSet`, `LinkedHashSet`, `TreeSet` and between `HashMap`, `LinkedHashMap`, `TreeMap`
- Explain conceptually how `HashMap` works (hashCode, buckets, equals, load factor, resize, treeification)
- Write correct `equals`/`hashCode` and avoid mutable keys
- Use `merge`, `computeIfAbsent`, `getOrDefault`, and `entrySet` idiomatically
- Use `Queue`, `Deque`/`ArrayDeque`, and `PriorityQueue` (heap) for real problems
- Create defensive immutable copies with `List.copyOf`, `Map.copyOf`, `Set.copyOf` and understand unmodifiable *views*

## Prerequisites

- Day 14 — List, Iterator, Comparable/Comparator
- Day 08–09 — `equals` and `hashCode` contract

## How to use this folder

1. Read [`DAY-15-THEORY-AND-REFERENCE.md`](DAY-15-THEORY-AND-REFERENCE.md) first.
2. Open each task folder under `practical-tasks/` as its own Maven project in IntelliJ.
3. Run `mvn test` (**red**), implement the `TODO(Day15-taskYY)` stubs, run `mvn test` again until **green**.
4. Do not edit tests, `TASK_INSTRUCTIONS.md`, or `EVALUATION_CRITERIA.md`.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-unique-normalize` | Plain Java | `mvn test` |
| 2 | `task-02-frequency-map` | Plain Java | `mvn test` |
| 3 | `task-03-priority-queue-lab` | Plain Java | `mvn test` |
| 4 | `task-04-immutable-copy` | Plain Java | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Core Java
