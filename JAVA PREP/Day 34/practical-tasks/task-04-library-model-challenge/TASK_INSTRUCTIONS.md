# Task 4 — Library Model: 1:1, 1:N and N:M Together

**Day:** 34 · **Task ID:** Day34-task04 · **Type:** Spring Boot · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Combine all three relationship types in one aggregate and decide cascade, orphanRemoval and fetch settings for each edge.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day34/task04/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day34/task04/Author.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day34/task04/Book.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day34/task04/BookDetail.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day34/task04/Tag.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day34/task04/LibraryModelTest.java` | Provided helper or test (do not edit) |
| `src/test/resources/application.properties` | Provided helper or test (do not edit) |

## Prerequisites

- Day 34 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Map `Author.books`, `Book.author`, `Book.detail`, `Book.tags` and `Tag.books`.
2. Implement `addBook`, `removeBook`, `tag`.
3. Decide where cascade is safe (author->book->detail) and where it is not (tags).

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day34-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day34-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 34: complete task-04-library-model-challenge`.

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
| `Author.java` | `Day34-task04` | inverse one-to-many to Book (mappedBy author, cascade ALL, orphanRemoval, LAZY |
| `Author.java` | `Day34-task04` | add and set back reference |
| `Author.java` | `Day34-task04` | remove and clear back reference |
| `Book.java` | `Day34-task04` | many-to-one to Author: LAZY, join column author_id, not nullable |
| `Book.java` | `Day34-task04` | one-to-one to BookDetail owned by Book: LAZY, cascade ALL, orphanRemoval, join column detail_id |
| `Book.java` | `Day34-task04` | many-to-many to Tag through join table book_tags(book_id, tag_id); no cascade |
| `Book.java` | `Day34-task04` | add to both sides |
| `Tag.java` | `Day34-task04` | inverse many-to-many (mappedBy tags |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `cascadesFromAuthorThroughBooksToDetails` |
| 2 | `associationsAreLazy` |
| 3 | `removingBookRemovesItsDetailButNotTags` |
| 4 | `removingAuthorRemovesBooksAndDetailsButKeepsTags` |
| 5 | `tagKnowsItsBooks` |

## Edge cases to handle

- Removing an author must not remove shared tags.
- All associations must be LAZY at runtime.
- `orphanRemoval` on Book.detail removes details together with removed books.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 34: Library Model: 1:1, 1:N and N:M Together`

## Hints (optional)

<details><summary>Hint 1</summary>
Think in aggregates: Author owns Books, Books own details; Tags are shared references.
</details>

<details><summary>Hint 2</summary>
Reuse patterns from tasks 1-3.
</details>
