# Task 1 — Maven Lifecycle Planner and POM Reader

**Day:** 24 · **Task ID:** Day24-task01 · **Type:** Plain Java · **Difficulty:** Warm-up

## Summary

Model Maven in code: compute which phases run for a command line (`mvn clean package`), look up the plugin goal bound to a phase for `jar`/`war`/`pom` packaging, parse the `<dependencies>` of a POM (resolving `${property}` versions and default `compile` scope), and decide which dependencies are on the compile, runtime, and test classpaths.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day24/task01/MavenLifecycle.java` | Stubs with TODOs |
| `src/main/java/com/javaprep/day24/task01/PomReader.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day24/task01/MavenLifecycleTest.java` | Specification tests (read-only) |
| `src/test/java/com/javaprep/day24/task01/PomReaderTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 24 theory file read

## What you will implement

1. `MavenLifecycle.phasesUpTo(phase)` returns the lifecycle phases up to and including the named one, for the clean (`pre-clean`, `clean`, `post-clean`), default (23 phases), and site (`pre-site`, `site`, `post-site`, `site-deploy`) lifecycles; unknown/blank -> `IllegalArgumentException`
2. `MavenLifecycle.plan(phases...)` concatenates `phasesUpTo` for each requested phase **without duplicates** keeping first-seen order (`plan("clean", "package")` = clean lifecycle up to clean + default up to package); no arguments -> `IllegalArgumentException`
3. `MavenLifecycle.boundGoal(packaging, phase)` returns the default plugin goal for `jar`, `war` (`package` -> `war:war`), or `pom` (only `install` and `deploy`) packaging in the default lifecycle; phases without a binding -> empty; unknown packaging or non-default phase -> `IllegalArgumentException`
4. `PomReader.dependencies(xml)` returns the project's direct `<dependencies>` (not those inside `<dependencyManagement>`) with `${property}` references resolved from `<properties>` (and `project.version`); scope defaults to `compile`; a missing version is `null`; malformed XML or DOCTYPE declarations -> `IllegalArgumentException`
5. `PomReader.onClasspath(scope, kind)` implements the scope table and `PomReader.classpath(deps, kind)` returns `groupId:artifactId:version` strings in declaration order for the dependencies on that classpath

## Constraints

- Use the JDK's `javax.xml` DOM API only; no third-party XML or Maven libraries
- Do not edit the tests or the provided helper methods in `PomReader`
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=MavenLifecycleTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **21 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day24-task01)`).

### Run one test class

```bash
mvn -Dtest=MavenLifecycleTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `MavenLifecycle.java` — `phasesUpTo` | `TODO(Day24-task01)` | null/blank/unknown -> IllegalArgumentException; find the lifecycle (CLEAN, DEFAULT, SITE) containing the phase and return a copy of its phases from the start up to and including it |
| `MavenLifecycle.java` — `plan` | `TODO(Day24-task01)` | no arguments -> IllegalArgumentException; for each requested phase add phasesUpTo(phase) to a LinkedHashSet (keeps order, drops duplicates); return it as a List |
| `MavenLifecycle.java` — `boundGoal` | `TODO(Day24-task01)` | packaging must be jar, war or pom and phase must be in DEFAULT (else IllegalArgumentException); pom binds only install:install and deploy:deploy; jar/war bind process-resources=resources:resources, compile=compiler:compile, process-test-resources=resources:testResources, test-compile=compiler:testCompile, test=surefire:test, package=jar:jar (war:war for war), install=install:install, deploy=deploy:deploy; everything else Optional.empty() |
| `PomReader.java` — `dependencies` | `TODO(Day24-task01)` | parse with a DocumentBuilderFactory that disallows DOCTYPE (feature http://apache.org/xml/features/disallow-doctype-decl) and wrap parser errors in IllegalArgumentException; collect <properties> children plus project.version; read ONLY project/dependencies/dependency (direct children) with groupId, artifactId, version (resolve ${...} via properties, unresolved stays as is, missing -> null) and scope (default compile) |
| `PomReader.java` — `onClasspath` | `TODO(Day24-task01)` | compile: all three kinds; provided and system: COMPILE and TEST; runtime: RUNTIME and TEST; test: TEST only; null/unknown scope -> IllegalArgumentException |
| `PomReader.java` — `classpath` | `TODO(Day24-task01)` | keep the dependencies for which onClasspath(scope, kind) is true and return their coordinates() in declaration order |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_defaultLifecycleHasTwentyThreePhasesInOrder`, `r1_phasesUpToCompile`, `r1_phasesUpToTestIncludesTestCompileButNotPackage`, `r1_otherLifecycles`, `r1_returnedListsAreIndependentCopies`, `r1_unknownPhasesAreRejected`, `r1_nullPhaseIsRejected` |
| 2 | `r2_cleanPackagePlan`, `r2_overlappingPhasesAreNotRepeated`, `r2_orderFollowsTheCommandLine`, `r2_planNeedsAtLeastOnePhase` |
| 3 | `r3_phasesWithoutBindingsAreEmpty`, `r3_warAndPomPackaging`, `r3_invalidArguments` |
| 4 | `r4_readsOnlyDirectDependenciesInOrder`, `r4_resolvesPropertiesAndDefaultsTheScope`, `r4_exclusionsAndManagedDependenciesDoNotLeak`, `r4_pomWithoutDependenciesIsEmpty`, `r4_malformedAndHostileXmlIsRejected` |
| 5 | `r5_unknownScopeIsRejected`, `r5_classpathsForThePom` |

## Edge cases to handle

- unknown phase names
- dependencies inside `dependencyManagement` and `exclusions` must not leak into the result
- unresolvable `${property}` stays literally as written
- DOCTYPE/external entities must be rejected (XXE)

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 24: Maven Lifecycle Planner and POM Reader`

## Hints (optional)

<details><summary>Hint 1</summary>

Keep the three lifecycle lists as the single source of truth; `phasesUpTo` is just `subList(0, index + 1)` on the list that contains the phase.

</details>

<details><summary>Hint 2</summary>

Walk the DOM with a helper that returns only **direct** children named X; `getElementsByTagName` would also find dependencies inside `dependencyManagement` and `exclusions`.

</details>

<details><summary>Hint 3</summary>

`Matcher.appendReplacement` needs `Matcher.quoteReplacement` when the value contains `$` or `\`.

</details>

<details><summary>Hint 4</summary>

Disable DOCTYPE processing to block XXE; the provided `parse` helper already does it.

</details>
