# Day 28 — Spring Core: IoC and Dependency Injection

## Learning objectives

- Explain IoC/DI and why constructor injection is preferred
- Register beans via stereotypes, component scanning and @Bean methods
- Resolve ambiguity with @Primary and @Qualifier
- Use @PostConstruct/@PreDestroy and understand singleton vs prototype scope
- Inject externalized properties with @Value and defaults

## Prerequisites

- Day 21–27 Java fundamentals and JDBC
- Interfaces and polymorphism

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-28-THEORY-AND-REFERENCE.md`](DAY-28-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-constructor-injection` | Spring Boot | `mvn test` |
| 2 | `task-02-qualifier-primary` | Spring Boot | `mvn test` |
| 3 | `task-03-bean-lifecycle` | Spring Boot | `mvn test` |
| 4 | `task-04-config-bean-lab` | Spring Boot | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Spring Boot
