# Task 2 — Filter Chain Composition

**Day:** 44 · **Task ID:** Day44-task02 · **Type:** Java · **Difficulty:** Core

## Summary

Compose gateway filters into a chain with pre/post phases and short-circuiting, the core idea behind Spring Cloud Gateway filters and servlet filters.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day44/task02/GatewayRequest.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task02/GatewayResponse.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task02/Handler.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task02/GatewayFilter.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day44/task02/FilterChain.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day44/task02/FilterChainTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 44 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Build a `Handler` that runs filters in list order (pre) and reverse order (post).
2. Allow a filter to short-circuit by not calling `next`.
3. An empty list returns the terminal handler behavior.
4. Copy the filter list when building.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day44-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day44-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 44: complete task-02-filter-chain`.

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
| `FilterChain.java` | `Day44-task02` | compose the filters around the terminal handler (hint: iterate backwards |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `filtersWrapTheTerminalInOrder` |
| 2 | `emptyChainIsTheTerminal` |
| 3 | `filterCanShortCircuit` |
| 4 | `filterCanChangeTheRequestForLaterFilters` |
| 5 | `listIsCopiedAtBuildTime` |

## Edge cases to handle

- Short-circuit in the middle of the chain.
- List mutated after build.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 44: Filter Chain Composition`

## Hints (optional)

<details><summary>Hint 1</summary>
Wrap from the last filter to the first: `next = req -> filter.filter(req, next)`.
</details>
