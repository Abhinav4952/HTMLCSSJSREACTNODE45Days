# Day 29 — Spring Boot Starters, YAML, Profiles, and ConfigurationProperties

## Learning objectives

- Explain starters, the BOM and auto-configuration back-off
- Configure apps with YAML and profiles
- Bind structured settings with @ConfigurationProperties
- Expose and extend Actuator health/info safely
- Choose the right starter for a use case

## Prerequisites

- Day 28 Spring Core (beans, scanning, @Value)

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-29-THEORY-AND-REFERENCE.md`](DAY-29-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-property-binding` | Spring Boot | `mvn test` |
| 2 | `task-02-profile-greeting` | Spring Boot | `mvn test` |
| 3 | `task-03-actuator-info-note` | Spring Boot | `mvn test` |
| 4 | `task-04-starter-dependency-quiz` | Spring Boot | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Spring Boot
