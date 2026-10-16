# Task 1 — Versioned JSON Event Contract

**Day:** 46 · **Task ID:** Day46-task01 · **Type:** Spring Boot (Jackson) · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Define a tolerant JSON event codec: ignore unknown fields, default the version, validate required fields and reject unsupported versions.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day46/task01/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day46/task01/OrderPlacedEvent.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day46/task01/EventFormatException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day46/task01/EventCodec.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day46/task01/EventCodecTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 46 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Configure the mapper with `FAIL_ON_UNKNOWN_PROPERTIES = false`.
2. Implement `toJson` / `fromJson` wrapping Jackson exceptions in `EventFormatException`.
3. Normalize version 0 (absent) to 1.
4. Reject blank/missing ids and versions above `MAX_SUPPORTED_VERSION`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day46-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day46-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 46: complete task-01-json-event-contract`.

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
| `EventCodec.java` | `Day46-task01` | create the ObjectMapper and configure it to IGNORE unknown properties (forward compatibility |
| `EventCodec.java` | `Day46-task01` | mapper.writeValueAsString, wrap checked exceptions in EventFormatException |
| `EventCodec.java` | `Day46-task01` | parse, then validate and normalise as described |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `roundTrip` |
| 2 | `unknownFieldsAreIgnored` |
| 3 | `missingVersionDefaultsToOne` |
| 4 | `invalidJsonIsRejected` |
| 5 | `blankIdsAreRejected` |
| 6 | `futureVersionsAreRejected` |

## Edge cases to handle

- Missing primitive fields deserialize as 0 in records.
- Null `customerId`.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 46: Versioned JSON Event Contract`

## Hints (optional)

<details><summary>Hint 1</summary>
Records are supported by Jackson 2.12+.
</details>

<details><summary>Hint 2</summary>
Because the record is immutable, build a new one to change the version.
</details>
