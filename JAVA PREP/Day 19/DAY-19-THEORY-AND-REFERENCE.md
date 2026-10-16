# Day 19 — Date/Time API (java.time) and NIO.2 Files and Path

**Phase:** Core Java  
**Primary theme:** Model time correctly (dates, instants, zones, durations) and do safe, portable file I/O with `Path` and `Files`.  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-localdate-span`, `task-02-zoned-meeting`, `task-03-path-normalize`, `task-04-files-read-write`  
**Instruction alignment:** Maps to the Day 19 entry of the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21 (no Spring today)

## Overview

Time bugs are among the most expensive in backend systems: invoices on the wrong day, meetings off by an hour after DST, tokens that expire in the wrong zone. The old `java.util.Date`/`Calendar`/`SimpleDateFormat` classes were mutable, non-thread-safe, and confusing; since Java 8 the immutable, thread-safe **`java.time`** API replaces them. The rule of thumb: **store and transmit instants (UTC), compute in the zone the business cares about, and display in the user's zone.**

File I/O is the other half of today. **NIO.2** (`java.nio.file`) gives you `Path` (a location, not a file) and `Files` (operations), with explicit charsets and proper exceptions. It also introduces the classic security topic of **path traversal** (`../../etc/passwd`). Interviews ask: *LocalDateTime vs ZonedDateTime vs Instant*, *Period vs Duration*, *how do you test time-dependent code*, *Path vs File*, *how do you read a big file lazily*.

## Day roadmap

1. java.time core types, spans, formatting, and Clock
2. Time zones, offsets, DST, and ZonedDateTime
3. NIO.2: Path, Files, charsets, and path-traversal safety
4. Interview angles
5. Common mistakes & debugging
6. Further reading, glossary, answers

### java.time core types, spans, formatting, and Clock

#### What it is

`LocalDate` (date, no time/zone), `LocalTime`, `LocalDateTime` (date+time, no zone - **not an instant**), `Instant` (a point on the UTC timeline, nanosecond precision), `Duration` (time-based amount: seconds/nanos), `Period` (date-based amount: years/months/days). All are **immutable**; operations return new objects (`date.plusDays(3)`). `ChronoUnit.DAYS.between(a, b)` counts whole units; `Period.between(a, b)` gives a human breakdown. `TemporalAdjusters` (`firstDayOfNextMonth`, `next(DayOfWeek.MONDAY)`) adjust dates. `DateTimeFormatter` formats/parses (thread-safe); `ISO_LOCAL_DATE` is the default format. `Clock` abstracts "now": `LocalDate.now(clock)`.

#### Why it exists / why it matters

Business rules revolve around calendar math: due dates, ages, billing cycles, business days. Immutability makes dates safe as map keys and across threads. Injecting a `Clock` is how you unit-test "is this invoice overdue today?" deterministically with `Clock.fixed(...)` instead of depending on the machine clock.

#### Pros and cons

**Pros**

- Immutable and thread-safe (unlike `Date`/`SimpleDateFormat`)
- Clear types: date vs time vs instant vs amount
- Rich arithmetic and adjusters; correct month-end/leap-year handling
- `Clock` injection enables deterministic tests

**Cons / tradeoffs**

- Many types to choose from; `LocalDateTime` is easily misused as if it were an instant
- Month lengths and leap years still produce surprising results (`Jan 31 + 1 month` = `Feb 28/29`)
- Legacy APIs (`java.sql.Date`, `Calendar`) still appear and need conversion

#### What happens without it / when misused

Using `LocalDateTime` for event timestamps loses the zone, so two servers in different zones disagree. `Duration.between(date1, date2)` on `LocalDate` throws `UnsupportedTemporalTypeException` (use `ChronoUnit.DAYS` / `Period`). `LocalDate.of(2023, 2, 29)` throws `DateTimeException`. `SimpleDateFormat` shared across threads produces garbage. Calling `LocalDate.now()` inside business logic makes tests fail depending on the day they run. `Period.ofDays(30)` is **not** one month; `plusMonths(1)` on Jan 31 gives Feb 28 (clamped, not an error).

#### Syntax and rules

- Create: `LocalDate.of(2024, Month.MAY, 17)`, `LocalDate.parse("2024-05-17")`, `Instant.now()`, `Duration.ofMinutes(90)`, `Period.of(1, 2, 3)`.
- Compare: `a.isBefore(b)`, `a.isAfter(b)`, `a.equals(b)`, `a.compareTo(b)`.
- Span: `ChronoUnit.DAYS.between(a, b)` (end exclusive, negative if reversed); `Period.between(a, b)` -> `getYears()/getMonths()/getDays()`.
- Adjust: `date.with(TemporalAdjusters.next(DayOfWeek.MONDAY))`, `date.withDayOfMonth(1)`, `date.with(TemporalAdjusters.lastDayOfMonth())`.
- Day of week: `date.getDayOfWeek()` -> `DayOfWeek.SATURDAY`/`SUNDAY` for weekends.
- Format: `DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")`; `yyyy` (year) vs `YYYY` (week-year) - use `yyyy`.
- Testability: pass a `Clock` into constructors/methods; tests use `Clock.fixed(Instant.parse("2024-05-20T10:00:00Z"), ZoneOffset.UTC)`.

