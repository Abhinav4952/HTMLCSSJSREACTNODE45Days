# Task 2 — Timed Round 2 (60 min): Spring + JPA Bug Hunt

**Day:** 50 · **Task ID:** Day50-task02 · **Type:** Spring Boot (JPA) · **Difficulty:** Timed

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

A handed-over service with three seeded defects and one missing method. Diagnose with the failing tests, fix each root cause, finish `reserve`. Start a 60-minute timer.

## Learning goals

- Debug unfamiliar code from failing tests
- Spot classic defects: off-by-one, integer division, unnormalised input
- Write a small transactional service method

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day50/task02/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day50/task02/Product.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day50/task02/ProductRepository.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day50/task02/ProductService.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day50/task02/ProductServiceTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 50 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Fix BUG-1 (comparison), BUG-2 (integer math + validation) and BUG-3 (input normalisation).
2. Implement `reserve` per the Javadoc SPEC (transactional, validated, no partial change).
3. Do not change the tests.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day50-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day50-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 50: complete task-02-timed-spring-jpa-bug-hunt-60min`.

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
| `ProductService.java` | `Day50-task02` | BUG-1 - something about this comparison does not match the spec |
| `ProductService.java` | `Day50-task02` | BUG-2 - integer division strikes again; also validate the range |
| `ProductService.java` | `Day50-task02` | BUG-3 - lookup does not normalise the input |
| `ProductService.java` | `Day50-task02` | implement reserve according to the SPEC |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `seed` |
| 2 | `lowStockIsStrictlyBelowThreshold` |
| 3 | `discountUsesIntegerPercentMath` |
| 4 | `discountRejectsOutOfRangePercent` |
| 5 | `skuLookupIgnoresCaseAndWhitespace` |
| 6 | `reserveReducesStock` |
| 7 | `reserveRejectsBadRequestsWithoutChangingStock` |
| 8 | `reservingExactlyTheStockIsAllowed` |

## Edge cases to handle

- Boundary value for `lowStock`.
- Rounding down in the discount.
- Null SKU.
- Failed reservation must not decrease stock.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 50: Timed Round 2 (60 min): Spring + JPA Bug Hunt`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the failing assertion first; reproduce in your head before editing.
</details>

<details><summary>Hint 2</summary>
`sku.trim().toUpperCase(Locale.ROOT)`.
</details>
