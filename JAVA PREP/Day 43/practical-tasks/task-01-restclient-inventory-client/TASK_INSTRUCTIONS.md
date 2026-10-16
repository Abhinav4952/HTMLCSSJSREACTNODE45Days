# Task 1 — RestClient Inventory Client

**Day:** 43 · **Task ID:** Day43-task01 · **Type:** Spring Boot · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Implement a service-to-service client with Spring's `RestClient`. The downstream service is simulated in-process with `MockRestServiceServer`, so no network or Docker is needed.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day43/task01/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day43/task01/InventoryClient.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day43/task01/StockResponse.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day43/task01/InventoryUnavailableException.java` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day43/task01/InventoryClientTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 43 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `availableStock(sku)` with `restClient.get().uri("/inventory/{sku}", sku)`.
2. Return the `available` count wrapped in `Optional` for 200 responses.
3. Return `Optional.empty()` for HTTP 404.
4. Throw `InventoryUnavailableException` for 5xx responses and for I/O failures (`ResourceAccessException`).
5. Use a URI template variable so the SKU is encoded for you (never concatenate strings).

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day43-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day43-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 43: complete task-01-restclient-inventory-client`.

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
| `InventoryClient.java` | `Day43-task01` | use restClient.get().uri("/inventory/{sku}", sku).retrieve()...body(StockResponse.class |
| `InventoryClient.java` | `Day43-task01` | map 404, 5xx and ResourceAccessException as described above |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `returnsAvailableStockOnSuccess` |
| 3 | `unknownSkuIsEmpty` |
| 4 | `serverErrorBecomesInventoryUnavailable` |
| 5 | `ioFailureBecomesInventoryUnavailable` |
| 6 | `skuIsUriEncoded` |

## Edge cases to handle

- SKU containing a space must be percent-encoded.
- A 4xx other than 404 may propagate (document your choice).
- Keep the original exception as `cause`.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 43: RestClient Inventory Client`

## Hints (optional)

<details><summary>Hint 1</summary>
`HttpClientErrorException.NotFound` and `HttpServerErrorException` are thrown by default for 4xx/5xx.
</details>

<details><summary>Hint 2</summary>
`ResourceAccessException` wraps `IOException`.
</details>

<details><summary>Hint 3</summary>
`.onStatus(...)` lets you convert statuses without try/catch.
</details>
