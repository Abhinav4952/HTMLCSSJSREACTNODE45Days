# Day 49 — Production Readiness: Profiles, Secrets, JAR, CI, Checkstyle, Git

## Learning objectives

- Configure profiles and externalize secrets safely
- Build and run an executable Spring Boot JAR
- Write a GitHub Actions workflow for Maven
- Explain and apply Checkstyle rules
- Apply branching, commit and versioning conventions

## Prerequisites

- Days 29-30 profiles and configuration
- Day 47-48 capstone slices

## Spring Boot version note

Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## How to use this folder

1. Read [`DAY-49-THEORY-AND-REFERENCE.md`](DAY-49-THEORY-AND-REFERENCE.md) first.
2. Open each task folder as its own Maven project in IntelliJ.
3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-production-config-check` | Java | `mvn test` |
| 2 | `task-02-github-actions-workflow` | Java + CI | `mvn test` |
| 3 | `task-03-style-linter` | Java | `mvn test` |
| 4 | `task-04-git-conventions-release-checklist` | Java + Git | `mvn test` |

**Estimated time:** 2-3 h theory + 4-6 h tasks  
**Phase:** Capstone
