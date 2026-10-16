# Task 4 — Notes API: Filters, Headers and Status Codes

**Day:** 30 · **Task ID:** Day30-task04 · **Type:** Spring Boot · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Combine optional query parameters, a custom response header and explicit 400/404 handling in one controller.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day30/task04/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day30/task04/Note.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day30/task04/NoteService.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day30/task04/NoteController.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day30/task04/NoteControllerTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 30 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `search` with `contains`, `limit` and the `X-Total-Count` header.
2. Implement `update` with 200/404/400 behavior; validation happens before lookup.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day30-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day30-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 30: complete task-04-notes-search-and-update`.

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
| `NoteController.java` | `Day30-task04` | filter, count, limit; return 200 with the X-Total-Count header |
| `NoteController.java` | `Day30-task04` | validate text (400 + error body), then update and answer 200 or 404 |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `seed` |
| 2 | `listsAllWithTotalHeader` |
| 3 | `filtersCaseInsensitively` |
| 4 | `limitCutsPageButNotTotal` |
| 5 | `updateReturnsNewNote` |
| 6 | `updateUnknownIs404` |
| 7 | `blankTextIs400EvenForUnknownId` |

## Edge cases to handle

- `limit=0` returns an empty array; total still counts matches.
- Missing `text` key behaves like blank.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 30: Notes API: Filters, Headers and Status Codes`

## Hints (optional)

<details><summary>Hint 1</summary>
Stream filter first, count, then `limit`.
</details>

<details><summary>Hint 2</summary>
Use `ResponseEntity.ok().header(name, value).body(x)`.
</details>
