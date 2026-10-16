# Task 3 — Spring Cache: @Cacheable, @CachePut and @CacheEvict

**Day:** 42 · **Task ID:** Day42-task03 · **Type:** Spring Boot (Async / Scheduling / Cache) · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Add caching declaratively: hit/miss behavior, SpEL keys, unless conditions, put and evict semantics.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day42/task03/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day42/task03/CacheConfig.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day42/task03/PriceService.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day42/task03/CachingTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 42 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Enable caching and annotate the five service methods exactly as documented.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day42-task03)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day42-task03)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 42: complete task-03-cache-abstraction`.

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
| `CacheConfig.java` | `Day42-task03` | switch on annotation-driven caching (@EnableCaching |
| `PriceService.java` | `Day42-task03` | @Cacheable in cache "prices", skip caching null results (unless = "#result == null |
| `PriceService.java` | `Day42-task03` | @CachePut in cache "prices" with key "#sku |
| `PriceService.java` | `Day42-task03` | @CacheEvict in cache "prices" with key "#sku |
| `PriceService.java` | `Day42-task03` | @CacheEvict in cache "prices" with allEntries = true |
| `PriceService.java` | `Day42-task03` | @Cacheable in cache "rates" with key "#from + '->' + #to |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `clean` |
| 2 | `cacheInfrastructureIsActive` |
| 3 | `secondCallHitsTheCache` |
| 4 | `differentKeysAreCachedSeparately` |
| 5 | `nullResultsAreNotCached` |
| 6 | `cachePutRefreshesTheEntryWithoutAnotherLoad` |
| 7 | `evictForcesReload` |
| 8 | `evictAllClearsEverything` |
| 9 | `compositeSpelKey` |

## Edge cases to handle

- Cache keys must be stable and cheap: avoid mutable objects.
- `@CachePut` always executes the method; `@Cacheable` skips it on a hit.
- Self-invocation bypasses the cache proxy like every other AOP feature.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 42: Spring Cache: @Cacheable, @CachePut and @CacheEvict`

## Hints (optional)

<details><summary>Hint 1</summary>
`unless` is evaluated after the call and can use `#result`.
</details>

<details><summary>Hint 2</summary>
Default cache manager (no provider on classpath) is a ConcurrentMap - fine for tests, use Caffeine/Redis in production.
</details>
