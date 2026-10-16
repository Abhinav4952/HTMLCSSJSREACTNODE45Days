# Task 2 — GROUP BY and HAVING

**Day:** 26 · **Task ID:** Day26-task02 · **Type:** SQL script + JDBC test · **Difficulty:** Core

## Summary

Aggregate a `sales` table with COUNT/SUM/AVG, GROUP BY, HAVING and ORDER BY ... LIMIT.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day26/task02/SqlLab.java` | Stubs / starter code (edit the TODOs) |
| `sql/schema.sql` | Provided helper or test (do not edit) |
| `sql/seed.sql` | Provided helper or test (do not edit) |
| `sql/answers.sql` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day26/task02/GroupByTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 26 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Fill the five blocks in `sql/answers.sql`.
2. Use HAVING (not WHERE) for filters on aggregates.
3. Use deterministic ORDER BY clauses.

## Constraints

- Java 21; plain JDBC/SQL only (no Spring, no Lombok); H2 2.3.232 in PostgreSQL mode is the only database.
- Do not edit test files or this document; edit only the places marked `TODO(Day26-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day26-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 26: complete task-02-group-by-having`.

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
| `answers.sql` | `Day26-task02` | region, SUM(amount_cents) per region ORDER BY region |
| `answers.sql` | `Day26-task02` | region, COUNT(*) per region ORDER BY region |
| `answers.sql` | `Day26-task02` | regions (one column) whose total exceeds 10000 — use HAVING; ORDER BY region |
| `answers.sql` | `Day26-task02` | rep and total amount of the single best rep (GROUP BY rep, ORDER BY total DESC, LIMIT 1 |
| `answers.sql` | `Day26-task02` | average sale of region 'EU' rounded DOWN to a whole number (FLOOR, then CAST AS INT |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `tearDown` |
| 3 | `totalsByRegion` |
| 4 | `saleCountByRegion` |
| 5 | `havingFiltersGroups` |
| 6 | `topRep` |
| 7 | `averageIsRoundedDown` |

## Edge cases to handle

- Ties are not present in the data, but your ORDER BY must still be explicit.
- AVG of integers: the expected value is `4333` (13000 / 3 rounded down).

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 26: GROUP BY and HAVING`

## Hints (optional)

<details><summary>Hint 1</summary>
WHERE filters rows before grouping; HAVING filters groups after.
</details>

<details><summary>Hint 2</summary>
`SELECT rep, SUM(amount_cents) t ... ORDER BY t DESC LIMIT 1`.
</details>
