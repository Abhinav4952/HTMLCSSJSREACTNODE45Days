# Task 1 — JDBC SELECT DAO

**Day:** 27 · **Task ID:** Day27-task01 · **Type:** Plain Java + JDBC (H2) · **Difficulty:** Warm-up

## Summary

Implement a read-only DAO with try-with-resources: findById, findAll and count against an H2 DataSource.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day27/task01/User.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day27/task01/UserDao.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day27/task01/UserDaoTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 27 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `findById`, `findAll` (ordered by id) and `count` using JDBC only.
2. Close every Connection, Statement and ResultSet with try-with-resources.
3. Wrap `SQLException` in an unchecked exception (e.g. `IllegalStateException`) — never swallow it.

## Constraints

- Java 21; plain JDBC/SQL only (no Spring, no Lombok); H2 2.3.232 in PostgreSQL mode is the only database.
- Do not edit test files or this document; edit only the places marked `TODO(Day27-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day27-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 27: complete task-01-jdbc-select-dao`.

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
| `UserDao.java` | `Day27-task01` | SELECT id, name, email FROM users WHERE id = ? using PreparedStatement |
| `UserDao.java` | `Day27-task01` | SELECT all users ordered by id; map each row with a private mapRow helper |
| `UserDao.java` | `Day27-task01` | SELECT COUNT(*) FROM users |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `exec` |
| 3 | `findsExistingUser` |
| 4 | `missingUserIsEmpty` |
| 5 | `findAllIsOrderedById` |
| 6 | `countsRows` |

## Edge cases to handle

- Missing id -> `Optional.empty()`, not null and not an exception.
- Empty table -> `findAll()` returns an empty list and `count()` returns 0.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 27: JDBC SELECT DAO`

## Hints (optional)

<details><summary>Hint 1</summary>
`ResultSet` columns can be read by name: `rs.getLong("id")`.
</details>

<details><summary>Hint 2</summary>
Extract a `mapRow(ResultSet)` helper to avoid duplication.
</details>
