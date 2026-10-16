# Task 3 — Class Loader Lab

**Day:** 22 · **Task ID:** Day22-task03 · **Type:** Plain Java · **Difficulty:** Stretch

## Summary

Explore class loading by building an `IsolatedLoader` that defines classes from raw bytes with **child-first** behaviour for the classes you register while still delegating everything else to its parent. Prove class identity rules: two loaders produce two `Class` objects with separate static state, and instances are not assignable across them.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day22/task03/SamplePlugin.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day22/task03/ClassLoaderLab.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day22/task03/ClassLoaderLabTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 22 theory file read

## What you will implement

1. `bytesOf(type)` reads the `.class` bytes of a loaded class from its resource (`/pkg/Name.class`); a missing resource -> `IllegalArgumentException`
2. `IsolatedLoader(parent, classes)` defines each registered class name **itself** (child-first, once per loader, synchronized on the class-loading lock) and delegates every other name to the parent
3. `loaderName(type)` returns `bootstrap` when the class loader is `null`, the loader's name when it has one (`app`, `platform`), otherwise the loader's simple class name
4. `loaderChain(loader)` lists loader names from the given loader up to and including `bootstrap`
5. `instantiate(type)` creates an instance via the public no-arg constructor, wrapping reflective failures in `IllegalStateException` with the cause

## Constraints

- Extend `ClassLoader` only - no `URLClassLoader`, no third-party bytecode libraries
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=ClassLoaderLabTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **8 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day22-task03)`).

### Run one test class

```bash
mvn -Dtest=ClassLoaderLabTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `ClassLoaderLab.java` — `loadClass` | `TODO(Day22-task03)` | synchronized (getClassLoadingLock(name)): when name is registered use findLoadedClass or defineClass(name, bytes, 0, length) (child-first); otherwise return super.loadClass(name, resolve) |
| `ClassLoaderLab.java` — `bytesOf` | `TODO(Day22-task03)` | type.getResourceAsStream("/" + name with dots replaced by slashes + ".class"); null stream -> IllegalArgumentException; read all bytes, wrap IOException in UncheckedIOException |
| `ClassLoaderLab.java` — `loaderName` | `TODO(Day22-task03)` | getClassLoader() == null -> "bootstrap"; loader.getName() when not null; else the loader's getClass().getSimpleName() |
| `ClassLoaderLab.java` — `loaderChain` | `TODO(Day22-task03)` | walk getParent() from the given loader collecting a name per loader (same naming rule as loaderName), then append "bootstrap" |
| `ClassLoaderLab.java` — `instantiate` | `TODO(Day22-task03)` | type.getDeclaredConstructor().newInstance(); wrap ReflectiveOperationException in IllegalStateException keeping the cause |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_bytesOfReturnsClassFileWithMagicNumber` |
| 2 | `r2_registeredClassIsDefinedByTheIsolatedLoader`, `r2_otherClassesAreDelegatedToTheParent`, `r2_sameBytesInTwoLoadersAreUnrelatedTypesWithSeparateStatics` |
| 3 | `r3_loaderNames`, `r3_loaderNameOfAnIsolatedClass` |
| 4 | `r4_loaderChainEndsAtBootstrap` |
| 5 | `r5_instantiateWrapsFailures` |

## Edge cases to handle

- unknown class names throw `ClassNotFoundException`
- java.* classes must still come from the parent
- loading the same name twice in one loader returns the same `Class`
- classes without a registered name delegate to the parent (same `Class` as the app loader)

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 22: Class Loader Lab`

## Hints (optional)

<details><summary>Hint 1</summary>

Override `loadClass(String, boolean)`, not `loadClass(String)`: the one-argument version just calls it.

</details>

<details><summary>Hint 2</summary>

`defineClass` can only be called once per name per loader - check `findLoadedClass` first (inside the class-loading lock).

</details>

<details><summary>Hint 3</summary>

A class whose `getClassLoader()` is `null` came from the bootstrap loader.

</details>
