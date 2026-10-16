# Task 3 — Optimistic Locking and JPA Auditing

**Day:** 35 · **Task ID:** Day35-task03 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Detect lost updates with @Version and stamp entities automatically with @CreatedDate/@LastModifiedDate.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day35/task03/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day35/task03/AuditConfig.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day35/task03/Product.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day35/task03/ProductRepository.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day35/task03/StockService.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day35/task03/VersionAndAuditingTest.java` | Provided helper or test (do not edit) |
| `src/test/resources/application.properties` | Provided helper or test (do not edit) |

## Prerequisites

- Day 35 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Enable auditing (`@EnableJpaAuditing`) and register `AuditingEntityListener` on `Product`.
2. Annotate `version`, `createdAt`, `updatedAt`.
3. Implement `StockService`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day35-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day35-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 35: complete task-03-version-and-auditing`.

## How to run and verify

```bash
java -version   # 21.x
mvn -v          # 3.9+
mvn test        # expected RED at the start
mvn -Dtest=<TestClass> test
```

## TODO map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `AuditConfig.java` | `Day35-task03` | turn on JPA auditing for the application |
| `Product.java` | `Day35-task03` | register the auditing listener on the entity |
| `Product.java` | `Day35-task03` | optimistic locking version column |
| `Product.java` | `Day35-task03` | creation timestamp (not updatable |
| `Product.java` | `Day35-task03` | last modification timestamp |
| `StockService.java` | `Day35-task03` | save a new product and return it |
| `StockService.java` | `Day35-task03` | load, apply delta with the rule, flush and return |
| `StockService.java` | `Day35-task03` | merge via repository.saveAndFlush |
| `StockService.java` | `Day35-task03` | load or throw |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `newProductStartsAtVersionZeroWithAuditTimestamps` |
| 2 | `everyUpdateBumpsVersionAndLastModified` |
| 3 | `staleDetachedCopyIsRejected` |
| 4 | `freshCopyCanBeSaved` |
| 5 | `businessRuleKeepsStockNonNegative` |

## Edge cases to handle

- A stale detached copy must raise `ObjectOptimisticLockingFailureException`.
- `createdAt` must never change on update (`updatable = false`).

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 35: Optimistic Locking and JPA Auditing`

## Hints (optional)

<details><summary>Hint 1</summary>
`@Version` can be `Long`, `Integer` or a timestamp; null means new.
</details>

<details><summary>Hint 2</summary>
Auditing needs both the listener and `@EnableJpaAuditing`.
</details>
