# Task 3 — Strip-Prefix, Header and Rewrite Filters

**Day:** 44 · **Task ID:** Day44-task03 · **Type:** Java · **Difficulty:** Core

## Summary

Implement three classic gateway filters: StripPrefix, AddRequestHeader and RewritePath.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day44/task03/GatewayRequest.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task03/GatewayResponse.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task03/Handler.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task03/GatewayFilter.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task03/StripPrefixFilter.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day44/task03/AddRequestHeaderFilter.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day44/task03/RewritePathFilter.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day44/task03/BuiltInFiltersTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 44 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. `StripPrefixFilter` removes N leading segments and keeps the query string.
2. `AddRequestHeaderFilter` sets/overwrites a header.
3. `RewritePathFilter` applies a regex replacement to the path.
4. Every filter must call `next` with the modified request and return its response.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day44-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day44-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 44: complete task-03-header-and-rewrite-filters`.

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
| `StripPrefixFilter.java` | `Day44-task03` | split the path into segments, drop the first `parts`, rebuild the path (keep query string |
| `AddRequestHeaderFilter.java` | `Day44-task03` | add the header (overwrite an existing one) and continue the chain |
| `RewritePathFilter.java` | `Day44-task03` | apply String.replaceAll(regex, replacement) to the path and continue |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `stripOnePrefixSegment` |
| 2 | `stripTwoPrefixSegments` |
| 3 | `stripMoreThanAvailableLeavesRoot` |
| 4 | `stripKeepsQueryString` |
| 5 | `addHeaderSetsAndOverwrites` |
| 6 | `addHeaderReturnsDownstreamResponse` |
| 7 | `rewritePathWithNamedGroup` |
| 8 | `rewriteLeavesNonMatchingPathsAlone` |

## Edge cases to handle

- More segments than available.
- Header already present.
- Non-matching rewrite.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 44: Strip-Prefix, Header and Rewrite Filters`

## Hints (optional)

<details><summary>Hint 1</summary>
Split the query string off first, then work on `path.split("/")`.
</details>
