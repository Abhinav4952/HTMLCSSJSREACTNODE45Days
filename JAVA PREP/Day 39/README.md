# Day 39 — Spring Testing: Slices, Mockito, and Security Tests

## Learning objectives

- Choose between unit, slice and integration tests
- Test controllers with @WebMvcTest and MockMvc
- Test repositories with @DataJpaTest
- Use @MockitoBean, captors and verification
- Test authorization with spring-security-test

## Prerequisites

- Day 30–38 REST, JPA, Security

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-39-THEORY-AND-REFERENCE.md`](DAY-39-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-webmvc-slice-test` | Spring Boot (Testing) | `mvn test` |
| 2 | `task-02-datajpa-slice` | Spring Boot (Testing) | `mvn test` |
| 3 | `task-03-mockbean-service` | Spring Boot (Testing) | `mvn test` |
| 4 | `task-04-security-test-util` | Spring Boot (Testing) | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Spring Boot
