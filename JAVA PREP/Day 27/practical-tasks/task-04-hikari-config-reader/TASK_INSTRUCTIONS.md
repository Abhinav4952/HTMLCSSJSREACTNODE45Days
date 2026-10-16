# Task 4 — HikariCP Config Reader

**Day:** 27 · **Task ID:** Day27-task04 · **Type:** Plain Java + JDBC (H2) · **Difficulty:** Challenge

## Summary

Parse and validate connection-pool settings from Properties, build a HikariConfig, and produce a log-safe summary that masks the password.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day27/task04/PoolSettingsReader.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day27/task04/PoolSettingsReaderTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 27 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `read` with defaults and validation (messages must mention the offending key).
2. Implement `toHikariConfig`.
3. Implement `maskedSummary` with the exact format.
4. Open a real HikariCP pool in the last test to prove the config works.

## Constraints

- Java 21; plain JDBC/SQL only (no Spring, no Lombok); H2 2.3.232 in PostgreSQL mode is the only database.
- Do not edit test files or this document; edit only the places marked `TODO(Day27-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day27-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 27: complete task-04-hikari-config-reader`.

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
| `PoolSettingsReader.java` | `Day27-task04` | parse + validate as documented |
| `PoolSettingsReader.java` | `Day27-task04` | populate and return a HikariConfig |
| `PoolSettingsReader.java` | `Day27-task04` | build the masked summary string |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `appliesDefaults` |
| 2 | `readsExplicitValues` |
| 3 | `rejectsInvalidSettings` |
| 4 | `summaryNeverLeaksPassword` |
| 5 | `hikariConfigIsUsableToOpenAPool` |

## Edge cases to handle

- Blank or missing `jdbcUrl` is an error.
- `minimumIdle` defaults to `maximumPoolSize`.
- Non-numeric values -> `IllegalArgumentException`.
- The password must never appear in the summary.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 27: HikariCP Config Reader`

## Hints (optional)

<details><summary>Hint 1</summary>
`Integer.parseInt` throws `NumberFormatException` (a subclass of `IllegalArgumentException`) — still add the key name to the message.
</details>

<details><summary>Hint 2</summary>
HikariCP 6.2.1 is an optional dependency used only by this task.
</details>
