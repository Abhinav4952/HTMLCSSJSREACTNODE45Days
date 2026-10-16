# Task 1 — Sign and Verify JWTs with jjwt

**Day:** 38 · **Task ID:** Day38-task01 · **Type:** Java + jjwt · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Build a small, testable JWT utility: HS256 signing key checks, claims, expiry driven by an injectable Clock, and safe validation.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day38/task01/JwtUtil.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day38/task01/JwtUtilTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 38 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement the constructor, `generate`, `isValid`, `username`, `roles`.
2. Reject secrets shorter than 32 bytes.
3. Validation must never throw.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day38-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day38-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 38: complete task-01-jwt-util-sign-verify`.

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
| `JwtUtil.java` | `Day38-task01` | validate the secret length and build the HMAC key with Keys.hmacShaKeyFor |
| `JwtUtil.java` | `Day38-task01` | build and sign the token |
| `JwtUtil.java` | `Day38-task01` | parse and catch JwtException / IllegalArgumentException |
| `JwtUtil.java` | `Day38-task01` | return the subject |
| `JwtUtil.java` | `Day38-task01` | read the "roles" claim defensively |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `roundTrip` |
| 2 | `expiresAfterTtl` |
| 3 | `tamperedPayloadIsRejected` |
| 4 | `differentSecretIsRejected` |
| 5 | `garbageIsInvalidNotAnException` |
| 6 | `shortSecretIsRejected` |

## Edge cases to handle

- Tampered payloads must fail signature verification.
- A token is valid just before expiry and invalid just after.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 38: Sign and Verify JWTs with jjwt`

## Hints (optional)

<details><summary>Hint 1</summary>
jjwt 0.12: `Jwts.builder().subject(..).claim(..).signWith(key).compact()` and `Jwts.parser().verifyWith(key).build().parseSignedClaims(t)`.
</details>

<details><summary>Hint 2</summary>
A JWT is signed, not encrypted: never put secrets in claims.
</details>