#### Examples

**Example 1.1 — Tiny — spans and breakdowns**

```java
LocalDate a = LocalDate.of(2020, 1, 31);
LocalDate b = LocalDate.of(2021, 3, 2);
System.out.println(ChronoUnit.DAYS.between(a, b));      // 396
Period p = Period.between(a, b);
System.out.println(p.getYears() + "y " + p.getMonths() + "m " + p.getDays() + "d");  // 1y 1m 2d
System.out.println(a.plusMonths(1));                    // 2020-02-29 (clamped to month end)
```

**Example 1.2 — Tiny — adjusters and weekdays**

```java
LocalDate fri = LocalDate.of(2024, 5, 17);
System.out.println(fri.getDayOfWeek());                              // FRIDAY
System.out.println(fri.with(TemporalAdjusters.next(DayOfWeek.MONDAY)));   // 2024-05-20
System.out.println(fri.with(TemporalAdjusters.lastDayOfMonth()));    // 2024-05-31
```

**Example 1.3 — Medium — deterministic overdue check with an injected Clock**

```java
import java.time.*;

public class Invoice {
    private final LocalDate due;
    private final Clock clock;

    public Invoice(LocalDate due, Clock clock) { this.due = due; this.clock = clock; }

    public boolean isOverdue() { return LocalDate.now(clock).isAfter(due); }

    public static void main(String[] args) {
        Clock may20 = Clock.fixed(Instant.parse("2024-05-20T10:00:00Z"), ZoneOffset.UTC);
        System.out.println(new Invoice(LocalDate.of(2024, 5, 19), may20).isOverdue());  // true
        System.out.println(new Invoice(LocalDate.of(2024, 5, 20), may20).isOverdue());  // false
    }
}
```

#### Quick checks

1. What is the difference between `Period` and `Duration`?
2. Why is `LocalDateTime` a poor choice for a stored event timestamp?
3. What is `LocalDate.of(2024,1,31).plusMonths(1)`?
4. How do you make `isOverdue()` unit-testable?

### Time zones, offsets, DST, and ZonedDateTime

#### What it is

A **`ZoneId`** (`Asia/Kolkata`, `America/New_York`) names a set of rules (offset history + DST); a **`ZoneOffset`** (`+05:30`) is a fixed difference from UTC. `ZonedDateTime` = `LocalDateTime` + `ZoneId` (+ the resolved offset); `OffsetDateTime` = `LocalDateTime` + `ZoneOffset`; `Instant` = a point on the UTC timeline. `zdt.withZoneSameInstant(otherZone)` changes the displayed zone but keeps the instant; `withZoneSameLocal` keeps the wall-clock time and changes the instant. During DST transitions the wall clock has a **gap** (spring forward, local times that never exist) and an **overlap** (fall back, local times that occur twice).

#### Why it exists / why it matters

Global systems schedule meetings, expire tokens, and bill by calendar day across zones. Using zone IDs (not hard-coded offsets) lets the JDK apply historical and future DST rules (from the IANA tz database that ships with the JDK). Knowing when arithmetic is **wall-clock** (`ZonedDateTime.plusDays/plusWeeks`) versus **elapsed time** (`plus(Duration)`, `Instant` math) prevents the classic "the meeting moved an hour" bug.

