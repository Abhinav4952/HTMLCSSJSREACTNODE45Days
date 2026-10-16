# Task 2 — HS256 JWT Token Service

**Day:** 47 · **Task ID:** Day47-task02 · **Type:** Spring Boot (security concepts) · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Implement signing and verification of a JWT by hand (HMAC-SHA256, base64url) to understand exactly what a library does and which attacks (tampering, alg=none, expiry) you must reject.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day47/task02/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day47/task02/TokenClaims.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day47/task02/InvalidTokenException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day47/task02/TokenService.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day47/task02/TokenServiceTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 47 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Constructor rejects secrets shorter than 32 chars.
2. `issue` builds header and payload JSON and signs `header.payload` with HmacSHA256.
3. `verify` validates structure, algorithm, signature (constant time) and expiry.
4. All failures raise `InvalidTokenException`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day47-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day47-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 47: complete task-02-jwt-token-service`.

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
| `TokenService.java` | `Day47-task02` | validate the secret length and keep the fields |
| `TokenService.java` | `Day47-task02` | build header + payload JSON (Jackson ObjectMapper), base64url without padding, sign with HmacSHA256 |
| `TokenService.java` | `Day47-task02` | split, check header, recompute and compare the signature, then parse payload and check expiry |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `issuedTokenVerifiesAndCarriesClaims` |
| 2 | `tokenHasThreeBase64UrlPartsAndHs256Header` |
| 3 | `expiredTokenIsRejected` |
| 4 | `tamperedPayloadIsRejected` |
| 5 | `wrongSecretIsRejected` |
| 6 | `algNoneTokenIsRejected` |
| 7 | `garbageIsRejected` |
| 8 | `invalidArgumentsAreRejected` |

## Edge cases to handle

- `alg: none`.
- Tampered payload with a valid-looking signature part.
- Expiry boundary (`exp <= now` is expired).
- Padding characters in base64url.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 47: HS256 JWT Token Service`

## Hints (optional)

<details><summary>Hint 1</summary>
`Mac.getInstance("HmacSHA256")` + `SecretKeySpec`.
</details>

<details><summary>Hint 2</summary>
`MessageDigest.isEqual(a, b)` for constant-time comparison.
</details>

<details><summary>Hint 3</summary>
`Base64.getUrlEncoder().withoutPadding()`.
</details>
