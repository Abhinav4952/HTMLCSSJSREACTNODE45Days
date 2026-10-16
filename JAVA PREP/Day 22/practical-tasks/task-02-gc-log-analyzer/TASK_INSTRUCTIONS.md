# Task 2 — GC Log and JVM Flags Analyzer

**Day:** 22 · **Task ID:** Day22-task02 · **Type:** Plain Java · **Difficulty:** Core

## Summary

Parse JDK unified GC log lines (`-Xlog:gc`), summarize pause behaviour, flag a probable memory leak from a rising post-full-GC live set, and interpret heap/collector flags and byte sizes the way you would while triaging a production incident.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day22/task02/GcLogAnalyzer.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day22/task02/GcLogAnalyzerTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 22 theory file read

## What you will implement

1. `parseSize(text)` converts `512K`, `24M`, `2G`, `100B` (case-insensitive, plain digits = bytes) to bytes; anything else -> `IllegalArgumentException`
2. `formatBytes(bytes)` renders human readable binary units with one decimal (`0 B`, `512 B`, `1.5 KiB`, `2.0 MiB`, `1.0 GiB`); negative -> `IllegalArgumentException`
3. `parseLine(line)` parses a line like `[2.345s][info][gc] GC(12) Pause Young (Normal) (G1 Evacuation Pause) 24M->4M(256M) 5.123ms` into a `GcEvent`, or returns empty for lines that do not describe a sized pause; `full` is true for `Pause Full`
4. `parse(log)` returns the events for all matching lines in order (ignore blank/other lines)
5. `summarize(events)` returns event count, number of full GCs, total and maximum pause millis, and total reclaimed bytes (`before - after` summed)
6. `leakSuspected(events, minConsecutive)` is true when at least `minConsecutive` consecutive **full** GC events have a strictly increasing `afterBytes`
7. `heapSettings(args)` reads `-Xms`, `-Xmx` (sizes like `512m`, `2g`) and the collector flag (`UseG1GC`->`G1`, `UseZGC`->`ZGC`, `UseParallelGC`->`Parallel`, `UseSerialGC`->`Serial`; default `G1`); the last occurrence wins; `Xms > Xmx` -> `IllegalArgumentException`

## Constraints

- Use `java.util.regex` and plain Java - no external libraries
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=GcLogAnalyzerTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **15 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day22-task02)`).

### Run one test class

```bash
mvn -Dtest=GcLogAnalyzerTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `GcLogAnalyzer.java` — `parseSize` | `TODO(Day22-task02)` | match digits + optional B/K/M/G (case-insensitive); K=1024, M=1024^2, G=1024^3; null/blank/unknown unit -> IllegalArgumentException |
| `GcLogAnalyzer.java` — `formatBytes` | `TODO(Day22-task02)` | negative -> IllegalArgumentException; below 1024 print "<n> B"; otherwise divide by 1024 up to TiB and print String.format(Locale.ROOT, "%.1f %s", value, unit) with units KiB, MiB, GiB, TiB |
| `GcLogAnalyzer.java` — `parseLine` | `TODO(Day22-task02)` | apply the LINE pattern (groups: uptime, id, kind, cause text, before, after, committed, pause); trim the cause text; full == kind equals Full; non-matching or null -> Optional.empty() |
| `GcLogAnalyzer.java` — `parse` | `TODO(Day22-task02)` | split on line breaks, keep the events produced by parseLine, preserve order; null/blank -> empty list |
| `GcLogAnalyzer.java` — `summarize` | `TODO(Day22-task02)` | count events and full GCs, sum pauses, track max pause, sum (before - after); empty list gives all zeros |
| `GcLogAnalyzer.java` — `leakSuspected` | `TODO(Day22-task02)` | consider only full GCs in order; true when minConsecutive consecutive full GCs have strictly increasing afterBytes (a run of N events means N-1 increases); minConsecutive < 2 -> IllegalArgumentException |
| `GcLogAnalyzer.java` — `heapSettings` | `TODO(Day22-task02)` | scan args: -Xms<size> / -Xmx<size> via parseSize, -XX:+UseG1GC/UseZGC/UseParallelGC/UseSerialGC set the collector name; last occurrence wins; default collector G1; throw IllegalArgumentException when Xms > Xmx |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_parseSizeUnits`, `r1_parseSizeRejectsGarbage` |
| 2 | `r2_formatBytes` |
| 3 | `r3_parseLineExtractsAllFields`, `r3_parseLineFullAndPaddedTag`, `r3_parseLineIgnoresOtherLines` |
| 4 | `r4_parseKeepsOrderAndSkipsNoise` |
| 5 | `r5_summaryOfTheSampleLog`, `r5_summaryOfNothing` |
| 6 | `r6_leakDetectedOnRisingFloor`, `r6_noLeakWhenFloorDropsOrPlateaus`, `r6_leakInTheSampleLog` |
| 7 | `r7_heapSettingsFromFlags`, `r7_defaultsAndLastWins`, `r7_initialLargerThanMaxIsRejected` |

## Edge cases to handle

- garbage lines in the log
- no events (summary of nothing)
- events that are young GCs between full GCs when looking for leaks
- missing `-Xms`/`-Xmx` flags
- lower-case size suffixes

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 22: GC Log and JVM Flags Analyzer`

## Hints (optional)

<details><summary>Hint 1</summary>

Use one compiled `Pattern` for log lines; `Matcher.matches()` plus named capture indices keeps parsing readable.

</details>

<details><summary>Hint 2</summary>

For `leakSuspected`, a *run length* counter that resets to 1 whenever the floor does not rise is simpler than comparing windows.

</details>

<details><summary>Hint 3</summary>

Remember `-XX:+UseG1GC` is a *flag string*, not something to `startsWith`-parse.

</details>
