# Task 1 — LocalDate Spans and Business Days

**Day:** 19 · **Task ID:** Day19-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Do calendar math with `LocalDate`: compute ages, add business days, enumerate date ranges, format a human-readable span, and check overdue status with an injected `Clock`.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day19/task01/LocalDateSpan.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day19/task01/LocalDateSpanTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 19 theory file read

## What you will implement

1. `ageOn(birth, on)` returns the completed years on that day; `birth` after `on` throws `IllegalArgumentException` (leap-day births handled by `Period`)
2. `addBusinessDays(start, n)` skips Saturdays and Sundays; `n == 0` returns `start` unchanged; `n < 0` throws `IllegalArgumentException`
3. `datesBetween(startInclusive, endExclusive)` lists every date; equal dates give an empty list; `end` before `start` throws `IllegalArgumentException`
4. `humanSpan(from, to)` returns `"<y>y <m>m <d>d"` using `Period.between`; `to` before `from` throws `IllegalArgumentException`
5. `nextWeekday(from, dayOfWeek)` returns the next occurrence **strictly after** `from`
6. `isOverdue(due, clock)` is true when today (per the clock) is after `due`

## Constraints

- Use `java.time` only - no `java.util.Date`, `Calendar`, or `SimpleDateFormat`
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=LocalDateSpanTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **8 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day19-task01)`).

### Run one test class

```bash
mvn -Dtest=LocalDateSpanTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `LocalDateSpan.java` — `ageOn` | `TODO(Day19-task01)` | completed years between birth and on (Period.between(...).getYears()); IllegalArgumentException if birth is after on |
| `LocalDateSpan.java` — `addBusinessDays` | `TODO(Day19-task01)` | move forward n weekdays skipping Saturday/Sunday; n == 0 returns start; negative n -> IllegalArgumentException |
| `LocalDateSpan.java` — `datesBetween` | `TODO(Day19-task01)` | every date from startInclusive up to (not including) endExclusive; equal -> empty; end before start -> IllegalArgumentException |
| `LocalDateSpan.java` — `humanSpan` | `TODO(Day19-task01)` | format Period.between(from, to) as "<years>y <months>m <days>d"; IllegalArgumentException if to is before from |
| `LocalDateSpan.java` — `nextWeekday` | `TODO(Day19-task01)` | the next date strictly after from that falls on dayOfWeek (TemporalAdjusters.next) |
| `LocalDateSpan.java` — `isOverdue` | `TODO(Day19-task01)` | true when LocalDate.now(clock) is after due (never call LocalDate.now() without the clock) |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_ageOnBirthday`, `r1_ageForLeapDayBirthAndInvalidOrder` |
| 2 | `r2_addBusinessDaysSkipsWeekends`, `r2_negativeBusinessDaysRejected` |
| 3 | `r3_datesBetween` |
| 4 | `r4_humanSpan` |
| 5 | `r5_nextWeekdayIsStrictlyAfter` |
| 6 | `r6_isOverdueUsesTheInjectedClock` |

## Edge cases to handle

- leap-day birthdays
- weekend start for business days
- month/year boundaries in ranges
- same-day comparisons for overdue

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 19: LocalDate Spans and Business Days`

## Hints (optional)

<details><summary>Hint 1</summary>

`Period.between(birth, on).getYears()` already handles Feb 29 and month ends.

</details>

<details><summary>Hint 2</summary>

Loop one day at a time and decrement the counter only on weekdays - simplest correct approach for `addBusinessDays`.

</details>
