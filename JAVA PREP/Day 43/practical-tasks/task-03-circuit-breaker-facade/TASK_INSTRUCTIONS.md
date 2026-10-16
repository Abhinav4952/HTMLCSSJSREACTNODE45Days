# Task 3 — Circuit Breaker Facade

**Day:** 43 · **Task ID:** Day43-task03 · **Type:** Java + Resilience4j · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Protect a failing downstream with a Resilience4j `CircuitBreaker`, fall back when it fails, and watch the CLOSED -> OPEN -> HALF_OPEN -> CLOSED life cycle.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day43/task03/BreakerFacade.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day43/task03/BreakerFacadeTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 43 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Configure the breaker: COUNT_BASED window 4, minimum 4 calls, 50 % failure threshold, wait in OPEN = `openWait`, 1 permitted call in HALF_OPEN.
2. `call()` returns the downstream value or `"FALLBACK"` for any failure and for `CallNotPermittedException`.
3. While OPEN the downstream supplier must not be invoked.
4. `state()` exposes the current `CircuitBreaker.State`.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day43-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day43-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 43: complete task-03-circuit-breaker-facade`.

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
| `BreakerFacade.java` | `Day43-task03` | create a CircuitBreakerConfig with the settings above and the CircuitBreaker |
| `BreakerFacade.java` | `Day43-task03` | decorate the supplier, catch failures (including CallNotPermittedException) and return the fallback |
| `BreakerFacade.java` | `Day43-task03` | expose the breaker state |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `opensAfterFourFailuresAndStopsCallingDownstream` |
| 2 | `recoversThroughHalfOpenWhenDownstreamIsHealthyAgain` |
| 3 | `staysClosedBelowTheFailureThreshold` |
| 4 | `healthyCallsReturnTheRealValue` |

## Edge cases to handle

- Transition OPEN -> HALF_OPEN happens on the first call after the wait elapsed.
- A single failure in a window of 4 stays below 50 %.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 43: Circuit Breaker Facade`

## Hints (optional)

<details><summary>Hint 1</summary>
`CircuitBreakerConfig.custom()` is the builder.
</details>

<details><summary>Hint 2</summary>
`CircuitBreaker.decorateSupplier(cb, supplier)` wraps the call.
</details>
