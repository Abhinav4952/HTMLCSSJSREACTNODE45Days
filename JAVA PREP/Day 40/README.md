# Day 40 — Spring AOP: Aspects, Pointcuts and Advice

## Learning objectives

- Explain aspects, join points, pointcuts, advice and proxies
- Write @Before/@AfterReturning/@AfterThrowing/@After/@Around advice
- Compose pointcut expressions and test them
- Control aspect precedence with @Order
- Recognize AOP pitfalls (self-invocation, final/private methods)

## Prerequisites

- Day 28-29 Spring Core and Boot
- Day 35 @Transactional (an AOP application)

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-40-THEORY-AND-REFERENCE.md`](DAY-40-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-advice-types-order-service` | Spring AOP | `mvn test` |
| 2 | `task-02-around-timing-and-args` | Spring AOP | `mvn test` |
| 3 | `task-03-pointcut-expressions-lab` | Spring AOP | `mvn test` |
| 4 | `task-04-aspect-ordering-challenge` | Spring AOP | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Spring Boot
