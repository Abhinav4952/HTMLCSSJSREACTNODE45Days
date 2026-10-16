# Task 1 — Ownership Guard: 403 vs 404 Policy

**Day:** 48 · **Task ID:** Day48-task01 · **Type:** Java · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Encode the object-level authorization decision table (owner, admin, stranger, missing) and the two classic disclosure policies.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day48/task01/Resource.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day48/task01/NotFoundException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day48/task01/ForbiddenException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day48/task01/OwnershipGuard.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day48/task01/OwnershipGuardTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 48 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Missing resource -> `NotFoundException` regardless of caller.
2. Owner or admin -> return the resource.
3. Stranger -> 404 (hide) or 403 (forbid) depending on the policy.
4. Exception messages must not reveal the owner id.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day48-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day48-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 48: complete task-01-ownership-guard`.

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
| `OwnershipGuard.java` | `Day48-task01` | implement the decision table above |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `ownerGetsTheResource` |
| 2 | `adminGetsTheResource` |
| 3 | `missingResourceIsAlways404` |
| 4 | `strangerIsHiddenUnderHidePolicy` |
| 5 | `strangerIsForbiddenUnderForbidPolicy` |
| 6 | `messagesDoNotLeakTheOwner` |

## Edge cases to handle

- Admin on a missing resource still gets 404.
- Messages leaking internals.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 48: Ownership Guard: 403 vs 404 Policy`

## Hints (optional)

<details><summary>Hint 1</summary>
Use a `switch` on the enum for the denial.
</details>
