from gen_helpers import sec, task

DAY = dict(
    num=19,
    title="Date/Time API (java.time) and NIO.2 Files and Path",
    theme="Model time correctly (dates, instants, zones, durations) and do safe, portable file I/O with `Path` and `Files`.",
    objectives=[
        "Choose the right `java.time` type: `LocalDate`, `LocalDateTime`, `Instant`, `ZonedDateTime`, `OffsetDateTime`, `Duration`, `Period`",
        "Compute spans, adjust dates, and format/parse with `DateTimeFormatter`",
        "Explain time zones, offsets, and DST gaps/overlaps, and why you store `Instant`/UTC",
        "Inject `Clock` to make time-dependent code testable",
        "Manipulate `Path` values (resolve, normalize, relativize) and prevent path traversal",
        "Read/write files with `Files` using explicit charsets, try-with-resources, and `@TempDir` in tests",
    ],
    prereqs=["Day 11 — exceptions (`IOException`, try-with-resources)", "Day 17 — streams (`Files.lines`, `Files.list` return streams)", "Day 15 — immutability"],
    overview="""Time bugs are among the most expensive in backend systems: invoices on the wrong day, meetings off by an hour after DST, tokens that expire in the wrong zone. The old `java.util.Date`/`Calendar`/`SimpleDateFormat` classes were mutable, non-thread-safe, and confusing; since Java 8 the immutable, thread-safe **`java.time`** API replaces them. The rule of thumb: **store and transmit instants (UTC), compute in the zone the business cares about, and display in the user's zone.**

File I/O is the other half of today. **NIO.2** (`java.nio.file`) gives you `Path` (a location, not a file) and `Files` (operations), with explicit charsets and proper exceptions. It also introduces the classic security topic of **path traversal** (`../../etc/passwd`). Interviews ask: *LocalDateTime vs ZonedDateTime vs Instant*, *Period vs Duration*, *how do you test time-dependent code*, *Path vs File*, *how do you read a big file lazily*.""",
    sections=[
        sec(
            "java.time core types, spans, formatting, and Clock",
            "`LocalDate` (date, no time/zone), `LocalTime`, `LocalDateTime` (date+time, no zone - **not an instant**), `Instant` (a point on the UTC timeline, nanosecond precision), `Duration` (time-based amount: seconds/nanos), `Period` (date-based amount: years/months/days). All are **immutable**; operations return new objects (`date.plusDays(3)`). `ChronoUnit.DAYS.between(a, b)` counts whole units; `Period.between(a, b)` gives a human breakdown. `TemporalAdjusters` (`firstDayOfNextMonth`, `next(DayOfWeek.MONDAY)`) adjust dates. `DateTimeFormatter` formats/parses (thread-safe); `ISO_LOCAL_DATE` is the default format. `Clock` abstracts \"now\": `LocalDate.now(clock)`.",
            "Business rules revolve around calendar math: due dates, ages, billing cycles, business days. Immutability makes dates safe as map keys and across threads. Injecting a `Clock` is how you unit-test \"is this invoice overdue today?\" deterministically with `Clock.fixed(...)` instead of depending on the machine clock.",
            ["Immutable and thread-safe (unlike `Date`/`SimpleDateFormat`)", "Clear types: date vs time vs instant vs amount", "Rich arithmetic and adjusters; correct month-end/leap-year handling", "`Clock` injection enables deterministic tests"],
            ["Many types to choose from; `LocalDateTime` is easily misused as if it were an instant", "Month lengths and leap years still produce surprising results (`Jan 31 + 1 month` = `Feb 28/29`)", "Legacy APIs (`java.sql.Date`, `Calendar`) still appear and need conversion"],
            "Using `LocalDateTime` for event timestamps loses the zone, so two servers in different zones disagree. `Duration.between(date1, date2)` on `LocalDate` throws `UnsupportedTemporalTypeException` (use `ChronoUnit.DAYS` / `Period`). `LocalDate.of(2023, 2, 29)` throws `DateTimeException`. `SimpleDateFormat` shared across threads produces garbage. Calling `LocalDate.now()` inside business logic makes tests fail depending on the day they run. `Period.ofDays(30)` is **not** one month; `plusMonths(1)` on Jan 31 gives Feb 28 (clamped, not an error).",
            """- Create: `LocalDate.of(2024, Month.MAY, 17)`, `LocalDate.parse(\"2024-05-17\")`, `Instant.now()`, `Duration.ofMinutes(90)`, `Period.of(1, 2, 3)`.
- Compare: `a.isBefore(b)`, `a.isAfter(b)`, `a.equals(b)`, `a.compareTo(b)`.
- Span: `ChronoUnit.DAYS.between(a, b)` (end exclusive, negative if reversed); `Period.between(a, b)` -> `getYears()/getMonths()/getDays()`.
- Adjust: `date.with(TemporalAdjusters.next(DayOfWeek.MONDAY))`, `date.withDayOfMonth(1)`, `date.with(TemporalAdjusters.lastDayOfMonth())`.
- Day of week: `date.getDayOfWeek()` -> `DayOfWeek.SATURDAY`/`SUNDAY` for weekends.
- Format: `DateTimeFormatter.ofPattern(\"yyyy-MM-dd HH:mm\")`; `yyyy` (year) vs `YYYY` (week-year) - use `yyyy`.
- Testability: pass a `Clock` into constructors/methods; tests use `Clock.fixed(Instant.parse(\"2024-05-20T10:00:00Z\"), ZoneOffset.UTC)`.""",
            [
                ("Tiny — spans and breakdowns", """LocalDate a = LocalDate.of(2020, 1, 31);
LocalDate b = LocalDate.of(2021, 3, 2);
System.out.println(ChronoUnit.DAYS.between(a, b));      // 396
Period p = Period.between(a, b);
System.out.println(p.getYears() + "y " + p.getMonths() + "m " + p.getDays() + "d");  // 1y 1m 2d
System.out.println(a.plusMonths(1));                    // 2020-02-29 (clamped to month end)"""),
                ("Tiny — adjusters and weekdays", """LocalDate fri = LocalDate.of(2024, 5, 17);
System.out.println(fri.getDayOfWeek());                              // FRIDAY
System.out.println(fri.with(TemporalAdjusters.next(DayOfWeek.MONDAY)));   // 2024-05-20
System.out.println(fri.with(TemporalAdjusters.lastDayOfMonth()));    // 2024-05-31"""),
                ("Medium — deterministic overdue check with an injected Clock", """import java.time.*;

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
}"""),
            ],
            [
                ("What is the difference between `Period` and `Duration`?", "`Period` is date-based (years, months, days); `Duration` is time-based (seconds, nanos). `Duration.between` on `LocalDate` is unsupported."),
                ("Why is `LocalDateTime` a poor choice for a stored event timestamp?", "It has no zone/offset, so it does not identify a single instant; store `Instant` (or `OffsetDateTime`/`ZonedDateTime`)."),
                ("What is `LocalDate.of(2024,1,31).plusMonths(1)`?", "`2024-02-29` - day clamped to the last valid day of the month."),
                ("How do you make `isOverdue()` unit-testable?", "Inject a `Clock` and use `LocalDate.now(clock)`; tests pass `Clock.fixed(...)`."),
            ],
        ),
        sec(
            "Time zones, offsets, DST, and ZonedDateTime",
            "A **`ZoneId`** (`Asia/Kolkata`, `America/New_York`) names a set of rules (offset history + DST); a **`ZoneOffset`** (`+05:30`) is a fixed difference from UTC. `ZonedDateTime` = `LocalDateTime` + `ZoneId` (+ the resolved offset); `OffsetDateTime` = `LocalDateTime` + `ZoneOffset`; `Instant` = a point on the UTC timeline. `zdt.withZoneSameInstant(otherZone)` changes the displayed zone but keeps the instant; `withZoneSameLocal` keeps the wall-clock time and changes the instant. During DST transitions the wall clock has a **gap** (spring forward, local times that never exist) and an **overlap** (fall back, local times that occur twice).",
            "Global systems schedule meetings, expire tokens, and bill by calendar day across zones. Using zone IDs (not hard-coded offsets) lets the JDK apply historical and future DST rules (from the IANA tz database that ships with the JDK). Knowing when arithmetic is **wall-clock** (`ZonedDateTime.plusDays/plusWeeks`) versus **elapsed time** (`plus(Duration)`, `Instant` math) prevents the classic \"the meeting moved an hour\" bug.",
            ["Correct DST handling by zone rules", "Explicit conversion between instants and local times", "ISO-8601 support for APIs (`Instant.parse`, `OffsetDateTime.parse`)", "UTC storage + zone-based display avoids ambiguity"],
            ["Zone rules change (governments update DST); old JDKs have stale tzdata", "Gaps and overlaps need explicit policy", "More conversion steps between database, JSON, and UI representations"],
            "Hard-coding `+05:30` or assuming `UTC-5` for New York is wrong half the year. Adding `Duration.ofDays(7)` to a `ZonedDateTime` across a DST change moves the *wall-clock* time by an hour (it adds exactly 168 hours) while `plusWeeks(1)` keeps the local time. Scheduling at a local time inside the spring-forward **gap** silently shifts the time forward (02:30 becomes 03:30). Using `ZoneId.of(\"EST\")` (a legacy short ID) ignores daylight saving; `ZoneId.of(\"Mars/Base\")` throws `ZoneRulesException` (a `DateTimeException`). Storing a local time without zone for a customer in another zone makes reports wrong.",
            """- `ZoneId.of(\"America/New_York\")`; list: `ZoneId.getAvailableZoneIds()`; `ZoneId.systemDefault()` (avoid in business logic).
- `ZonedDateTime.of(localDateTime, zone)`; `localDateTime.atZone(zone)`; `instant.atZone(zone)`.
- Change display zone, same instant: `zdt.withZoneSameInstant(ZoneId.of(\"UTC\"))`.
- Wall-clock arithmetic: `zdt.plusDays(n)`, `plusWeeks(n)`; elapsed arithmetic: `zdt.plus(Duration.ofHours(n))`, `Duration.between(a, b)`.
- DST gap/overlap: `zdt.withEarlierOffsetAtOverlap()`, `withLaterOffsetAtOverlap()`; gaps move forward by the gap length.
- Serialize: `Instant.toString()` (`2024-05-20T09:00:00Z`), `OffsetDateTime.toString()`, ISO formatters.
- Business hours check: use the **meeting's local zone**, e.g. `t.getDayOfWeek()` and `t.toLocalTime()`.""",
            [
                ("Tiny — same instant in several zones", """Instant meeting = Instant.parse("2024-05-20T12:00:00Z");
for (String id : List.of("Asia/Kolkata", "America/New_York", "Europe/London")) {
    System.out.println(id + " -> " + meeting.atZone(ZoneId.of(id)).toLocalDateTime());
}
// Asia/Kolkata -> 2024-05-20T17:30
// America/New_York -> 2024-05-20T08:00
// Europe/London -> 2024-05-20T13:00"""),
                ("Tiny — DST: elapsed time vs wall-clock time", """ZoneId ny = ZoneId.of("America/New_York");
ZonedDateTime start = ZonedDateTime.of(2024, 3, 4, 10, 0, 0, 0, ny);       // before DST starts on Mar 10
System.out.println(start.plusWeeks(1));                  // 2024-03-11T10:00-04:00[America/New_York]  (wall clock kept)
System.out.println(start.plus(Duration.ofDays(7)));      // 2024-03-11T11:00-04:00[America/New_York]  (exactly 168 h)

ZonedDateTime a = ZonedDateTime.of(2024, 3, 10, 1, 30, 0, 0, ny);
ZonedDateTime b = ZonedDateTime.of(2024, 3, 10, 3, 30, 0, 0, ny);
System.out.println(Duration.between(a, b).toMinutes());  // 60, not 120 (02:00-03:00 does not exist)"""),
                ("Medium — a tiny meeting planner", """import java.time.*;
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
}"""),
            ],
            [
                ("Instant vs ZonedDateTime vs LocalDateTime - when do you use each?", "`Instant`: store/compare moments in UTC. `ZonedDateTime`: calendar logic in a specific zone (meetings, DST-aware). `LocalDateTime`: wall-clock value with no zone, e.g. a user-entered schedule before the zone is known."),
                ("Why does `plus(Duration.ofDays(7))` differ from `plusWeeks(1)` across DST?", "`Duration` adds exactly 168 hours; `plusWeeks` keeps the local time and recalculates the offset."),
                ("How long is 01:30 to 03:30 on a spring-forward day in New York?", "One hour; the 02:00-03:00 local hour is skipped."),
                ("Why is `ZoneId.of(\"EST\")` risky?", "It is a fixed-offset legacy alias with no daylight-saving rules; use `America/New_York`."),
            ],
        ),
        sec(
            "NIO.2: Path, Files, charsets, and path-traversal safety",
            "`java.nio.file.Path` is an immutable, platform-aware **location** (it need not exist). Key operations: `resolve` (join), `resolveSibling`, `relativize`, `normalize` (collapse `.`/`..`), `toAbsolutePath`, `getFileName`, `getParent`, `startsWith`, iteration over name elements. `Files` offers static operations: `readString/writeString`, `readAllLines/write(lines)`, `lines` and `list`/`walk` (lazy, **must be closed**), `newBufferedReader/Writer`, `copy/move` with `StandardCopyOption`, `createDirectories`, `delete/deleteIfExists`, `exists/isRegularFile`, `size`. Always pass an explicit `Charset` (`StandardCharsets.UTF_8`) where an overload exists; `readString/writeString` default to UTF-8, `FileReader`/`FileWriter` historically used the platform default (UTF-8 by default only since Java 18).",
            "`java.io.File` mixed paths with operations, returned booleans instead of exceptions, and handled symlinks, attributes, and atomic moves poorly. NIO.2 gives precise exceptions (`NoSuchFileException`, `FileAlreadyExistsException`, `AccessDeniedException`), atomic/replace options, and lazy streams for large files. Server-side code that builds file paths from user input must guard against **path traversal**: `base.resolve(\"../../etc/passwd\")` escapes the base directory unless you normalize and check `startsWith(base)`.",
            ["Clear separation of location (`Path`) and operations (`Files`)", "Precise exceptions and options (`REPLACE_EXISTING`, `ATOMIC_MOVE`, `CREATE_NEW`)", "Lazy line/directory streams support huge files", "Explicit charsets prevent mojibake"],
            ["`Files.lines/list/walk` hold OS handles - forgetting try-with-resources leaks them", "`readAllLines`/`readString` load the whole file into memory", "Checked `IOException` forces wrapping (`UncheckedIOException`) in lambdas and APIs"],
            "Using the platform-default charset corrupts non-ASCII text (`MalformedInputException: Input length = 1` or silent `?`). `Files.lines(path).forEach(...)` without closing leaks file descriptors under load (`Too many open files`). `Files.readAllLines` on a 10 GB log triggers `OutOfMemoryError`. Concatenating user input into a path string (`\"/data/\" + name`) lets `../` escape the directory; `Path.resolve(\"/etc/passwd\")` with an **absolute** argument *replaces* the base entirely. `Files.copy` without `REPLACE_EXISTING` throws `FileAlreadyExistsException`. Comparing paths as strings fails on case-insensitive file systems and unnormalized forms.",
            """- Build: `Path p = Path.of(\"data\", \"2024\", \"a.txt\");`, `base.resolve(\"x/y.txt\")`, `base.relativize(target)`.
- Clean: `p.normalize()` removes `.` and `..` segments *lexically* (does not touch the disk or follow symlinks); `toRealPath()` resolves symlinks and requires existence.
- **Safe resolve:** `Path n = base.toAbsolutePath().normalize(); Path r = n.resolve(user).normalize(); if (!r.startsWith(n)) throw ...`.
- Read: `Files.readString(p)`, `Files.readAllLines(p, UTF_8)`, lazy: `try (Stream<String> s = Files.lines(p)) { ... }`.
- Write: `Files.writeString(p, text)` (truncates), `Files.write(p, lines, UTF_8)`, append: `Files.writeString(p, s, CREATE, APPEND)`.
- Directories: `Files.createDirectories(p.getParent())`; list one level: `try (Stream<Path> s = Files.list(dir))`.
- Tests: JUnit 5 `@TempDir Path tmp` creates an isolated directory deleted afterward - never write to the project tree.""",
            [
                ("Tiny — path manipulation without touching the disk", """Path p = Path.of("/srv/data/reports/../reports/./q1.txt");
System.out.println(p.normalize());                                  // /srv/data/reports/q1.txt
System.out.println(Path.of("/srv/data").relativize(p.normalize())); // reports/q1.txt
System.out.println(p.getFileName() + " in " + p.getParent().getFileName()); // q1.txt in reports"""),
                ("Tiny — read and write with explicit charset", """Path file = Files.createTempFile("demo", ".txt");
Files.write(file, List.of("héllo", "wörld"), StandardCharsets.UTF_8);
List<String> lines = Files.readAllLines(file, StandardCharsets.UTF_8);
System.out.println(lines);                  // [héllo, wörld]
try (Stream<String> s = Files.lines(file, StandardCharsets.UTF_8)) {
    System.out.println(s.count());           // 2
}
Files.deleteIfExists(file);"""),
                ("Medium — a path-traversal-safe resolver", """import java.nio.file.Path;

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
}"""),
            ],
            [
                ("Why must you close the stream returned by `Files.lines`?", "It holds an open file handle; not closing leaks descriptors. Use try-with-resources."),
                ("What does `Path.of(\"/data\").resolve(\"/etc/passwd\")` return?", "`/etc/passwd` - resolving an absolute path returns it unchanged."),
                ("What does `normalize()` do and not do?", "It lexically removes `.` and `..`; it does not access the file system or resolve symlinks (`toRealPath` does)."),
                ("Which JUnit 5 feature gives you a safe scratch directory?", "`@TempDir` (a `Path` or `File` parameter/field), deleted automatically after the test."),
            ],
        ),
    ],
    interview=[
        ("Why was java.time introduced and what is wrong with java.util.Date?", "`Date` is mutable, not thread-safe, has confusing indexes and a misleading name (it is an instant), and `SimpleDateFormat` is not thread-safe. `java.time` is immutable, explicit about zones, and fluent."),
        ("How would you store a user's appointment time?", "Store an `Instant` (UTC) plus the user's `ZoneId` (or store `LocalDateTime` + `ZoneId` if the appointment is defined in local wall-clock terms), convert for display."),
        ("How do you unit test code that depends on the current time?", "Inject `java.time.Clock`; use `Clock.fixed(...)` in tests and `Clock.systemUTC()` in production."),
        ("Path vs File?", "`Path` is the modern NIO.2 location type with better operations and precise exceptions; `File` is legacy and mixes location with operations."),
        ("How do you read a huge file safely?", "Stream lazily with `Files.lines`/`BufferedReader` inside try-with-resources instead of `readAllLines`."),
        ("What is path traversal and how do you prevent it?", "Using user input in a path so that `..` or an absolute path escapes the intended directory. Normalize the resolved path and verify `startsWith(baseDir)`; consider `toRealPath` to defeat symlink tricks."),
    ],
    mistakes=[
        "Treating `LocalDateTime` as an instant or comparing local times from different zones.",
        "Hard-coded offsets (`+05:30`, `UTC-5`) instead of `ZoneId`s with DST rules.",
        "`YYYY` instead of `yyyy` in formatter patterns (week-based year bug around New Year).",
        "`Duration.between` on `LocalDate`, or `Period.ofDays(30)` as \"one month\".",
        "Not closing `Files.lines/list/walk` streams; using default charsets; `readAllLines` on huge files.",
        "Concatenating user-provided file names onto base paths without normalize + `startsWith` check.",
    ],
    reading=[
        "Javadoc: `java.time` package summary, `ZonedDateTime`, `Clock`, `DateTimeFormatter`, `TemporalAdjusters`",
        "Oracle Java Tutorials - *Date Time* trail and *Essential Java Classes: Basic I/O (File I/O with NIO.2)*",
        "Javadoc: `java.nio.file.Path`, `Files`, `StandardOpenOption`, `StandardCopyOption`",
        "OWASP: Path Traversal (concept and mitigations); JUnit 5 user guide - `@TempDir`",
    ],
    glossary=[
        ("Instant", "A point on the UTC timeline"),
        ("ZoneId", "Region-based time-zone rules (e.g. `Europe/London`)"),
        ("ZoneOffset", "Fixed difference from UTC (e.g. `+05:30`)"),
        ("DST gap / overlap", "Local times skipped / repeated when clocks change"),
        ("Wall-clock arithmetic", "Calendar math that keeps local time (`plusDays`)"),
        ("Clock", "Source of the current time; injectable for tests"),
        ("Path normalization", "Lexically removing `.` and `..` segments"),
        ("Path traversal", "Escaping a base directory via `..` or absolute paths"),
        ("@TempDir", "JUnit 5 annotation providing a temporary directory"),
    ],
    tasks=[
        task(
            "localdate-span", "LocalDate Spans and Business Days", "Warm-up", "LocalDateSpan",
            "Do calendar math with `LocalDate`: compute ages, add business days, enumerate date ranges, format a human-readable span, and check overdue status with an injected `Clock`.",
            [
                "`ageOn(birth, on)` returns the completed years on that day; `birth` after `on` throws `IllegalArgumentException` (leap-day births handled by `Period`)",
                "`addBusinessDays(start, n)` skips Saturdays and Sundays; `n == 0` returns `start` unchanged; `n < 0` throws `IllegalArgumentException`",
                "`datesBetween(startInclusive, endExclusive)` lists every date; equal dates give an empty list; `end` before `start` throws `IllegalArgumentException`",
                "`humanSpan(from, to)` returns `\"<y>y <m>m <d>d\"` using `Period.between`; `to` before `from` throws `IllegalArgumentException`",
                "`nextWeekday(from, dayOfWeek)` returns the next occurrence **strictly after** `from`",
                "`isOverdue(due, clock)` is true when today (per the clock) is after `due`",
            ],
            ["leap-day birthdays", "weekend start for business days", "month/year boundaries in ranges", "same-day comparisons for overdue"],
            {"LocalDateSpan.java": r'''package @PKG@;

import java.time.Clock;
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.Period;
import java.time.temporal.TemporalAdjusters;
import java.util.ArrayList;
import java.util.List;

/** Calendar math with java.time. */
public final class LocalDateSpan {

    private LocalDateSpan() {
    }

    public static int ageOn(LocalDate birth, LocalDate on) {
        //@TODO ageOn | completed years between birth and on (Period.between(...).getYears()); IllegalArgumentException if birth is after on
        if (birth.isAfter(on)) {
            throw new IllegalArgumentException("birth must not be after the reference date");
        }
        return Period.between(birth, on).getYears();
        //@END
    }

    public static LocalDate addBusinessDays(LocalDate start, int n) {
        //@TODO addBusinessDays | move forward n weekdays skipping Saturday/Sunday; n == 0 returns start; negative n -> IllegalArgumentException
        if (n < 0) {
            throw new IllegalArgumentException("n must be >= 0");
        }
        LocalDate date = start;
        int remaining = n;
        while (remaining > 0) {
            date = date.plusDays(1);
            DayOfWeek day = date.getDayOfWeek();
            if (day != DayOfWeek.SATURDAY && day != DayOfWeek.SUNDAY) {
                remaining--;
            }
        }
        return date;
        //@END
    }

    public static List<LocalDate> datesBetween(LocalDate startInclusive, LocalDate endExclusive) {
        //@TODO datesBetween | every date from startInclusive up to (not including) endExclusive; equal -> empty; end before start -> IllegalArgumentException
        if (endExclusive.isBefore(startInclusive)) {
            throw new IllegalArgumentException("end must not be before start");
        }
        List<LocalDate> dates = new ArrayList<>();
        for (LocalDate d = startInclusive; d.isBefore(endExclusive); d = d.plusDays(1)) {
            dates.add(d);
        }
        return dates;
        //@END
    }

    public static String humanSpan(LocalDate from, LocalDate to) {
        //@TODO humanSpan | format Period.between(from, to) as "<years>y <months>m <days>d"; IllegalArgumentException if to is before from
        if (to.isBefore(from)) {
            throw new IllegalArgumentException("to must not be before from");
        }
        Period p = Period.between(from, to);
        return p.getYears() + "y " + p.getMonths() + "m " + p.getDays() + "d";
        //@END
    }

    public static LocalDate nextWeekday(LocalDate from, DayOfWeek dayOfWeek) {
        //@TODO nextWeekday | the next date strictly after from that falls on dayOfWeek (TemporalAdjusters.next)
        return from.with(TemporalAdjusters.next(dayOfWeek));
        //@END
    }

    public static boolean isOverdue(LocalDate due, Clock clock) {
        //@TODO isOverdue | true when LocalDate.now(clock) is after due (never call LocalDate.now() without the clock)
        return LocalDate.now(clock).isAfter(due);
        //@END
    }
}
'''},
            {"LocalDateSpanTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.Clock;
import java.time.DayOfWeek;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;
import org.junit.jupiter.api.Test;

class LocalDateSpanTest {

    @Test
    void r1_ageOnBirthday() {
        LocalDate birth = LocalDate.of(1990, 5, 15);
        assertThat(LocalDateSpan.ageOn(birth, LocalDate.of(2024, 5, 14))).isEqualTo(33);
        assertThat(LocalDateSpan.ageOn(birth, LocalDate.of(2024, 5, 15))).isEqualTo(34);
        assertThat(LocalDateSpan.ageOn(birth, birth)).isZero();
    }

    @Test
    void r1_ageForLeapDayBirthAndInvalidOrder() {
        LocalDate leap = LocalDate.of(2000, 2, 29);
        assertThat(LocalDateSpan.ageOn(leap, LocalDate.of(2023, 2, 28))).isEqualTo(22);
        assertThat(LocalDateSpan.ageOn(leap, LocalDate.of(2023, 3, 1))).isEqualTo(23);
        assertThatThrownBy(() -> LocalDateSpan.ageOn(LocalDate.of(2025, 1, 1), LocalDate.of(2024, 1, 1)))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r2_addBusinessDaysSkipsWeekends() {
        LocalDate friday = LocalDate.of(2024, 5, 17);
        assertThat(LocalDateSpan.addBusinessDays(friday, 1)).isEqualTo(LocalDate.of(2024, 5, 20));
        assertThat(LocalDateSpan.addBusinessDays(friday, 5)).isEqualTo(LocalDate.of(2024, 5, 24));
        assertThat(LocalDateSpan.addBusinessDays(friday, 0)).isEqualTo(friday);
        LocalDate saturday = LocalDate.of(2024, 5, 18);
        assertThat(LocalDateSpan.addBusinessDays(saturday, 1)).isEqualTo(LocalDate.of(2024, 5, 20));
        assertThat(LocalDateSpan.addBusinessDays(LocalDate.of(2024, 5, 20), 10)).isEqualTo(LocalDate.of(2024, 6, 3));
    }

    @Test
    void r2_negativeBusinessDaysRejected() {
        assertThatThrownBy(() -> LocalDateSpan.addBusinessDays(LocalDate.of(2024, 5, 17), -1))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r3_datesBetween() {
        assertThat(LocalDateSpan.datesBetween(LocalDate.of(2024, 2, 27), LocalDate.of(2024, 3, 2)))
                .containsExactly(LocalDate.of(2024, 2, 27), LocalDate.of(2024, 2, 28), LocalDate.of(2024, 2, 29), LocalDate.of(2024, 3, 1));
        LocalDate same = LocalDate.of(2024, 1, 1);
        assertThat(LocalDateSpan.datesBetween(same, same)).isEmpty();
        assertThatThrownBy(() -> LocalDateSpan.datesBetween(LocalDate.of(2024, 1, 2), LocalDate.of(2024, 1, 1)))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r4_humanSpan() {
        assertThat(LocalDateSpan.humanSpan(LocalDate.of(2020, 1, 31), LocalDate.of(2021, 3, 2))).isEqualTo("1y 1m 2d");
        assertThat(LocalDateSpan.humanSpan(LocalDate.of(2024, 5, 1), LocalDate.of(2024, 5, 1))).isEqualTo("0y 0m 0d");
        assertThat(LocalDateSpan.humanSpan(LocalDate.of(2024, 1, 1), LocalDate.of(2024, 12, 31))).isEqualTo("0y 11m 30d");
        assertThatThrownBy(() -> LocalDateSpan.humanSpan(LocalDate.of(2024, 5, 2), LocalDate.of(2024, 5, 1)))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r5_nextWeekdayIsStrictlyAfter() {
        LocalDate friday = LocalDate.of(2024, 5, 17);
        assertThat(LocalDateSpan.nextWeekday(friday, DayOfWeek.MONDAY)).isEqualTo(LocalDate.of(2024, 5, 20));
        assertThat(LocalDateSpan.nextWeekday(friday, DayOfWeek.FRIDAY)).isEqualTo(LocalDate.of(2024, 5, 24));
        assertThat(LocalDateSpan.nextWeekday(friday, DayOfWeek.SATURDAY)).isEqualTo(LocalDate.of(2024, 5, 18));
    }

    @Test
    void r6_isOverdueUsesTheInjectedClock() {
        Clock may20 = Clock.fixed(Instant.parse("2024-05-20T10:00:00Z"), ZoneOffset.UTC);
        assertThat(LocalDateSpan.isOverdue(LocalDate.of(2024, 5, 19), may20)).isTrue();
        assertThat(LocalDateSpan.isOverdue(LocalDate.of(2024, 5, 20), may20)).isFalse();
        assertThat(LocalDateSpan.isOverdue(LocalDate.of(2024, 5, 21), may20)).isFalse();
    }
}
'''},
            ["`Period.between(birth, on).getYears()` already handles Feb 29 and month ends.", "Loop one day at a time and decrement the counter only on weekdays - simplest correct approach for `addBusinessDays`."],
            ["Uses `java.time` only (no `Date`/`Calendar`)", "`Clock` is injected, never `LocalDate.now()` bare", "Immutability respected (no shared mutable dates)"],
            constraints=["Use `java.time` only - no `java.util.Date`, `Calendar`, or `SimpleDateFormat`", "Do not edit the tests"],
        ),
        task(
            "zoned-meeting", "Zoned Meeting Scheduler", "Core", "ZonedMeeting",
            "Convert and compare moments across time zones: convert a local date-time between zones, render one instant in several zones, check business hours in the meeting's own zone, measure elapsed minutes across a DST jump, schedule weekly recurrences by wall-clock time, and format as UTC.",
            [
                "`convert(local, from, to)` returns the `ZonedDateTime` in zone `to` for the instant described by `local` in zone `from`",
                "`localTimes(instant, zoneIds)` returns `\"yyyy-MM-dd HH:mm\"` strings in the order of `zoneIds`; an unknown zone id throws `java.time.DateTimeException`",
                "`isDuringWorkHours(t)` is true for Monday-Friday from 09:00 (inclusive) to 17:00 (exclusive) in `t`'s own zone",
                "`minutesBetween(a, b)` returns the **elapsed** minutes (DST aware): on 2024-03-10 in `America/New_York`, 01:30 -> 03:30 is 60 minutes",
                "`plusWeeksWallClock(start, weeks)` keeps the local time across DST changes",
                "`formatUtc(t)` returns the ISO-8601 instant string such as `2024-05-20T09:00:00Z`",
            ],
            ["DST spring-forward day", "boundaries 08:59/09:00/16:59/17:00", "weekends", "unknown zone id", "negative weeks"],
            {"ZonedMeeting.java": r'''package @PKG@;

import java.time.DayOfWeek;
import java.time.Duration;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

/** Cross-zone scheduling helpers. */
public final class ZonedMeeting {

    private static final DateTimeFormatter FORMAT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm");

    private ZonedMeeting() {
    }

    public static ZonedDateTime convert(LocalDateTime local, ZoneId from, ZoneId to) {
        //@TODO convert | interpret local in zone from, then return the same instant expressed in zone to (withZoneSameInstant)
        return local.atZone(from).withZoneSameInstant(to);
        //@END
    }

    public static List<String> localTimes(Instant instant, List<String> zoneIds) {
        //@TODO localTimes | for each zone id (in order) format instant.atZone(ZoneId.of(id)) as yyyy-MM-dd HH:mm; unknown id propagates DateTimeException
        List<String> result = new ArrayList<>();
        for (String id : zoneIds) {
            result.add(instant.atZone(ZoneId.of(id)).format(FORMAT));
        }
        return result;
        //@END
    }

    public static boolean isDuringWorkHours(ZonedDateTime t) {
        //@TODO isDuringWorkHours | Monday-Friday and 09:00 <= local time < 17:00 in t's own zone
        DayOfWeek day = t.getDayOfWeek();
        if (day == DayOfWeek.SATURDAY || day == DayOfWeek.SUNDAY) {
            return false;
        }
        LocalTime time = t.toLocalTime();
        return !time.isBefore(LocalTime.of(9, 0)) && time.isBefore(LocalTime.of(17, 0));
        //@END
    }

    public static long minutesBetween(ZonedDateTime a, ZonedDateTime b) {
        //@TODO minutesBetween | elapsed minutes from a to b using Duration.between (so DST changes are respected)
        return Duration.between(a, b).toMinutes();
        //@END
    }

    public static ZonedDateTime plusWeeksWallClock(ZonedDateTime start, int weeks) {
        //@TODO plusWeeksWallClock | add weeks keeping the local wall-clock time (ZonedDateTime.plusWeeks, not Duration)
        return start.plusWeeks(weeks);
        //@END
    }

    public static String formatUtc(ZonedDateTime t) {
        //@TODO formatUtc | the instant of t as an ISO-8601 UTC string (Instant#toString)
        return t.toInstant().toString();
        //@END
    }
}
'''},
            {"ZonedMeetingTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.DateTimeException;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.List;
import org.junit.jupiter.api.Test;

class ZonedMeetingTest {

    private static final ZoneId NY = ZoneId.of("America/New_York");
    private static final ZoneId KOLKATA = ZoneId.of("Asia/Kolkata");

    @Test
    void r1_convertKeepsTheInstant() {
        ZonedDateTime utc = ZonedMeeting.convert(LocalDateTime.of(2024, 5, 20, 9, 0), KOLKATA, ZoneOffset.UTC);
        assertThat(utc.toLocalDateTime()).isEqualTo(LocalDateTime.of(2024, 5, 20, 3, 30));
        assertThat(utc.getZone()).isEqualTo(ZoneOffset.UTC);
        ZonedDateTime ny = ZonedMeeting.convert(LocalDateTime.of(2024, 12, 1, 12, 0), ZoneOffset.UTC, NY);
        assertThat(ny.toLocalDateTime()).isEqualTo(LocalDateTime.of(2024, 12, 1, 7, 0));
    }

    @Test
    void r2_localTimesInRequestedOrder() {
        Instant meeting = Instant.parse("2024-05-20T12:00:00Z");
        assertThat(ZonedMeeting.localTimes(meeting, List.of("Asia/Kolkata", "America/New_York", "Europe/London")))
                .containsExactly("2024-05-20 17:30", "2024-05-20 08:00", "2024-05-20 13:00");
        assertThat(ZonedMeeting.localTimes(meeting, List.of())).isEmpty();
    }

    @Test
    void r2_unknownZoneFails() {
        Instant meeting = Instant.parse("2024-05-20T12:00:00Z");
        assertThatThrownBy(() -> ZonedMeeting.localTimes(meeting, List.of("Mars/Base")))
                .isInstanceOf(DateTimeException.class);
    }

    @Test
    void r3_workHoursInTheMeetingsOwnZone() {
        assertThat(ZonedMeeting.isDuringWorkHours(ZonedDateTime.of(2024, 5, 20, 9, 0, 0, 0, KOLKATA))).isTrue();
        assertThat(ZonedMeeting.isDuringWorkHours(ZonedDateTime.of(2024, 5, 20, 16, 59, 0, 0, KOLKATA))).isTrue();
        assertThat(ZonedMeeting.isDuringWorkHours(ZonedDateTime.of(2024, 5, 20, 17, 0, 0, 0, KOLKATA))).isFalse();
        assertThat(ZonedMeeting.isDuringWorkHours(ZonedDateTime.of(2024, 5, 20, 8, 59, 0, 0, NY))).isFalse();
        assertThat(ZonedMeeting.isDuringWorkHours(ZonedDateTime.of(2024, 5, 18, 10, 0, 0, 0, NY))).isFalse();
        assertThat(ZonedMeeting.isDuringWorkHours(ZonedDateTime.of(2024, 5, 19, 10, 0, 0, 0, NY))).isFalse();
    }

    @Test
    void r4_minutesBetweenIsElapsedTime() {
        ZonedDateTime before = ZonedDateTime.of(2024, 3, 10, 1, 30, 0, 0, NY);
        ZonedDateTime after = ZonedDateTime.of(2024, 3, 10, 3, 30, 0, 0, NY);
        assertThat(ZonedMeeting.minutesBetween(before, after)).isEqualTo(60);
        ZonedDateTime a = ZonedDateTime.of(2024, 5, 20, 9, 0, 0, 0, KOLKATA);
        ZonedDateTime b = ZonedDateTime.of(2024, 5, 20, 10, 30, 0, 0, KOLKATA);
        assertThat(ZonedMeeting.minutesBetween(a, b)).isEqualTo(90);
        assertThat(ZonedMeeting.minutesBetween(b, a)).isEqualTo(-90);
    }

    @Test
    void r5_weeklyRecurrenceKeepsLocalTimeAcrossDst() {
        ZonedDateTime start = ZonedDateTime.of(2024, 3, 4, 10, 0, 0, 0, NY);
        ZonedDateTime next = ZonedMeeting.plusWeeksWallClock(start, 1);
        assertThat(next.toLocalTime()).isEqualTo(LocalTime.of(10, 0));
        assertThat(next.getOffset()).isEqualTo(ZoneOffset.ofHours(-4));
        assertThat(next.toLocalDate()).hasToString("2024-03-11");
        assertThat(ZonedMeeting.plusWeeksWallClock(start, 0)).isEqualTo(start);
    }

    @Test
    void r6_formatUtc() {
        assertThat(ZonedMeeting.formatUtc(ZonedDateTime.of(2024, 5, 20, 9, 0, 0, 0, ZoneOffset.UTC))).isEqualTo("2024-05-20T09:00:00Z");
        assertThat(ZonedMeeting.formatUtc(ZonedDateTime.of(2024, 5, 20, 9, 0, 0, 0, KOLKATA))).isEqualTo("2024-05-20T03:30:00Z");
    }
}
'''},
            ["`LocalDateTime.atZone(zone)` interprets the wall-clock value in that zone; `withZoneSameInstant` then re-expresses the same instant.", "`ZonedDateTime.plusWeeks` is calendar arithmetic; `plus(Duration)` is elapsed arithmetic."],
            ["Zone IDs, never fixed offsets, for region-based logic", "Understands wall-clock vs elapsed arithmetic and can explain the test on DST", "No `ZoneId.systemDefault()` in logic"],
            constraints=["Use `java.time` only; do not use `ZoneId.systemDefault()` anywhere", "Do not edit the tests"],
        ),
        task(
            "path-normalize", "Path Normalize and Traversal Guard", "Stretch", "PathTools",
            "Manipulate `Path` values without touching the disk: normalize, split into segments, compute file extensions, change extensions, relativize, and - most importantly - resolve a user-provided relative path **safely** under a base directory (no `..` escape, no absolute paths).",
            [
                "`normalized(String)` returns `Path.of(text).normalize()`",
                "`segments(Path)` returns the name elements as strings (root excluded); an empty path gives an empty list",
                "`extension(Path)` returns the text after the last dot of the file name, or `\"\"` when none (hidden files like `.bashrc` and names ending with `.` have no extension)",
                "`changeExtension(file, newExt)` replaces (or adds) the extension, keeping the parent directory",
                "`relativeTo(base, target)` returns the relative path from `base` to `target`",
                "`resolveSafe(base, userPath)` returns the normalized absolute path under `base`; throws `IllegalArgumentException` if the result escapes `base` (including absolute `userPath`s and `../` tricks)",
            ],
            ["`..` that stays inside the base (allowed)", "`..` that leaves the base (rejected)", "absolute user path", "hidden files and trailing dots", "files without extension"],
            {"PathTools.java": r'''package @PKG@;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/** Pure Path logic; nothing here touches the file system. */
public final class PathTools {

    private PathTools() {
    }

    public static Path normalized(String text) {
        //@TODO normalized | Path.of(text).normalize()
        return Path.of(text).normalize();
        //@END
    }

    public static List<String> segments(Path path) {
        //@TODO segments | the name elements of the path as strings, root excluded; empty path gives an empty list
        List<String> result = new ArrayList<>();
        for (Path element : path) {
            String name = element.toString();
            if (!name.isEmpty()) {
                result.add(name);
            }
        }
        return result;
        //@END
    }

    public static String extension(Path file) {
        //@TODO extension | text after the last '.' of the file name; "" when no dot, when the dot is the first char (.bashrc), or when the name ends with '.'
        Path fileName = file.getFileName();
        if (fileName == null) {
            return "";
        }
        String name = fileName.toString();
        int dot = name.lastIndexOf('.');
        if (dot <= 0 || dot == name.length() - 1) {
            return "";
        }
        return name.substring(dot + 1);
        //@END
    }

    public static Path changeExtension(Path file, String newExtension) {
        //@TODO changeExtension | replace the extension of the file name (or append one if absent), keeping the parent; newExtension has no leading dot
        String name = file.getFileName().toString();
        String ext = extension(file);
        String stem = ext.isEmpty() ? name : name.substring(0, name.length() - ext.length() - 1);
        if (name.endsWith(".") && ext.isEmpty()) {
            stem = name.substring(0, name.length() - 1);
        }
        return file.resolveSibling(stem + "." + newExtension);
        //@END
    }

    public static Path relativeTo(Path base, Path target) {
        //@TODO relativeTo | base.relativize(target)
        return base.relativize(target);
        //@END
    }

    public static Path resolveSafe(Path base, String userPath) {
        //@TODO resolveSafe | normalize the absolute base, resolve userPath, normalize; throw IllegalArgumentException when the result does not start with the base (absolute userPath or .. escape)
        Path root = base.toAbsolutePath().normalize();
        Path resolved = root.resolve(userPath).normalize();
        if (!resolved.startsWith(root)) {
            throw new IllegalArgumentException("path escapes base directory: " + userPath);
        }
        return resolved;
        //@END
    }
}
'''},
            {"PathToolsTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.nio.file.Path;
import org.junit.jupiter.api.Test;

class PathToolsTest {

    @Test
    void r1_normalized() {
        assertThat(PathTools.normalized("a/./b/../c/file.txt")).isEqualTo(Path.of("a", "c", "file.txt"));
        assertThat(PathTools.normalized("../x")).isEqualTo(Path.of("..", "x"));
    }

    @Test
    void r2_segments() {
        assertThat(PathTools.segments(Path.of("a", "b", "c.txt"))).containsExactly("a", "b", "c.txt");
        assertThat(PathTools.segments(Path.of(""))).isEmpty();
        assertThat(PathTools.segments(Path.of("single"))).containsExactly("single");
    }

    @Test
    void r3_extension() {
        assertThat(PathTools.extension(Path.of("dir", "report.final.pdf"))).isEqualTo("pdf");
        assertThat(PathTools.extension(Path.of("README"))).isEmpty();
        assertThat(PathTools.extension(Path.of(".bashrc"))).isEmpty();
        assertThat(PathTools.extension(Path.of("odd."))).isEmpty();
        assertThat(PathTools.extension(Path.of("a.tar.gz"))).isEqualTo("gz");
    }

    @Test
    void r4_changeExtension() {
        assertThat(PathTools.changeExtension(Path.of("a", "b", "report.txt"), "md")).isEqualTo(Path.of("a", "b", "report.md"));
        assertThat(PathTools.changeExtension(Path.of("notes"), "txt")).isEqualTo(Path.of("notes.txt"));
        assertThat(PathTools.changeExtension(Path.of("x", "archive.tar.gz"), "zip")).isEqualTo(Path.of("x", "archive.tar.zip"));
        assertThat(PathTools.changeExtension(Path.of("odd."), "txt")).isEqualTo(Path.of("odd.txt"));
    }

    @Test
    void r5_relativeTo() {
        Path base = Path.of("srv", "data");
        Path target = Path.of("srv", "data", "reports", "q1.txt");
        assertThat(PathTools.relativeTo(base, target)).isEqualTo(Path.of("reports", "q1.txt"));
        assertThat(PathTools.relativeTo(target, base)).isEqualTo(Path.of("..", ".."));
    }

    @Test
    void r6_resolveSafeAllowsInsidePaths() {
        Path base = Path.of("srv", "data");
        Path expectedRoot = base.toAbsolutePath().normalize();
        assertThat(PathTools.resolveSafe(base, "reports/q1.txt")).isEqualTo(expectedRoot.resolve("reports").resolve("q1.txt"));
        assertThat(PathTools.resolveSafe(base, "a/../b.txt")).isEqualTo(expectedRoot.resolve("b.txt"));
        assertThat(PathTools.resolveSafe(base, ".")).isEqualTo(expectedRoot);
    }

    @Test
    void r6_resolveSafeRejectsEscapes() {
        Path base = Path.of("srv", "data");
        assertThatThrownBy(() -> PathTools.resolveSafe(base, "../secret.txt")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> PathTools.resolveSafe(base, "a/../../secret.txt")).isInstanceOf(IllegalArgumentException.class);
        Path absolute = Path.of("srv").toAbsolutePath().getRoot().resolve("etc").resolve("passwd");
        assertThatThrownBy(() -> PathTools.resolveSafe(base, absolute.toString())).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r6_siblingDirectoryWithSharedPrefixIsRejected() {
        Path base = Path.of("srv", "data");
        assertThatThrownBy(() -> PathTools.resolveSafe(base, "../data-private/x.txt")).isInstanceOf(IllegalArgumentException.class);
    }
}
'''},
            ["`Path.startsWith(Path)` compares whole name elements (so `/srv/data-private` does not start with `/srv/data`) - do not convert to strings.", "`resolve` with an absolute argument returns the argument: the `startsWith` check after `normalize()` catches it."],
            ["`Path` API used instead of string concatenation", "`resolveSafe` normalizes before the `startsWith` check", "No file system access in this class"],
            constraints=["Use `java.nio.file.Path`; do not use `java.io.File` or `String.startsWith` for the traversal check", "Do not edit the tests"],
        ),
        task(
            "files-read-write", "Files Read/Write Lab", "Challenge", "FilesLab",
            "Do real file I/O with NIO.2 in a JUnit `@TempDir`: write UTF-8 lines (creating parent folders), read them back, append, count lines lazily with a closed stream, list text files in a directory, copy with replacement, and delete if present. IO failures are wrapped in `UncheckedIOException`.",
            [
                "`writeLines(file, lines)` creates missing parent directories and writes UTF-8 lines, replacing existing content",
                "`readLines(file)` returns all lines decoded as UTF-8; a missing file throws `UncheckedIOException` caused by `NoSuchFileException`",
                "`appendLine(file, line)` appends one line (creating the file when absent) without touching earlier content",
                "`countLines(file)` counts lines using `Files.lines` inside try-with-resources",
                "`listTextFiles(dir)` returns the regular `.txt` files directly inside `dir` (not recursive), sorted by file name; closes the directory stream",
                "`copyReplacing(src, dst)` copies the file, replacing an existing target",
                "`deleteIfPresent(file)` deletes the file and returns whether something was deleted",
            ],
            ["non-ASCII text", "missing source file", "parent directories not yet created", "empty file", "sub-directories and non-.txt files are ignored by `listTextFiles`"],
            {"FilesLab.java": r'''package @PKG@;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.nio.file.StandardOpenOption;
import java.util.List;
import java.util.stream.Stream;

/** NIO.2 file helpers; IOExceptions are rethrown as UncheckedIOException. */
public final class FilesLab {

    private FilesLab() {
    }

    public static void writeLines(Path file, List<String> lines) {
        //@TODO writeLines | create parent directories if needed, then Files.write(file, lines, UTF_8) replacing existing content; wrap IOException in UncheckedIOException
        try {
            Path parent = file.toAbsolutePath().getParent();
            if (parent != null) {
                Files.createDirectories(parent);
            }
            Files.write(file, lines, StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        //@END
    }

    public static List<String> readLines(Path file) {
        //@TODO readLines | Files.readAllLines(file, UTF_8); wrap IOException (e.g. NoSuchFileException) in UncheckedIOException
        try {
            return Files.readAllLines(file, StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        //@END
    }

    public static void appendLine(Path file, String line) {
        //@TODO appendLine | append line + System.lineSeparator() with CREATE and APPEND options in UTF-8; wrap IOException
        try {
            Files.writeString(file, line + System.lineSeparator(), StandardCharsets.UTF_8,
                    StandardOpenOption.CREATE, StandardOpenOption.APPEND);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        //@END
    }

    public static long countLines(Path file) {
        //@TODO countLines | count lines with Files.lines(file, UTF_8) in try-with-resources; wrap IOException
        try (Stream<String> lines = Files.lines(file, StandardCharsets.UTF_8)) {
            return lines.count();
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        //@END
    }

    public static List<Path> listTextFiles(Path dir) {
        //@TODO listTextFiles | regular files directly in dir whose name ends with .txt, sorted by file name; use try-with-resources around Files.list; wrap IOException
        try (Stream<Path> entries = Files.list(dir)) {
            return entries
                    .filter(Files::isRegularFile)
                    .filter(p -> p.getFileName().toString().endsWith(".txt"))
                    .sorted()
                    .toList();
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        //@END
    }

    public static void copyReplacing(Path src, Path dst) {
        //@TODO copyReplacing | Files.copy(src, dst, REPLACE_EXISTING); wrap IOException
        try {
            Files.copy(src, dst, StandardCopyOption.REPLACE_EXISTING);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        //@END
    }

    public static boolean deleteIfPresent(Path file) {
        //@TODO deleteIfPresent | Files.deleteIfExists(file) and return its result; wrap IOException
        try {
            return Files.deleteIfExists(file);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        //@END
    }
}
'''},
            {"FilesLabTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.NoSuchFileException;
import java.nio.file.Path;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class FilesLabTest {

    @TempDir
    Path tmp;

    @Test
    void r1_writeCreatesParentsAndReplacesContent() throws Exception {
        Path file = tmp.resolve("nested").resolve("deeper").resolve("a.txt");
        FilesLab.writeLines(file, List.of("one", "two"));
        assertThat(Files.readAllLines(file)).containsExactly("one", "two");
        FilesLab.writeLines(file, List.of("only"));
        assertThat(Files.readAllLines(file)).containsExactly("only");
    }

    @Test
    void r2_readUsesUtf8() throws Exception {
        Path file = tmp.resolve("utf8.txt");
        Files.writeString(file, "héllo ✓\nwörld\n");
        assertThat(FilesLab.readLines(file)).containsExactly("héllo ✓", "wörld");
        Path empty = tmp.resolve("empty.txt");
        Files.createFile(empty);
        assertThat(FilesLab.readLines(empty)).isEmpty();
    }

    @Test
    void r2_missingFileBecomesUncheckedIoException() {
        Path missing = tmp.resolve("missing.txt");
        assertThatThrownBy(() -> FilesLab.readLines(missing))
                .isInstanceOf(UncheckedIOException.class)
                .hasCauseInstanceOf(NoSuchFileException.class);
    }

    @Test
    void r3_appendCreatesAndKeepsEarlierLines() {
        Path file = tmp.resolve("log.txt");
        FilesLab.appendLine(file, "first");
        FilesLab.appendLine(file, "second");
        assertThat(FilesLab.readLines(file)).containsExactly("first", "second");
    }

    @Test
    void r4_countLines() throws Exception {
        Path file = tmp.resolve("count.txt");
        Files.write(file, List.of("a", "b", "c"));
        assertThat(FilesLab.countLines(file)).isEqualTo(3);
        Path empty = tmp.resolve("e.txt");
        Files.createFile(empty);
        assertThat(FilesLab.countLines(empty)).isZero();
        assertThatThrownBy(() -> FilesLab.countLines(tmp.resolve("nope.txt"))).isInstanceOf(UncheckedIOException.class);
    }

    @Test
    void r5_listTextFilesIsSortedFlatAndFiltered() throws Exception {
        Files.writeString(tmp.resolve("b.txt"), "b");
        Files.writeString(tmp.resolve("a.txt"), "a");
        Files.writeString(tmp.resolve("c.md"), "c");
        Files.createDirectory(tmp.resolve("sub.txt"));
        Files.writeString(Files.createDirectory(tmp.resolve("inner")).resolve("z.txt"), "z");
        assertThat(FilesLab.listTextFiles(tmp)).extracting(p -> p.getFileName().toString()).containsExactly("a.txt", "b.txt");
        Path emptyDir = Files.createDirectory(tmp.resolve("empty-dir"));
        assertThat(FilesLab.listTextFiles(emptyDir)).isEmpty();
    }

    @Test
    void r6_copyReplacesExistingTarget() throws Exception {
        Path src = tmp.resolve("src.txt");
        Path dst = tmp.resolve("dst.txt");
        Files.writeString(src, "new");
        Files.writeString(dst, "old");
        FilesLab.copyReplacing(src, dst);
        assertThat(Files.readString(dst)).isEqualTo("new");
        assertThat(Files.exists(src)).isTrue();
        assertThatThrownBy(() -> FilesLab.copyReplacing(tmp.resolve("missing"), dst)).isInstanceOf(UncheckedIOException.class);
    }

    @Test
    void r7_deleteIfPresent() throws Exception {
        Path file = tmp.resolve("gone.txt");
        Files.writeString(file, "x");
        assertThat(FilesLab.deleteIfPresent(file)).isTrue();
        assertThat(Files.exists(file)).isFalse();
        assertThat(FilesLab.deleteIfPresent(file)).isFalse();
    }
}
'''},
            ["`Files.createDirectories` is idempotent - no need to check if the directory exists.", "A `Stream` from `Files.list`/`Files.lines` is a resource: put it in the try-with-resources header."],
            ["Every stream-returning `Files` call is closed", "Explicit UTF-8 everywhere", "`UncheckedIOException` wraps the original cause (not just its message)"],
            constraints=["Use NIO.2 (`Path`/`Files`) only - no `java.io.File`, `FileReader`, or `FileWriter`", "Always specify UTF-8 explicitly", "Do not edit the tests"],
        ),
    ],
)
