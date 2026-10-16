# Task 4 — HTTP Gateway: Retry, Fallback and Headers

**Day:** 36 · **Task ID:** Day36-task04 · **Type:** Spring Boot · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Wrap a remote API behind a Spring-managed gateway: query building, fallback on 404, bounded retry on 5xx and response header access.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day36/task04/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day36/task04/Quote.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day36/task04/UpstreamException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day36/task04/QuoteGateway.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day36/task04/QuoteGatewayTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 36 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement all four gateway methods using the injected `RestClient`.
2. Retry exactly once on 5xx; never retry 4xx.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day36-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day36-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 36: complete task-04-quote-gateway-challenge`.

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
| `QuoteGateway.java` | `Day36-task04` | use uriBuilder with path /quotes and query param limit |
| `QuoteGateway.java` | `Day36-task04` | map 404 to fallback, 5xx to UpstreamException |
| `QuoteGateway.java` | `Day36-task04` | loop at most twice |
| `QuoteGateway.java` | `Day36-task04` | read headers from ResponseEntity |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `reset` |
| 2 | `verify` |
| 3 | `allUsesQueryParameter` |
| 4 | `fallbackOn404` |
| 5 | `textOnSuccess` |
| 6 | `serverErrorBecomesUpstreamException` |
| 7 | `retryRecoversFromOneFailure` |
| 8 | `retryGivesUpAfterTwoAttempts` |
| 9 | `etagIsReadFromHeaders` |
| 10 | `missingEtagIsEmpty` |

## Edge cases to handle

- Build URIs with `uriBuilder`, never string concatenation.
- `toBodilessEntity()` still exposes headers and status.
- Retry loops must be bounded.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 36: HTTP Gateway: Retry, Fallback and Headers`

## Hints (optional)

<details><summary>Hint 1</summary>
`@RestClientTest` provides a `MockRestServiceServer` bound to the auto-configured `RestClient.Builder`.
</details>

<details><summary>Hint 2</summary>
Throw from `onStatus` to translate errors.
</details>
