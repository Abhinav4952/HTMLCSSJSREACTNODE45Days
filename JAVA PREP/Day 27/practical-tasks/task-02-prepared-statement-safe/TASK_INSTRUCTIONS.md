# Task 2 — PreparedStatement and SQL Injection

**Day:** 27 · **Task ID:** Day27-task02 · **Type:** Plain Java + JDBC (H2) · **Difficulty:** Core

## Summary

Replace vulnerable string concatenation with PreparedStatement parameters, escape LIKE wildcards, and return generated keys.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day27/task02/User.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day27/task02/SafeSearchDao.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day27/task02/SafeSearchDaoTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 27 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `findByName` with a `?` placeholder.
2. Implement `findByNamePrefix` so `%` and `_` in user input are literal.
3. Implement `insertUser` returning the generated id.
4. Never concatenate user input into SQL (the provided `buildUnsafeSql` is the anti-example).

## Constraints

- Java 21; plain JDBC/SQL only (no Spring, no Lombok); H2 2.3.232 in PostgreSQL mode is the only database.
- Do not edit test files or this document; edit only the places marked `TODO(Day27-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day27-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 27: complete task-02-prepared-statement-safe`.

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
| `SafeSearchDao.java` | `Day27-task02` | prepared statement with a ? placeholder (no string concatenation |
| `SafeSearchDao.java` | `Day27-task02` | LIKE ? ESCAPE with an escaped prefix + "% |
| `SafeSearchDao.java` | `Day27-task02` | insert with a prepared statement and read the generated key |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `exec` |
| 3 | `unsafeSqlShowsTheInjection` |
| 4 | `findsByExactName` |
| 5 | `injectionPayloadIsJustAName` |
| 6 | `prefixSearchTreatsPercentLiterally` |
| 7 | `insertReturnsGeneratedIdAndPersists` |
| 8 | `insertCanStoreQuotesSafely` |

## Edge cases to handle

- Quotes in names (`O'Brien`) must work without escaping by hand.
- Injection payloads match nothing.
- Prefix `%` must not match every row.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 27: PreparedStatement and SQL Injection`

## Hints (optional)

<details><summary>Hint 1</summary>
Escape the user prefix first, then append the real wildcard `%`.
</details>

<details><summary>Hint 2</summary>
`connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)`.
</details>
