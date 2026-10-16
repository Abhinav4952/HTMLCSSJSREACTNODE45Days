# Task 4 — Files Read/Write Lab

**Day:** 19 · **Task ID:** Day19-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Do real file I/O with NIO.2 in a JUnit `@TempDir`: write UTF-8 lines (creating parent folders), read them back, append, count lines lazily with a closed stream, list text files in a directory, copy with replacement, and delete if present. IO failures are wrapped in `UncheckedIOException`.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day19/task04/FilesLab.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day19/task04/FilesLabTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 19 theory file read

## What you will implement

1. `writeLines(file, lines)` creates missing parent directories and writes UTF-8 lines, replacing existing content
2. `readLines(file)` returns all lines decoded as UTF-8; a missing file throws `UncheckedIOException` caused by `NoSuchFileException`
3. `appendLine(file, line)` appends one line (creating the file when absent) without touching earlier content
4. `countLines(file)` counts lines using `Files.lines` inside try-with-resources
5. `listTextFiles(dir)` returns the regular `.txt` files directly inside `dir` (not recursive), sorted by file name; closes the directory stream
6. `copyReplacing(src, dst)` copies the file, replacing an existing target
7. `deleteIfPresent(file)` deletes the file and returns whether something was deleted

## Constraints

- Use NIO.2 (`Path`/`Files`) only - no `java.io.File`, `FileReader`, or `FileWriter`
- Always specify UTF-8 explicitly
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=FilesLabTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **8 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day19-task04)`).

### Run one test class

```bash
mvn -Dtest=FilesLabTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `FilesLab.java` — `writeLines` | `TODO(Day19-task04)` | create parent directories if needed, then Files.write(file, lines, UTF_8) replacing existing content; wrap IOException in UncheckedIOException |
| `FilesLab.java` — `readLines` | `TODO(Day19-task04)` | Files.readAllLines(file, UTF_8); wrap IOException (e.g. NoSuchFileException) in UncheckedIOException |
| `FilesLab.java` — `appendLine` | `TODO(Day19-task04)` | append line + System.lineSeparator() with CREATE and APPEND options in UTF-8; wrap IOException |
| `FilesLab.java` — `countLines` | `TODO(Day19-task04)` | count lines with Files.lines(file, UTF_8) in try-with-resources; wrap IOException |
| `FilesLab.java` — `listTextFiles` | `TODO(Day19-task04)` | regular files directly in dir whose name ends with .txt, sorted by file name; use try-with-resources around Files.list; wrap IOException |
| `FilesLab.java` — `copyReplacing` | `TODO(Day19-task04)` | Files.copy(src, dst, REPLACE_EXISTING); wrap IOException |
| `FilesLab.java` — `deleteIfPresent` | `TODO(Day19-task04)` | Files.deleteIfExists(file) and return its result; wrap IOException |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_writeCreatesParentsAndReplacesContent` |
| 2 | `r2_readUsesUtf8`, `r2_missingFileBecomesUncheckedIoException` |
| 3 | `r3_appendCreatesAndKeepsEarlierLines` |
| 4 | `r4_countLines` |
| 5 | `r5_listTextFilesIsSortedFlatAndFiltered` |
| 6 | `r6_copyReplacesExistingTarget` |
| 7 | `r7_deleteIfPresent` |

## Edge cases to handle

- non-ASCII text
- missing source file
- parent directories not yet created
- empty file
- sub-directories and non-.txt files are ignored by `listTextFiles`

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 19: Files Read/Write Lab`

## Hints (optional)

<details><summary>Hint 1</summary>

`Files.createDirectories` is idempotent - no need to check if the directory exists.

</details>

<details><summary>Hint 2</summary>

A `Stream` from `Files.list`/`Files.lines` is a resource: put it in the try-with-resources header.

</details>
