# Task 3 — Index and EXPLAIN Notes

**Day:** 26 · **Task ID:** Day26-task03 · **Type:** Plain Java · **Difficulty:** Core

## Summary

Turn query shapes into recommended index DDL strings, decide whether a predicate can use a B-tree index, and classify an EXPLAIN plan.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day26/task03/IndexAdvisor.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day26/task03/IndexAdvisorTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 26 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `recommendIndex` (equality columns first, then range) and `recommendUniqueIndex` with the documented naming.
2. Implement `isIndexUsable` for leading-wildcard LIKE and function-wrapped columns.
3. Implement `classifyPlan` for H2-style plan text.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day26-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day26-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 26: complete task-03-index-explain-notes`.

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
| `IndexAdvisor.java` | `Day26-task03` | build the DDL string as documented above |
| `IndexAdvisor.java` | `Day26-task03` | build the unique-index DDL string |
| `IndexAdvisor.java` | `Day26-task03` | lower-case + trim the predicate and apply the two rules |
| `IndexAdvisor.java` | `Day26-task03` | classify the plan |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `compositeIndexPutsEqualityBeforeRange` |
| 2 | `rangeColumnIsOptional` |
| 3 | `onlyRangeColumn` |
| 4 | `nothingToIndexIsRejected` |
| 5 | `uniqueIndex` |
| 6 | `sargability` |
| 7 | `planClassification` |

## Edge cases to handle

- `rangeColumn == null` is allowed; no columns at all -> `IllegalArgumentException`.
- Predicate checks are case-insensitive and ignore surrounding whitespace.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 26: Index and EXPLAIN Notes`

## Hints (optional)

<details><summary>Hint 1</summary>
Column order in a composite index matters: equality predicates first, range last.
</details>

<details><summary>Hint 2</summary>
`String.join` builds the comma lists.
</details>
