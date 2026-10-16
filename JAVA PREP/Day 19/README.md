# Day 19 — Date/Time API (java.time) and NIO.2 Files and Path

## Learning objectives

- Choose the right `java.time` type: `LocalDate`, `LocalDateTime`, `Instant`, `ZonedDateTime`, `OffsetDateTime`, `Duration`, `Period`
- Compute spans, adjust dates, and format/parse with `DateTimeFormatter`
- Explain time zones, offsets, and DST gaps/overlaps, and why you store `Instant`/UTC
- Inject `Clock` to make time-dependent code testable
- Manipulate `Path` values (resolve, normalize, relativize) and prevent path traversal
- Read/write files with `Files` using explicit charsets, try-with-resources, and `@TempDir` in tests

## Prerequisites

- Day 11 — exceptions (`IOException`, try-with-resources)
- Day 17 — streams (`Files.lines`, `Files.list` return streams)
- Day 15 — immutability

## How to use this folder

1. Read [`DAY-19-THEORY-AND-REFERENCE.md`](DAY-19-THEORY-AND-REFERENCE.md) first.
2. Open each task folder under `practical-tasks/` as its own Maven project in IntelliJ.
3. Run `mvn test` (**red**), implement the `TODO(Day19-taskYY)` stubs, run `mvn test` again until **green**.
4. Do not edit tests, `TASK_INSTRUCTIONS.md`, or `EVALUATION_CRITERIA.md`.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-localdate-span` | Plain Java | `mvn test` |
| 2 | `task-02-zoned-meeting` | Plain Java | `mvn test` |
| 3 | `task-03-path-normalize` | Plain Java | `mvn test` |
| 4 | `task-04-files-read-write` | Plain Java | `mvn test` |

**Estimated time:** 2–3 h theory + 3–5 h tasks  
**Phase:** Core Java
