# Task 1 — Route Predicate Matching

**Day:** 44 · **Task ID:** Day44-task01 · **Type:** Java · **Difficulty:** Warm-up

## Summary

Simulate gateway route predicates: match request paths to routes by prefix with segment boundaries and longest-prefix-wins.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day44/task01/GatewayRequest.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task01/GatewayResponse.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task01/Handler.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task01/GatewayFilter.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task01/Route.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task01/RouteLocator.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day44/task01/RouteLocatorTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 44 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Ignore the query string when matching.
2. Match only on whole path segments (`/api/users` must not match `/api/usersX`).
3. Pick the route with the longest matching prefix.
4. Return `Optional.empty()` when nothing matches.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day44-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day44-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 44: complete task-01-route-matching`.

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
| `RouteLocator.java` | `Day44-task01` | strip the query string, filter matching routes (segment boundary!), pick the longest prefix |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `exactPrefixMatches` |
| 2 | `nestedPathMatches` |
| 3 | `longestPrefixWins` |
| 4 | `segmentBoundaryIsRespected` |
| 5 | `queryStringIsIgnored` |
| 6 | `unknownPathHasNoRoute` |

## Edge cases to handle

- Path equal to the prefix.
- Overlapping prefixes.
- Query strings.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 44: Route Predicate Matching`

## Hints (optional)

<details><summary>Hint 1</summary>
`Comparator.comparingInt(...)` with `Stream.max`.
</details>
