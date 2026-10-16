# Task 4 — Method References Zoo

**Day:** 16 · **Task ID:** Day16-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Return functions implemented with each kind of method reference (static, bound, unbound, constructor) and build a map index from a key-extractor reference. **Challenge:** the implementation of each method must be a method reference (not a lambda), except where a lambda is unavoidable - justify those in a comment.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day16/task04/Person.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day16/task04/MethodRefMap.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day16/task04/MethodRefMapTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 16 theory file read

## What you will implement

1. `parser()` returns a `Function<String,Integer>` using `Integer::parseInt` (static reference)
2. `upper()` returns a `Function<String,String>` using `String::toUpperCase` (unbound instance reference)
3. `prefixer(prefix)` returns a function that prepends `prefix`, using a bound reference (`prefix::concat`); `null` prefix throws `NullPointerException` immediately (when creating the reference)
4. `listFactory()` returns a `Supplier<List<String>>` producing a **new** empty mutable list each call (`ArrayList::new`)
5. `personFactory()` returns a `Function<String, Person>` using the `Person::new` constructor reference
6. `indexBy(values, keyFn)` returns a `LinkedHashMap` of key -> value in input order and throws `IllegalArgumentException` on duplicate keys

## Constraints

- Return method references (not lambdas) from `parser`, `upper`, `prefixer`, `listFactory`, `personFactory`
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=MethodRefMapTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **8 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day16-task04)`).

### Run one test class

```bash
mvn -Dtest=MethodRefMapTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `MethodRefMap.java` — `parser` | `TODO(Day16-task04)` | return Integer::parseInt (static method reference) |
| `MethodRefMap.java` — `upper` | `TODO(Day16-task04)` | return String::toUpperCase (unbound instance method reference) |
| `MethodRefMap.java` — `prefixer` | `TODO(Day16-task04)` | return prefix::concat (bound reference); a null prefix must fail immediately with NullPointerException |
| `MethodRefMap.java` — `listFactory` | `TODO(Day16-task04)` | return ArrayList::new (constructor reference) |
| `MethodRefMap.java` — `personFactory` | `TODO(Day16-task04)` | return Person::new (constructor reference) |
| `MethodRefMap.java` — `indexBy` | `TODO(Day16-task04)` | build a LinkedHashMap key -> value in input order; IllegalArgumentException on a duplicate key (use putIfAbsent) |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_parser` |
| 2 | `r2_upper` |
| 3 | `r3_prefixerIsBound`, `r3_nullPrefixFailsImmediately` |
| 4 | `r4_listFactoryReturnsFreshMutableLists` |
| 5 | `r5_personFactory` |
| 6 | `r6_indexByKeepsOrder`, `r6_indexByRejectsDuplicates` |

## Edge cases to handle

- null prefix
- each listFactory call yields a distinct list
- duplicate keys
- empty input

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 16: Method References Zoo`

## Hints (optional)

<details><summary>Hint 1</summary>

`prefix::concat` evaluates `prefix` immediately; a null receiver fails when the reference is created, which is exactly what the test expects.

</details>

<details><summary>Hint 2</summary>

`map.putIfAbsent` returns the previous value (or null) - handy for duplicate detection.

</details>
