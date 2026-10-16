# Day 23 — Testing in Depth: JUnit 5, Parameterized Tests, Mockito, TDD, the Test Pyramid, and JaCoCo

## Learning objectives

- Use the JUnit 5 (Jupiter) lifecycle, `@Nested`, `@DisplayName`, `assertAll`, `assertThrows`, and `@TempDir` effectively
- Write data-driven tests with `@ParameterizedTest` (`@ValueSource`, `@CsvSource`, `@MethodSource`, `@NullSource`)
- Create mocks and stubs with Mockito (`@Mock`, `when/thenReturn/thenThrow`, `verify`, `ArgumentCaptor`, `InOrder`, `never`) and know when *not* to mock
- Practise the TDD red-green-refactor loop and explain its benefits and limits
- Explain the test pyramid (unit, integration, end-to-end) and the cost/feedback trade-offs of each layer
- Generate and interpret a JaCoCo report (line vs branch coverage) without worshipping the percentage

## Prerequisites

- Day 13 — exceptions
- Day 16 — lambdas and functional interfaces
- Day 21 — concurrency basics (for flaky-test reasoning)
- Day 24 preview — Maven phases (`test`, `verify`)

## How to use this folder

1. Read [`DAY-23-THEORY-AND-REFERENCE.md`](DAY-23-THEORY-AND-REFERENCE.md) first.
2. Open each task folder under `practical-tasks/` as its own Maven project in IntelliJ.
3. Run `mvn test` (**red**), implement the `TODO(Day23-taskYY)` stubs, run `mvn test` again until **green**.
4. Do not edit tests, `TASK_INSTRUCTIONS.md`, or `EVALUATION_CRITERIA.md`.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-parameterized-conversions` | Plain Java | `mvn test` |
| 2 | `task-02-mockito-order-service` | Plain Java | `mvn test` |
| 3 | `task-03-tdd-rpn-calculator` | Plain Java | `mvn test` |
| 4 | `task-04-jacoco-loyalty-service` | Plain Java | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Core Java
