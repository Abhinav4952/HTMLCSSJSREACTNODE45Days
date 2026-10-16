# Task 3 — Mocking Collaborators with @MockitoBean

**Day:** 39 · **Task ID:** Day39-task03 · **Type:** Spring Boot (Testing) · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Test a service in isolation: stub with BDDMockito, capture arguments, verify absence of interactions, and simulate failures.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day39/task03/GatewayException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day39/task03/EmailGateway.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day39/task03/UserLookup.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day39/task03/NotificationService.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day39/task03/NotificationServiceTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 39 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `notifyUser` following the documented order of checks.
2. Implement `broadcast` so failures never abort the loop.
3. List which collaborators each test needs and why.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day39-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day39-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 39: complete task-03-mockbean-service`.

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
| `NotificationService.java` | `Day39-task03` | validate, look up the email, call the gateway, translate GatewayException to false |
| `NotificationService.java` | `Day39-task03` | loop over ids, count successes, skip unknown users |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `sendsToLookedUpEmail` |
| 2 | `blankMessageTouchesNothing` |
| 3 | `unknownUserNeverCallsGateway` |
| 4 | `gatewayFailureBecomesFalse` |
| 5 | `rejectedByProviderIsFalse` |
| 6 | `broadcastCountsOnlySuccessesAndKeepsGoing` |

## Edge cases to handle

- Validation failures must not touch collaborators (`verifyNoInteractions`).
- A provider returning false and a provider throwing both mean `false`.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 39: Mocking Collaborators with @MockitoBean`

## Hints (optional)

<details><summary>Hint 1</summary>
`@SpringBootTest(classes = ...)` builds a tiny context instead of scanning everything.
</details>

<details><summary>Hint 2</summary>
Unstubbed Mockito methods return defaults (false, empty Optional is NOT guaranteed for Optional in older versions: stub explicitly).
</details>
