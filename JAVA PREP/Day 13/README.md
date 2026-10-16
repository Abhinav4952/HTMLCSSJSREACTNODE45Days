# Day 13 — Generics: Classes, Methods, Bounds, and Wildcards (PECS)

## Learning objectives

- Declare and use generic classes and generic methods with correct type-parameter naming
- Explain type erasure and what it forbids (`new T()`, `instanceof List<String>`, generic arrays)
- Apply bounded type parameters (`extends`, intersection bounds) to express capabilities
- Choose between `? extends`, `? super`, and unbounded `?` using the PECS rule
- Implement a small generic data structure (stack) that is safe for callers and iterable
- Read generic compiler errors and fix them without raw types or blind casts

## Prerequisites

- Day 06–10 — classes, interfaces, inheritance, and polymorphism
- Day 12 — wrappers/autoboxing (generics work only with reference types)

## How to use this folder

1. Read [`DAY-13-THEORY-AND-REFERENCE.md`](DAY-13-THEORY-AND-REFERENCE.md) first.
2. Open each task folder under `practical-tasks/` as its own Maven project in IntelliJ.
3. Run `mvn test` (**red**), implement the `TODO(Day13-taskYY)` stubs, run `mvn test` again until **green**.
4. Do not edit tests, `TASK_INSTRUCTIONS.md`, or `EVALUATION_CRITERIA.md`.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-box-generic` | Plain Java | `mvn test` |
| 2 | `task-02-bounded-max` | Plain Java | `mvn test` |
| 3 | `task-03-pecs-copy` | Plain Java | `mvn test` |
| 4 | `task-04-generic-stack` | Plain Java | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Core Java
