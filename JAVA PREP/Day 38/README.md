# Day 38 — Spring Security II: JWT, 401 vs 403, Method Security

## Learning objectives

- Create and verify HS256 JWTs with jjwt 0.12
- Build a Bearer-token authentication filter
- Return correct 401/403 JSON responses
- Apply @PreAuthorize with SpEL
- Understand JWT trade-offs (revocation, claims, secrets)

## Prerequisites

- Day 37 Spring Security I

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-38-THEORY-AND-REFERENCE.md`](DAY-38-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-jwt-util-sign-verify` | Java + jjwt | `mvn test` |
| 2 | `task-02-jwt-filter` | Spring Boot (Security + JWT) | `mvn test` |
| 3 | `task-03-status-401-vs-403` | Spring Boot (Security + JWT) | `mvn test` |
| 4 | `task-04-preauthorize-method` | Spring Boot (Security + JWT) | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Spring Boot