#### Pros and cons

**Pros**

- Correct DST handling by zone rules
- Explicit conversion between instants and local times
- ISO-8601 support for APIs (`Instant.parse`, `OffsetDateTime.parse`)
- UTC storage + zone-based display avoids ambiguity

**Cons / tradeoffs**

- Zone rules change (governments update DST); old JDKs have stale tzdata
- Gaps and overlaps need explicit policy
- More conversion steps between database, JSON, and UI representations

#### What happens without it / when misused

Hard-coding `+05:30` or assuming `UTC-5` for New York is wrong half the year. Adding `Duration.ofDays(7)` to a `ZonedDateTime` across a DST change moves the *wall-clock* time by an hour (it adds exactly 168 hours) while `plusWeeks(1)` keeps the local time. Scheduling at a local time inside the spring-forward **gap** silently shifts the time forward (02:30 becomes 03:30). Using `ZoneId.of("EST")` (a legacy short ID) ignores daylight saving; `ZoneId.of("Mars/Base")` throws `ZoneRulesException` (a `DateTimeException`). Storing a local time without zone for a customer in another zone makes reports wrong.

#### Syntax and rules

- `ZoneId.of("America/New_York")`; list: `ZoneId.getAvailableZoneIds()`; `ZoneId.systemDefault()` (avoid in business logic).
- `ZonedDateTime.of(localDateTime, zone)`; `localDateTime.atZone(zone)`; `instant.atZone(zone)`.
- Change display zone, same instant: `zdt.withZoneSameInstant(ZoneId.of("UTC"))`.
- Wall-clock arithmetic: `zdt.plusDays(n)`, `plusWeeks(n)`; elapsed arithmetic: `zdt.plus(Duration.ofHours(n))`, `Duration.between(a, b)`.
- DST gap/overlap: `zdt.withEarlierOffsetAtOverlap()`, `withLaterOffsetAtOverlap()`; gaps move forward by the gap length.
- Serialize: `Instant.toString()` (`2024-05-20T09:00:00Z`), `OffsetDateTime.toString()`, ISO formatters.
- Business hours check: use the **meeting's local zone**, e.g. `t.getDayOfWeek()` and `t.toLocalTime()`.

#### Examples

**Example 2.1 — Tiny — same instant in several zones**

```java
Instant meeting = Instant.parse("2024-05-20T12:00:00Z");
for (String id : List.of("Asia/Kolkata", "America/New_York", "Europe/London")) {
    System.out.println(id + " -> " + meeting.atZone(ZoneId.of(id)).toLocalDateTime());
}
// Asia/Kolkata -> 2024-05-20T17:30
// America/New_York -> 2024-05-20T08:00
// Europe/London -> 2024-05-20T13:00
```

**Example 2.2 — Tiny — DST: elapsed time vs wall-clock time**

```java
ZoneId ny = ZoneId.of("America/New_York");
ZonedDateTime start = ZonedDateTime.of(2024, 3, 4, 10, 0, 0, 0, ny);       // before DST starts on Mar 10
System.out.println(start.plusWeeks(1));                  // 2024-03-11T10:00-04:00[America/New_York]  (wall clock kept)
System.out.println(start.plus(Duration.ofDays(7)));      // 2024-03-11T11:00-04:00[America/New_York]  (exactly 168 h)

ZonedDateTime a = ZonedDateTime.of(2024, 3, 10, 1, 30, 0, 0, ny);
ZonedDateTime b = ZonedDateTime.of(2024, 3, 10, 3, 30, 0, 0, ny);
System.out.println(Duration.between(a, b).toMinutes());  // 60, not 120 (02:00-03:00 does not exist)
```

**Example 2.3 — Medium — a tiny meeting planner**

