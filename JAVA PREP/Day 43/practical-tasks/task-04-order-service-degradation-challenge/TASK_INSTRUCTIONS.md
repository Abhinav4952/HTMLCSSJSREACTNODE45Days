# Task 4 — Order Service with Graceful Degradation (Challenge)

**Day:** 43 · **Task ID:** Day43-task04 · **Type:** Java · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Combine retry and fallback in an order service: transient inventory failures are retried, permanent ones degrade to a PENDING order instead of an error.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day43/task04/InventoryPort.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day43/task04/InventoryUnavailableException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day43/task04/OrderResult.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day43/task04/OrderService.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day43/task04/OrderServiceTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 43 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Validate quantity.
2. Retry only `InventoryUnavailableException`, at most `maxAttempts` total calls.
3. Map stock levels to `CONFIRMED` / `REJECTED_OUT_OF_STOCK`.
4. Return `PENDING_INVENTORY_UNAVAILABLE` when all attempts failed.
5. Let unexpected exceptions bubble up unchanged.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day43-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day43-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 43: complete task-04-order-service-degradation-challenge`.

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
| `OrderService.java` | `Day43-task04` | implement the rules above (hand-written loop or Resilience4j Retry |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `confirmsWhenStockIsSufficient` |
| 2 | `rejectsWithoutRetryWhenStockIsTooLow` |
| 3 | `retriesTransientFailures` |
| 4 | `degradesToPendingWhenInventoryStaysDown` |
| 5 | `otherExceptionsPropagateImmediately` |
| 6 | `rejectsNonPositiveQuantity` |

## Edge cases to handle

- `maxAttempts` of 1 means no retry.
- Out-of-stock is a business answer, not a failure: never retried.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 43: Order Service with Graceful Degradation (Challenge)`

## Hints (optional)

<details><summary>Hint 1</summary>
A plain `for` loop is enough; Resilience4j is optional.
</details>

<details><summary>Hint 2</summary>
Think: which outcomes are failures and which are valid business results?
</details>
