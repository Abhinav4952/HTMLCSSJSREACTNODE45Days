# Day 18 — Streams II: groupingBy, partitioningBy, flatMap, Primitive Streams, and Parallel Cautions

## Learning objectives

- Group and aggregate with `Collectors.groupingBy` and downstream collectors (`counting`, `summingX`, `averagingX`, `mapping`, `maxBy`, `collectingAndThen`)
- Split data in two with `partitioningBy` and explain how it differs from `groupingBy`
- Flatten nested collections with `flatMap`, `flatMapToInt`, and `mapMulti` awareness
- Use `IntStream`, `LongStream`, `DoubleStream`, ranges, and boxing conversions
- State the rules for safe parallel streams (stateless, non-interfering, associative) and list their performance cautions
- Choose deterministic result types (`TreeMap`, `LinkedHashMap`) for tests and APIs

## Prerequisites

- Day 17 — stream pipelines, reduce, collectors
- Day 15 — maps and ordering
- Day 16 — Optional and functional interfaces

## How to use this folder

1. Read [`DAY-18-THEORY-AND-REFERENCE.md`](DAY-18-THEORY-AND-REFERENCE.md) first.
2. Open each task folder under `practical-tasks/` as its own Maven project in IntelliJ.
3. Run `mvn test` (**red**), implement the `TODO(Day18-taskYY)` stubs, run `mvn test` again until **green**.
4. Do not edit tests, `TASK_INSTRUCTIONS.md`, or `EVALUATION_CRITERIA.md`.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-group-by-dept` | Plain Java | `mvn test` |
| 2 | `task-02-partition-even` | Plain Java | `mvn test` |
| 3 | `task-03-flatmap-orders` | Plain Java | `mvn test` |
| 4 | `task-04-parallel-safe-note` | Plain Java | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Core Java
