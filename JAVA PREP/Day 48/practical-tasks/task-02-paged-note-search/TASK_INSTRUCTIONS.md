# Task 2 — Owner-Scoped Paged Search

**Day:** 48 · **Task ID:** Day48-task02 · **Type:** Spring Boot (JPA) · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Build the capstone's list endpoint logic: owner scoping, pagination, whitelisted sorting and a stable page envelope.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day48/task02/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day48/task02/Note.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day48/task02/NoteRepository.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day48/task02/PageResponse.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day48/task02/NoteSearchService.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day48/task02/NoteSearchServiceTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 48 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Validate page, size, sort field (whitelist) and direction.
2. Clamp size to `MAX_SIZE`.
3. Query by owner and case-insensitive title fragment through the repository.
4. Return a `PageResponse` with the effective page size.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day48-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day48-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 48: complete task-02-paged-note-search`.

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
| `NoteSearchService.java` | `Day48-task02` | validate, build PageRequest.of(page, size, Sort.by(dir, sortBy)), query the repository, map the Page |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `seed` |
| 2 | `pagesAndTotalsAreReported` |
| 3 | `sortsByCreatedAtDescending` |
| 4 | `searchIsScopedToTheOwner` |
| 5 | `sizeIsClamped` |
| 6 | `invalidArgumentsAreRejected` |

## Edge cases to handle

- Null query.
- Sorting by a field that must not be exposed (e.g. `ownerId`).
- Huge page size.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 48: Owner-Scoped Paged Search`

## Hints (optional)

<details><summary>Hint 1</summary>
`Sort.Direction.fromString` throws IAE for bad values (wrap or rely on it).
</details>

<details><summary>Hint 2</summary>
`Page#getTotalPages()` and `getTotalElements()`.
</details>
