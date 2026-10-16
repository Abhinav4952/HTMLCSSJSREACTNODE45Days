# Task 4 — Ownership-Enforcing Note Service (Challenge)

**Day:** 48 · **Task ID:** Day48-task04 · **Type:** Spring Boot (JPA) · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Integrate ownership checks with JPA: read, rename and delete notes with a hide-existence policy, admin override and validation order.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day48/task04/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day48/task04/Note.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day48/task04/NoteRepository.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day48/task04/NotFoundException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day48/task04/NoteService.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day48/task04/NoteServiceTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 48 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. `get`, `rename`, `delete` enforce: owner or admin only; strangers and missing ids both yield `NotFoundException`.
2. `rename` validates the title first (IAE), then authorizes, then persists.
3. Failed authorization must leave data untouched.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day48-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day48-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 48: complete task-04-note-service-ownership-challenge`.

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
| `NoteService.java` | `Day48-task04` | load the note and apply the ownership rule |
| `NoteService.java` | `Day48-task04` | validate, authorize, change the title, save |
| `NoteService.java` | `Day48-task04` | authorize and delete |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `seed` |
| 2 | `ownerCanReadRenameAndDelete` |
| 3 | `strangerSeesNotFoundForEverything` |
| 4 | `adminCanAccessAnyNote` |
| 5 | `unknownIdIsNotFound` |
| 6 | `blankTitleIsRejectedBeforeAnyLookup` |

## Edge cases to handle

- Unknown id.
- Admin on someone else's note.
- Validation vs authorization order.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 48: Ownership-Enforcing Note Service (Challenge)`

## Hints (optional)

<details><summary>Hint 1</summary>
Write one private `loadAuthorized(callerId, admin, id)` helper and reuse it.
</details>

<details><summary>Hint 2</summary>
Inside `@Transactional`, changing a managed entity is persisted at commit; `save` makes intent explicit.
</details>
