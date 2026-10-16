# Task 4 — Edge Gateway: API Key + Rate Limit (Challenge)

**Day:** 44 · **Task ID:** Day44-task04 · **Type:** Java · **Difficulty:** Challenge

## Summary

Assemble a small gateway: route lookup, API-key authentication filter and a fixed-window rate limiter, all as ordered filters.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day44/task04/GatewayRequest.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task04/GatewayResponse.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task04/Handler.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task04/GatewayFilter.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task04/Route.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task04/RouteLocator.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task04/FilterChain.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task04/ApiKeyFilter.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day44/task04/RateLimitFilter.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day44/task04/Gateway.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day44/task04/GatewayTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 44 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. `ApiKeyFilter`: 401 for missing/unknown keys, otherwise continue.
2. `RateLimitFilter`: per-client fixed window using the injected `Clock`; 429 when exceeded.
3. `Gateway.handle`: 404 for unknown route, 502 when no backend, else filters around backend.
4. Filter order matters: authentication happens before rate limiting.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day44-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day44-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 44: complete task-04-gateway-auth-rate-limit-challenge`.

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
| `ApiKeyFilter.java` | `Day44-task04` | check the X-API-Key header against validKeys |
| `RateLimitFilter.java` | `Day44-task04` | look up/create the client's window, reset if expired, count, and allow or answer 429 |
| `Gateway.java` | `Day44-task04` | use locator.match, backendsByRouteId and FilterChain.build |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `validKeyReachesBackend` |
| 3 | `missingOrWrongKeyIs401` |
| 4 | `unknownRouteIs404EvenWithoutKey` |
| 5 | `routeWithoutBackendIs502` |
| 6 | `thirdRequestInWindowIs429` |
| 7 | `limitsAreTrackedPerClient` |
| 8 | `windowResetsAfterItElapses` |
| 9 | `rejectedRequestsDoNotConsumeRateLimit` |

## Edge cases to handle

- Window expiry.
- Anonymous clients.
- Unauthenticated requests must not consume quota.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 44: Edge Gateway: API Key + Rate Limit (Challenge)`

## Hints (optional)

<details><summary>Hint 1</summary>
`clock.millis()` gives the current time; compare with the window start.
</details>

<details><summary>Hint 2</summary>
`FilterChain.build` and `RouteLocator` are provided.
</details>