```java
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.*;

public class MeetingPlanner {
    private static final DateTimeFormatter F = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm");

    public static List<String> localTimes(Instant when, List<String> zoneIds) {
        List<String> out = new ArrayList<>();
        for (String id : zoneIds) out.add(when.atZone(ZoneId.of(id)).format(F));   // ZoneId.of throws on bad id
        return out;
    }

    public static boolean duringWork(ZonedDateTime t) {
        DayOfWeek d = t.getDayOfWeek();
        LocalTime time = t.toLocalTime();
        boolean weekday = d != DayOfWeek.SATURDAY && d != DayOfWeek.SUNDAY;
        return weekday && !time.isBefore(LocalTime.of(9, 0)) && time.isBefore(LocalTime.of(17, 0));
    }

    public static void main(String[] args) {
        Instant m = Instant.parse("2024-05-20T03:30:00Z");
        System.out.println(localTimes(m, List.of("Asia/Kolkata", "America/New_York")));
        // [2024-05-20 09:00, 2024-05-19 23:30]
        System.out.println(duringWork(m.atZone(ZoneId.of("Asia/Kolkata"))));   // true
    }
}
```

#### Quick checks

1. Instant vs ZonedDateTime vs LocalDateTime - when do you use each?
2. Why does `plus(Duration.ofDays(7))` differ from `plusWeeks(1)` across DST?
3. How long is 01:30 to 03:30 on a spring-forward day in New York?
4. Why is `ZoneId.of("EST")` risky?

### NIO.2: Path, Files, charsets, and path-traversal safety

#### What it is

`java.nio.file.Path` is an immutable, platform-aware **location** (it need not exist). Key operations: `resolve` (join), `resolveSibling`, `relativize`, `normalize` (collapse `.`/`..`), `toAbsolutePath`, `getFileName`, `getParent`, `startsWith`, iteration over name elements. `Files` offers static operations: `readString/writeString`, `readAllLines/write(lines)`, `lines` and `list`/`walk` (lazy, **must be closed**), `newBufferedReader/Writer`, `copy/move` with `StandardCopyOption`, `createDirectories`, `delete/deleteIfExists`, `exists/isRegularFile`, `size`. Always pass an explicit `Charset` (`StandardCharsets.UTF_8`) where an overload exists; `readString/writeString` default to UTF-8, `FileReader`/`FileWriter` historically used the platform default (UTF-8 by default only since Java 18).

#### Why it exists / why it matters

`java.io.File` mixed paths with operations, returned booleans instead of exceptions, and handled symlinks, attributes, and atomic moves poorly. NIO.2 gives precise exceptions (`NoSuchFileException`, `FileAlreadyExistsException`, `AccessDeniedException`), atomic/replace options, and lazy streams for large files. Server-side code that builds file paths from user input must guard against **path traversal**: `base.resolve("../../etc/passwd")` escapes the base directory unless you normalize and check `startsWith(base)`.

#### Pros and cons

**Pros**

- Clear separation of location (`Path`) and operations (`Files`)
- Precise exceptions and options (`REPLACE_EXISTING`, `ATOMIC_MOVE`, `CREATE_NEW`)
- Lazy line/directory streams support huge files
- Explicit charsets prevent mojibake

**Cons / tradeoffs**

- `Files.lines/list/walk` hold OS handles - forgetting try-with-resources leaks them
- `readAllLines`/`readString` load the whole file into memory
- Checked `IOException` forces wrapping (`UncheckedIOException`) in lambdas and APIs

#### What happens without it / when misused

Using the platform-default charset corrupts non-ASCII text (`MalformedInputException: Input length = 1` or silent `?`). `Files.lines(path).forEach(...)` without closing leaks file descriptors under load (`Too many open files`). `Files.readAllLines` on a 10 GB log triggers `OutOfMemoryError`. Concatenating user input into a path string (`"/data/" + name`) lets `../` escape the directory; `Path.resolve("/etc/passwd")` with an **absolute** argument *replaces* the base entirely. `Files.copy` without `REPLACE_EXISTING` throws `FileAlreadyExistsException`. Comparing paths as strings fails on case-insensitive file systems and unnormalized forms.

#### Syntax and rules

