# Task 3 — Jackson JSON Contract

**Day:** 30 · **Task ID:** Day30-task03 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Shape a record's JSON representation with Jackson annotations: rename, format, ignore and omit nulls — verified against Spring Boot's auto-configured ObjectMapper.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day30/task03/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day30/task03/Event.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day30/task03/EventJsonTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 30 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Add `@JsonInclude(NON_NULL)` to the record.
2. Rename `name` to `event_name`.
3. Format `date` as `yyyy-MM-dd` text.
4. Hide `internalNote` in both directions.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day30-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day30-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 30: complete task-03-jackson-event-contract`.

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
| `Event.java` | `Day30-task03` | add @JsonInclude(JsonInclude.Include.NON_NULL) on the record |
| `Event.java` | `Day30-task03` | rename to event_name with @JsonProperty |
| `Event.java` | `Day30-task03` | format as yyyy-MM-dd text with @JsonFormat(shape = STRING, pattern = "yyyy-MM-dd |
| `Event.java` | `Day30-task03` | exclude from JSON with @JsonIgnore |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `serializesWithRenamedFormattedFields` |
| 2 | `internalNoteIsNeverSerialized` |
| 3 | `nullsAreOmitted` |
| 4 | `deserializesAndIgnoresInternalNote` |

## Edge cases to handle

- Null `amount`/`venue` must not appear in output.
- Incoming `internalNote` must be ignored (stay null).

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 30: Jackson JSON Contract`

## Hints (optional)

<details><summary>Hint 1</summary>
On records, annotate the component; Jackson 2.15+ propagates it correctly.
</details>

<details><summary>Hint 2</summary>
Boot already registers `JavaTimeModule` and disables timestamp dates.
</details>
