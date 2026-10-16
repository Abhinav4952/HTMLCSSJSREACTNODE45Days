# Task 2 — Zoned Meeting Scheduler

**Day:** 19 · **Task ID:** Day19-task02 · **Type:** Plain Java · **Difficulty:** Core

## Summary

Convert and compare moments across time zones: convert a local date-time between zones, render one instant in several zones, check business hours in the meeting's own zone, measure elapsed minutes across a DST jump, schedule weekly recurrences by wall-clock time, and format as UTC.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day19/task02/ZonedMeeting.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day19/task02/ZonedMeetingTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 19 theory file read

## What you will implement

1. `convert(local, from, to)` returns the `ZonedDateTime` in zone `to` for the instant described by `local` in zone `from`
2. `localTimes(instant, zoneIds)` returns `"yyyy-MM-dd HH:mm"` strings in the order of `zoneIds`; an unknown zone id throws `java.time.DateTimeException`
3. `isDuringWorkHours(t)` is true for Monday-Friday from 09:00 (inclusive) to 17:00 (exclusive) in `t`'s own zone
4. `minutesBetween(a, b)` returns the **elapsed** minutes (DST aware): on 2024-03-10 in `America/New_York`, 01:30 -> 03:30 is 60 minutes
5. `plusWeeksWallClock(start, weeks)` keeps the local time across DST changes
6. `formatUtc(t)` returns the ISO-8601 instant string such as `2024-05-20T09:00:00Z`

## Constraints

- Use `java.time` only; do not use `ZoneId.systemDefault()` anywhere
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=ZonedMeetingTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **7 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day19-task02)`).

### Run one test class

```bash
mvn -Dtest=ZonedMeetingTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `ZonedMeeting.java` — `convert` | `TODO(Day19-task02)` | interpret local in zone from, then return the same instant expressed in zone to (withZoneSameInstant) |
| `ZonedMeeting.java` — `localTimes` | `TODO(Day19-task02)` | for each zone id (in order) format instant.atZone(ZoneId.of(id)) as yyyy-MM-dd HH:mm; unknown id propagates DateTimeException |
| `ZonedMeeting.java` — `isDuringWorkHours` | `TODO(Day19-task02)` | Monday-Friday and 09:00 <= local time < 17:00 in t's own zone |
| `ZonedMeeting.java` — `minutesBetween` | `TODO(Day19-task02)` | elapsed minutes from a to b using Duration.between (so DST changes are respected) |
| `ZonedMeeting.java` — `plusWeeksWallClock` | `TODO(Day19-task02)` | add weeks keeping the local wall-clock time (ZonedDateTime.plusWeeks, not Duration) |
| `ZonedMeeting.java` — `formatUtc` | `TODO(Day19-task02)` | the instant of t as an ISO-8601 UTC string (Instant#toString) |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_convertKeepsTheInstant` |
| 2 | `r2_localTimesInRequestedOrder`, `r2_unknownZoneFails` |
| 3 | `r3_workHoursInTheMeetingsOwnZone` |
| 4 | `r4_minutesBetweenIsElapsedTime` |
| 5 | `r5_weeklyRecurrenceKeepsLocalTimeAcrossDst` |
| 6 | `r6_formatUtc` |

## Edge cases to handle

- DST spring-forward day
- boundaries 08:59/09:00/16:59/17:00
- weekends
- unknown zone id
- negative weeks

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 19: Zoned Meeting Scheduler`

## Hints (optional)

<details><summary>Hint 1</summary>

`LocalDateTime.atZone(zone)` interprets the wall-clock value in that zone; `withZoneSameInstant` then re-expresses the same instant.

</details>

<details><summary>Hint 2</summary>

`ZonedDateTime.plusWeeks` is calendar arithmetic; `plus(Duration)` is elapsed arithmetic.

</details>
