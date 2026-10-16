# Task 1 — Constructor Injection

**Day:** 28 · **Task ID:** Day28-task01 · **Type:** Spring Boot · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Register a service as a bean, inject its collaborator through the constructor, and prove it works both as a plain object and inside a container.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day28/task01/MessageRepository.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day28/task01/InMemoryMessageRepository.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day28/task01/GreetingService.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day28/task01/GreetingServiceImpl.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day28/task01/AppConfig.java` | Provided helper or test (do not edit) |
| `src/test/java/com/javaprep/day28/task01/GreetingServiceTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 28 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Annotate `GreetingServiceImpl` with a stereotype annotation so component scanning registers it.
2. Implement `greet` using the injected repository.
3. Keep the dependency `final` and constructor-injected (no field injection).

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day28-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day28-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 28: complete task-01-constructor-injection`.

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
| `GreetingServiceImpl.java` | `Day28-task01` | register this class as a Spring bean with a stereotype annotation (@Service |
| `GreetingServiceImpl.java` | `Day28-task01` | use the injected repository and validate the name |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `greetsUsingTheInjectedRepository` |
| 2 | `rejectsBlankNames` |
| 3 | `containerWiresTheServiceWithConstructorInjection` |

## Edge cases to handle

- Blank or null names -> `IllegalArgumentException`.
- Exactly one `GreetingService` bean must exist.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 28: Constructor Injection`

## Hints (optional)

<details><summary>Hint 1</summary>
`@Service` is a specialization of `@Component`.
</details>

<details><summary>Hint 2</summary>
A class with one constructor needs no `@Autowired`.
</details>
