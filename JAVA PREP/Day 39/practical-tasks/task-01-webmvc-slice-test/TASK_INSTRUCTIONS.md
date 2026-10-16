# Task 1 — @WebMvcTest Slice with a Mocked Service

**Day:** 39 · **Task ID:** Day39-task01 · **Type:** Spring Boot (Testing) · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Implement a controller and prove it with a web-layer slice test: MockMvc, @MockitoBean, BDD stubbing and interaction verification.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day39/task01/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day39/task01/Book.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day39/task01/BookService.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day39/task01/BookController.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day39/task01/BookControllerSliceTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 39 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement `get` and `list` in `BookController`.
2. Add one more test of your own (e.g. a 404 body check).
3. Explain what a slice does and does not load.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day39-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day39-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 39: complete task-01-webmvc-slice-test`.

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
| `BookController.java` | `Day39-task01` | return the book as 200 or answer 404 |
| `BookController.java` | `Day39-task01` | delegate to findAll or byAuthor depending on the parameter |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `returnsBookJson` |
| 2 | `unknownBookIs404` |
| 3 | `listsAll` |
| 4 | `filtersByAuthor` |
| 5 | `badIdTypeIs400` |

## Edge cases to handle

- `list` with an author must never call `findAll()`.
- Type mismatch on `{id}` yields 400 without any code from you.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 39: @WebMvcTest Slice with a Mocked Service`

## Hints (optional)

<details><summary>Hint 1</summary>
`@MockitoBean` (Spring Framework 6.2, Boot 3.4) replaces the older `@MockBean`.
</details>

<details><summary>Hint 2</summary>
A web slice contains controllers, advice, converters and filters — not `@Service` beans.
</details>