- Build: `Path p = Path.of("data", "2024", "a.txt");`, `base.resolve("x/y.txt")`, `base.relativize(target)`.
- Clean: `p.normalize()` removes `.` and `..` segments *lexically* (does not touch the disk or follow symlinks); `toRealPath()` resolves symlinks and requires existence.
- **Safe resolve:** `Path n = base.toAbsolutePath().normalize(); Path r = n.resolve(user).normalize(); if (!r.startsWith(n)) throw ...`.
- Read: `Files.readString(p)`, `Files.readAllLines(p, UTF_8)`, lazy: `try (Stream<String> s = Files.lines(p)) { ... }`.
- Write: `Files.writeString(p, text)` (truncates), `Files.write(p, lines, UTF_8)`, append: `Files.writeString(p, s, CREATE, APPEND)`.
- Directories: `Files.createDirectories(p.getParent())`; list one level: `try (Stream<Path> s = Files.list(dir))`.
- Tests: JUnit 5 `@TempDir Path tmp` creates an isolated directory deleted afterward - never write to the project tree.

#### Examples

**Example 3.1 — Tiny — path manipulation without touching the disk**

```java
Path p = Path.of("/srv/data/reports/../reports/./q1.txt");
System.out.println(p.normalize());                                  // /srv/data/reports/q1.txt
System.out.println(Path.of("/srv/data").relativize(p.normalize())); // reports/q1.txt
System.out.println(p.getFileName() + " in " + p.getParent().getFileName()); // q1.txt in reports
```

**Example 3.2 — Tiny — read and write with explicit charset**

```java
Path file = Files.createTempFile("demo", ".txt");
Files.write(file, List.of("héllo", "wörld"), StandardCharsets.UTF_8);
List<String> lines = Files.readAllLines(file, StandardCharsets.UTF_8);
System.out.println(lines);                  // [héllo, wörld]
try (Stream<String> s = Files.lines(file, StandardCharsets.UTF_8)) {
    System.out.println(s.count());           // 2
}
Files.deleteIfExists(file);
```

**Example 3.3 — Medium — a path-traversal-safe resolver**

```java
import java.nio.file.Path;

public final class SafePaths {
    public static Path resolveSafe(Path base, String userPath) {
        Path root = base.toAbsolutePath().normalize();
        Path resolved = root.resolve(userPath).normalize();   // an absolute userPath replaces root!
        if (!resolved.startsWith(root)) {
            throw new IllegalArgumentException("path escapes base directory: " + userPath);
        }
        return resolved;
    }

    public static void main(String[] args) {
        Path base = Path.of("/srv/data");
        System.out.println(resolveSafe(base, "a/../b.txt"));        // /srv/data/b.txt
        try { resolveSafe(base, "../etc/passwd"); }
        catch (IllegalArgumentException e) { System.out.println("blocked"); }   // blocked
        try { resolveSafe(base, "/etc/passwd"); }
        catch (IllegalArgumentException e) { System.out.println("blocked"); }   // blocked
    }
}
```

#### Quick checks

1. Why must you close the stream returned by `Files.lines`?
2. What does `Path.of("/data").resolve("/etc/passwd")` return?
3. What does `normalize()` do and not do?
4. Which JUnit 5 feature gives you a safe scratch directory?

## Interview angles

**Q: Why was java.time introduced and what is wrong with java.util.Date?**

`Date` is mutable, not thread-safe, has confusing indexes and a misleading name (it is an instant), and `SimpleDateFormat` is not thread-safe. `java.time` is immutable, explicit about zones, and fluent.

**Q: How would you store a user's appointment time?**

Store an `Instant` (UTC) plus the user's `ZoneId` (or store `LocalDateTime` + `ZoneId` if the appointment is defined in local wall-clock terms), convert for display.

**Q: How do you unit test code that depends on the current time?**

Inject `java.time.Clock`; use `Clock.fixed(...)` in tests and `Clock.systemUTC()` in production.

**Q: Path vs File?**

`Path` is the modern NIO.2 location type with better operations and precise exceptions; `File` is legacy and mixes location with operations.

**Q: How do you read a huge file safely?**

Stream lazily with `Files.lines`/`BufferedReader` inside try-with-resources instead of `readAllLines`.

**Q: What is path traversal and how do you prevent it?**

