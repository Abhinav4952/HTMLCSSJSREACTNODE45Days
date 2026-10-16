# Day 37 — Spring Security I: Filter Chain, UserDetailsService, BCrypt and Roles

## Learning objectives

- Explain the servlet filter chain and configure a SecurityFilterChain
- Implement UserDetailsService and understand DaoAuthenticationProvider
- Hash and verify passwords with BCrypt
- Apply role-based URL rules and test them with MockMvc

## Prerequisites

- Day 31 REST II
- Day 36 CORS

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-37-THEORY-AND-REFERENCE.md`](DAY-37-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-security-filter-chain` | Spring Boot | `mvn test` |
| 2 | `task-02-user-details-service` | Spring Boot | `mvn test` |
| 3 | `task-03-bcrypt-password-service` | Spring Boot | `mvn test` |
| 4 | `task-04-role-rules-challenge` | Spring Boot | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Spring Boot
