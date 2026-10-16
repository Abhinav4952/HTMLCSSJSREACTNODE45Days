# Task 2 — @Primary and @Qualifier

**Day:** 28 · **Task ID:** Day28-task02 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Resolve ambiguity between two beans of the same type with @Primary and override the default with @Qualifier at a single injection point.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day28/task02/PaymentGateway.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day28/task02/SimpleGateway.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day28/task02/GatewayConfig.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day28/task02/DefaultCheckout.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day28/task02/PaypalCheckout.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day28/task02/CheckoutTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 28 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Mark the `stripe` bean as `@Primary`.
2. Make `PaypalCheckout` inject the `paypal` bean with `@Qualifier`.
3. Implement both `pay` methods.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day28-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day28-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 28: complete task-02-qualifier-primary`.

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
| `GatewayConfig.java` | `Day28-task02` | mark this bean as the default choice when a PaymentGateway is injected without a qualifier |
| `DefaultCheckout.java` | `Day28-task02` | delegate to the injected gateway |
| `PaypalCheckout.java` | `Day28-task02` | select the bean named "paypal" for this parameter (@Qualifier |
| `PaypalCheckout.java` | `Day28-task02` | delegate to the injected gateway |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `unqualifiedInjectionPicksThePrimaryGateway` |
| 2 | `qualifierOverridesPrimary` |
| 3 | `rejectsNonPositiveAmounts` |

## Edge cases to handle

- Without `@Primary` the context fails with `NoUniqueBeanDefinitionException` — that is the lesson.
- Non-positive amounts are rejected.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 28: @Primary and @Qualifier`

## Hints (optional)

<details><summary>Hint 1</summary>
`@Qualifier("paypal")` matches the bean name given in `@Bean("paypal")`.
</details>

<details><summary>Hint 2</summary>
`@Primary` is a default; `@Qualifier` is an explicit choice.
</details>
