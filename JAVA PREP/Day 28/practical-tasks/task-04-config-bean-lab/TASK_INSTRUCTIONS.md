# Task 4 — Java Config and @Value

**Day:** 28 · **Task ID:** Day28-task04 · **Type:** Spring Boot · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Build beans with @Configuration/@Bean methods, inject a property with a default via @Value, validate it, and wire one bean into another.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day28/task04/TaxPolicy.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day28/task04/PriceCalculator.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day28/task04/PricingConfig.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day28/task04/PricingConfigTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 28 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Add `@Value("${tax.rate:0.2}")` to the `taxPolicy` parameter and validate the range.
2. Implement both `@Bean` methods.
3. Show the default and an overridden property both work.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day28-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day28-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 28: complete task-04-config-bean-lab`.

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
| `PricingConfig.java` | `Day28-task04` | inject the property: add @Value("${tax.rate:0.2}") to the parameter |
| `PricingConfig.java` | `Day28-task04` | validate the rate and return the policy |
| `PricingConfig.java` | `Day28-task04` | wire the calculator with the policy bean |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `defaultRateIsTwentyPercent` |
| 2 | `rateComesFromTheEnvironment` |
| 3 | `invalidRateFailsContextStartup` |
| 4 | `calculatorUsesTheSameTaxPolicyBean` |

## Edge cases to handle

- Rate must be within 0..1 inclusive; otherwise context startup fails.
- Both beans are singletons: the calculator must receive the container's `TaxPolicy`.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 28: Java Config and @Value`

## Hints (optional)

<details><summary>Hint 1</summary>
Without `@Value` Spring cannot inject a primitive `double` and fails with `NoSuchBeanDefinitionException`.
</details>

<details><summary>Hint 2</summary>
`${key:default}` supplies the default.
</details>
