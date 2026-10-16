# Day 17 — Streams I: Pipelines, filter/map/reduce, and Collectors

## Learning objectives

- Describe a stream pipeline as source -> intermediate operations -> terminal operation and explain laziness and short-circuiting
- Use `filter`, `map`, `distinct`, `sorted`, `limit`, `skip`, `peek`, `findFirst`, `anyMatch` correctly
- Reduce streams with `reduce`, primitive streams (`IntStream`) and summary statistics
- Collect results with `Collectors.toList/toSet/toMap/joining/counting/collectingAndThen`
- Avoid stream anti-patterns: reuse, side effects in lambdas, `toMap` duplicate keys, `get()` on empty results
- Decide when a plain loop is clearer than a stream

## Prerequisites

- Day 16 — lambdas, functional interfaces, method references, Optional
- Day 14–15 — collections, comparators, maps

## How to use this folder

1. Read [`DAY-17-THEORY-AND-REFERENCE.md`](DAY-17-THEORY-AND-REFERENCE.md) first.
2. Open each task folder under `practical-tasks/` as its own Maven project in IntelliJ.
3. Run `mvn test` (**red**), implement the `TODO(Day17-taskYY)` stubs, run `mvn test` again until **green**.
4. Do not edit tests, `TASK_INSTRUCTIONS.md`, or `EVALUATION_CRITERIA.md`.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-stream-filter-map` | Plain Java | `mvn test` |
| 2 | `task-02-reduce-sum` | Plain Java | `mvn test` |
| 3 | `task-03-collectors-tolist` | Plain Java | `mvn test` |
| 4 | `task-04-challenge-word-count` | Plain Java | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Core Java
