# Task 2 — RestClient Basics with MockRestServiceServer

**Day:** 36 · **Task ID:** Day36-task02 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Call an HTTP API with Spring 6.1's fluent RestClient: base URL, default header, status handling, generic lists and JSON posts.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day36/task02/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day36/task02/Quote.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day36/task02/QuoteServiceException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day36/task02/QuoteClient.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day36/task02/QuoteClientTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 36 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Configure the builder with base URL and `X-Api-Key`.
2. Implement `find` (404 -> empty, 5xx -> domain exception), `list` and `create`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day36-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day36-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 36: complete task-02-rest-client-basics`.

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
| `QuoteClient.java` | `Day36-task02` | builder.baseUrl(baseUrl).defaultHeader X-Api-Key then build |
| `QuoteClient.java` | `Day36-task02` | retrieve with onStatus handlers; map 404 to empty |
| `QuoteClient.java` | `Day36-task02` | GET and read a List<Quote> |
| `QuoteClient.java` | `Day36-task02` | POST a body as JSON and read the Quote |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `findSendsApiKeyAndMapsJson` |
| 3 | `notFoundBecomesEmpty` |
| 4 | `serverErrorBecomesDomainException` |
| 5 | `listReadsGenericCollection` |
| 6 | `createPostsJsonBody` |

## Edge cases to handle

- Without `onStatus`, 4xx/5xx raise `HttpClientErrorException`/`HttpServerErrorException`.
- Generic collections need `ParameterizedTypeReference`.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 36: RestClient Basics with MockRestServiceServer`

## Hints (optional)

<details><summary>Hint 1</summary>
`MockRestServiceServer.bindTo(builder)` intercepts calls without a network.
</details>

<details><summary>Hint 2</summary>
Never use real network calls in unit tests.
</details>