Using user input in a path so that `..` or an absolute path escapes the intended directory. Normalize the resolved path and verify `startsWith(baseDir)`; consider `toRealPath` to defeat symlink tricks.

## Common mistakes & debugging

- Treating `LocalDateTime` as an instant or comparing local times from different zones.
- Hard-coded offsets (`+05:30`, `UTC-5`) instead of `ZoneId`s with DST rules.
- `YYYY` instead of `yyyy` in formatter patterns (week-based year bug around New Year).
- `Duration.between` on `LocalDate`, or `Period.ofDays(30)` as "one month".
- Not closing `Files.lines/list/walk` streams; using default charsets; `readAllLines` on huge files.
- Concatenating user-provided file names onto base paths without normalize + `startsWith` check.

## Further reading

- Javadoc: `java.time` package summary, `ZonedDateTime`, `Clock`, `DateTimeFormatter`, `TemporalAdjusters`
- Oracle Java Tutorials - *Date Time* trail and *Essential Java Classes: Basic I/O (File I/O with NIO.2)*
- Javadoc: `java.nio.file.Path`, `Files`, `StandardOpenOption`, `StandardCopyOption`
- OWASP: Path Traversal (concept and mitigations); JUnit 5 user guide - `@TempDir`

## Glossary

| Term | Meaning |
|------|---------|
| Instant | A point on the UTC timeline |
| ZoneId | Region-based time-zone rules (e.g. `Europe/London`) |
| ZoneOffset | Fixed difference from UTC (e.g. `+05:30`) |
| DST gap / overlap | Local times skipped / repeated when clocks change |
| Wall-clock arithmetic | Calendar math that keeps local time (`plusDays`) |
| Clock | Source of the current time; injectable for tests |
| Path normalization | Lexically removing `.` and `..` segments |
| Path traversal | Escaping a base directory via `..` or absolute paths |
| @TempDir | JUnit 5 annotation providing a temporary directory |

## Answers

Answers to every **Quick check** above (numbered `section.question`).

- **1.1** — What is the difference between `Period` and `Duration`?  
  `Period` is date-based (years, months, days); `Duration` is time-based (seconds, nanos). `Duration.between` on `LocalDate` is unsupported.

- **1.2** — Why is `LocalDateTime` a poor choice for a stored event timestamp?  
  It has no zone/offset, so it does not identify a single instant; store `Instant` (or `OffsetDateTime`/`ZonedDateTime`).

- **1.3** — What is `LocalDate.of(2024,1,31).plusMonths(1)`?  
  `2024-02-29` - day clamped to the last valid day of the month.

- **1.4** — How do you make `isOverdue()` unit-testable?  
  Inject a `Clock` and use `LocalDate.now(clock)`; tests pass `Clock.fixed(...)`.

- **2.1** — Instant vs ZonedDateTime vs LocalDateTime - when do you use each?  
  `Instant`: store/compare moments in UTC. `ZonedDateTime`: calendar logic in a specific zone (meetings, DST-aware). `LocalDateTime`: wall-clock value with no zone, e.g. a user-entered schedule before the zone is known.

- **2.2** — Why does `plus(Duration.ofDays(7))` differ from `plusWeeks(1)` across DST?  
  `Duration` adds exactly 168 hours; `plusWeeks` keeps the local time and recalculates the offset.

- **2.3** — How long is 01:30 to 03:30 on a spring-forward day in New York?  
  One hour; the 02:00-03:00 local hour is skipped.

- **2.4** — Why is `ZoneId.of("EST")` risky?  
  It is a fixed-offset legacy alias with no daylight-saving rules; use `America/New_York`.

- **3.1** — Why must you close the stream returned by `Files.lines`?  
  It holds an open file handle; not closing leaks descriptors. Use try-with-resources.

- **3.2** — What does `Path.of("/data").resolve("/etc/passwd")` return?  
  `/etc/passwd` - resolving an absolute path returns it unchanged.

- **3.3** — What does `normalize()` do and not do?  
  It lexically removes `.` and `..`; it does not access the file system or resolve symlinks (`toRealPath` does).

- **3.4** — Which JUnit 5 feature gives you a safe scratch directory?  
  `@TempDir` (a `Path` or `File` parameter/field), deleted automatically after the test.
