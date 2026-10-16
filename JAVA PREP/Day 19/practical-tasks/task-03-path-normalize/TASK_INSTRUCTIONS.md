# Task 3 — Path Normalize and Traversal Guard

**Day:** 19 · **Task ID:** Day19-task03 · **Type:** Plain Java · **Difficulty:** Stretch

## Summary

Manipulate `Path` values without touching the disk: normalize, split into segments, compute file extensions, change extensions, relativize, and - most importantly - resolve a user-provided relative path **safely** under a base directory (no `..` escape, no absolute paths).

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day19/task03/PathTools.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day19/task03/PathToolsTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 19 theory file read

## What you will implement

1. `normalized(String)` returns `Path.of(text).normalize()`
2. `segments(Path)` returns the name elements as strings (root excluded); an empty path gives an empty list
3. `extension(Path)` returns the text after the last dot of the file name, or `""` when none (hidden files like `.bashrc` and names ending with `.` have no extension)
4. `changeExtension(file, newExt)` replaces (or adds) the extension, keeping the parent directory
5. `relativeTo(base, target)` returns the relative path from `base` to `target`
6. `resolveSafe(base, userPath)` returns the normalized absolute path under `base`; throws `IllegalArgumentException` if the result escapes `base` (including absolute `userPath`s and `../` tricks)

## Constraints

- Use `java.nio.file.Path`; do not use `java.io.File` or `String.startsWith` for the traversal check
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=PathToolsTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **8 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day19-task03)`).

### Run one test class

```bash
mvn -Dtest=PathToolsTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `PathTools.java` — `normalized` | `TODO(Day19-task03)` | Path.of(text).normalize() |
| `PathTools.java` — `segments` | `TODO(Day19-task03)` | the name elements of the path as strings, root excluded; empty path gives an empty list |
| `PathTools.java` — `extension` | `TODO(Day19-task03)` | text after the last '.' of the file name; "" when no dot, when the dot is the first char (.bashrc), or when the name ends with '.' |
| `PathTools.java` — `changeExtension` | `TODO(Day19-task03)` | replace the extension of the file name (or append one if absent), keeping the parent; newExtension has no leading dot |
| `PathTools.java` — `relativeTo` | `TODO(Day19-task03)` | base.relativize(target) |
| `PathTools.java` — `resolveSafe` | `TODO(Day19-task03)` | normalize the absolute base, resolve userPath, normalize; throw IllegalArgumentException when the result does not start with the base (absolute userPath or .. escape) |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_normalized` |
| 2 | `r2_segments` |
| 3 | `r3_extension` |
| 4 | `r4_changeExtension` |
| 5 | `r5_relativeTo` |
| 6 | `r6_resolveSafeAllowsInsidePaths`, `r6_resolveSafeRejectsEscapes`, `r6_siblingDirectoryWithSharedPrefixIsRejected` |

## Edge cases to handle

- `..` that stays inside the base (allowed)
- `..` that leaves the base (rejected)
- absolute user path
- hidden files and trailing dots
- files without extension

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 19: Path Normalize and Traversal Guard`

## Hints (optional)

<details><summary>Hint 1</summary>

`Path.startsWith(Path)` compares whole name elements (so `/srv/data-private` does not start with `/srv/data`) - do not convert to strings.

</details>

<details><summary>Hint 2</summary>

`resolve` with an absolute argument returns the argument: the `startsWith` check after `normalize()` catches it.

</details>
