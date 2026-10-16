# Task 1 — Timed Round 1 (45 min): Collections and Streams

**Day:** 50 · **Task ID:** Day50-task01 · **Type:** Core Java · **Difficulty:** Timed

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Four classic interview utilities (word frequency, anagram groups, first non-repeated character, balanced brackets). Start a 45-minute timer, then stop and note how far you got.

## Learning goals

- Practice solving a mixed collections problem set under time pressure
- Choose the right collection and complexity
- Explain trade-offs aloud as you would in an interview

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day50/task01/TextStats.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day50/task01/TextStatsTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 50 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. `topWords`: frequency count, deterministic ordering.
2. `groupAnagrams`: stable grouping.
3. `firstNonRepeated`: single pass counting with insertion order.
4. `isBalanced`: stack-based matching.

## Constraints

- Java 21; no Spring; no Lombok.
- Do not edit test files or this document; edit only the places marked `TODO(Day50-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day50-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 50: complete task-01-timed-collections-streams-45min`.

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
| `TextStats.java` | `Day50-task01` | count with a Map, sort with a Comparator (count desc, word asc), limit n |
| `TextStats.java` | `Day50-task01` | key = sorted characters; use a LinkedHashMap |
| `TextStats.java` | `Day50-task01` | LinkedHashMap<Character,Integer> counting, then first entry with count 1 |
| `TextStats.java` | `Day50-task01` | stack (Deque) of expected closers |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `topWordsCountsCaseInsensitivelyAndBreaksTiesAlphabetically` |
| 2 | `topWordsEdgeCases` |
| 3 | `groupsAnagramsInStableOrder` |
| 4 | `firstNonRepeatedCharacter` |
| 5 | `balancedBrackets` |

## Edge cases to handle

- Empty/null input.
- Ties in frequency.
- Case sensitivity differences between methods.
- Unbalanced closers at the start.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 50: Timed Round 1 (45 min): Collections and Streams`

## Hints (optional)

<details><summary>Hint 1</summary>
Think about the data structure first: `HashMap` vs `LinkedHashMap` vs `ArrayDeque`.
</details>

<details><summary>Hint 2</summary>
`Comparator.comparing(...).reversed().thenComparing(...)` or `Map.Entry` comparators.
</details>
