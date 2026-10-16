# Task 4 — Micrometer Counters, Timers, Gauges and Summaries

**Day:** 41 · **Task ID:** Day41-task04 · **Type:** Spring Boot (Observability) · **Difficulty:** Challenge

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Instrument business code with Micrometer meters (tagged counter, timer, live gauge, distribution summary) and read them back from a SimpleMeterRegistry.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day41/task04/OrderMetrics.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day41/task04/MicrometerMetricsTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 41 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Implement the four `OrderMetrics` methods with the exact meter names, tags and units.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day41-task04)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day41-task04)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 41: complete task-04-micrometer-order-metrics`.

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
| `OrderMetrics.java` | `Day41-task04` | registry.counter(name, tags...).increment( |
| `OrderMetrics.java` | `Day41-task04` | Timer.builder(...).register(registry) then timer.record(supplier |
| `OrderMetrics.java` | `Day41-task04` | Gauge.builder(name, queue, AtomicInteger::get).register(registry |
| `OrderMetrics.java` | `Day41-task04` | DistributionSummary.builder(...).baseUnit(...).register(registry).record(amount |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `counterIsTaggedPerChannel` |
| 3 | `timerRecordsDurationAndReturnsResult` |
| 4 | `timerAlsoCountsFailures` |
| 5 | `gaugeFollowsTheLiveValue` |
| 6 | `distributionSummaryTracksAmounts` |

## Edge cases to handle

- Gauges hold a weak reference to the observed object: keep it referenced elsewhere.
- Tag values must have bounded cardinality (never user ids).
- Timers must record even when the work throws.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 41: Micrometer Counters, Timers, Gauges and Summaries`

## Hints (optional)

<details><summary>Hint 1</summary>
`registry.counter(name, "key", "value")` creates/gets a tagged counter.
</details>

<details><summary>Hint 2</summary>
`Timer#record(Supplier)` returns the supplier's value.
</details>
