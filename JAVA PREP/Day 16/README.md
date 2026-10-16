# Day 16 — Lambdas, Functional Interfaces, Method References, and Optional

## Learning objectives

- Write lambda expressions and explain what a functional interface (SAM type) is
- Use the core `java.util.function` types: `Predicate`, `Function`, `Supplier`, `Consumer`, `UnaryOperator`, `BiFunction`, and primitive specializations
- Explain variable capture and the *effectively final* rule, including the loop-variable pitfall
- Choose among the four kinds of method references and rewrite lambdas as method references
- Compose behavior with `andThen`, `compose`, `and`, `or`, `negate`
- Use `Optional` correctly (`map`, `flatMap`, `orElseGet`, `orElseThrow`) and avoid its misuses

## Prerequisites

- Day 13 — generics (`Function<? super T, ? extends R>`)
- Day 14–15 — collections and comparators
- Day 10 — interfaces and anonymous classes

## How to use this folder

1. Read [`DAY-16-THEORY-AND-REFERENCE.md`](DAY-16-THEORY-AND-REFERENCE.md) first.
2. Open each task folder under `practical-tasks/` as its own Maven project in IntelliJ.
3. Run `mvn test` (**red**), implement the `TODO(Day16-taskYY)` stubs, run `mvn test` again until **green**.
4. Do not edit tests, `TASK_INSTRUCTIONS.md`, or `EVALUATION_CRITERIA.md`.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-lambda-filter` | Plain Java | `mvn test` |
| 2 | `task-02-predicate-compose` | Plain Java | `mvn test` |
| 3 | `task-03-optional-chain` | Plain Java | `mvn test` |
| 4 | `task-04-method-ref-map` | Plain Java | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Core Java
