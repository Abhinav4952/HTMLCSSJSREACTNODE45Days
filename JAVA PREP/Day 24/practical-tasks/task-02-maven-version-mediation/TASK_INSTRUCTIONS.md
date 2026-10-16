# Task 2 — Maven Versions, Ranges, and Dependency Mediation

**Day:** 24 · **Task ID:** Day24-task02 · **Type:** Plain Java · **Difficulty:** Core

## Summary

Implement Maven's version ordering (`1.9 < 1.10`, `1.0-alpha < 1.0-rc1 < 1.0-SNAPSHOT < 1.0`), version ranges (`[1.0,2.0)`), and the **nearest-wins** mediation rule used when two dependency paths disagree - the logic behind most 'works locally, `NoSuchMethodError` in prod' incidents.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day24/task02/MavenVersion.java` | Stubs with TODOs |
| `src/main/java/com/javaprep/day24/task02/VersionRange.java` | Stubs with TODOs |
| `src/main/java/com/javaprep/day24/task02/DependencyMediation.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day24/task02/MavenVersionTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 24 theory file read

## What you will implement

1. `MavenVersion.parse(text)` accepts `N(.N)*` optionally followed by `-qualifier` where the qualifier is `alpha|beta|milestone|rc|cr|snapshot|ga|final` (case-insensitive) with an optional number (`rc1`, `rc.2`, `beta-3`); otherwise `IllegalArgumentException` (also for null/blank)
2. `MavenVersion` implements `Comparable`: numeric components compare numerically with missing components treated as 0 (`1.0 == 1.0.0`), then qualifiers by rank `alpha < beta < milestone < rc(=cr) < snapshot < release(none/ga/final)`, then the qualifier number; `equals`/`hashCode` are consistent with `compareTo`
3. `VersionRange.parse(spec)` supports `[a,b]`, `[a,b)`, `(a,b]`, `(a,b)`, `[a,)`, `(,b]` and the exact form `[a]`; anything else (plain `1.0`, empty bounds on both sides, lower > upper) -> `IllegalArgumentException`; `contains(version)` honours inclusive/exclusive bounds
4. `DependencyMediation.resolve(declarations)` picks, for every `groupId:artifactId`, the declaration with the **smallest depth** (ties: first declared) and returns `artifact -> version` in order of first appearance
5. `DependencyMediation.highest(versions)` returns the highest version string (by `MavenVersion` ordering; empty -> `IllegalArgumentException`) and `satisfying(range, versions)` returns the matching version strings sorted ascending

## Constraints

- No Maven libraries (`maven-artifact`, etc.) - implement the rules yourself
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=MavenVersionTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **12 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day24-task02)`).

### Run one test class

```bash
mvn -Dtest=MavenVersionTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `MavenVersion.java` — `parse` | `TODO(Day24-task02)` | null/blank/non-matching -> IllegalArgumentException; split numeric parts (strip trailing zero components), qualifier rank (alpha 0, beta 1, milestone 2, rc/cr 3, snapshot 4, none/ga/final 5) and qualifier number (default 0) |
| `MavenVersion.java` — `compareTo` | `TODO(Day24-task02)` | compare numeric components pairwise (missing = 0), then rank, then qualifierNumber |
| `VersionRange.java` — `parse` | `TODO(Day24-task02)` | null/short/no brackets -> IllegalArgumentException; strip the brackets; no comma means exact [a] (both brackets must be square); otherwise exactly two parts split on the comma, blank part = unbounded, both blank -> IAE, lower > upper -> IAE; remember inclusive ('[' / ']') vs exclusive ('(' / ')') |
| `VersionRange.java` — `contains` | `TODO(Day24-task02)` | lower bound (when present): version >= lower if inclusive else > lower; upper bound (when present): version <= upper if inclusive else < upper |
| `DependencyMediation.java` — `resolve` | `TODO(Day24-task02)` | for every artifact keep the declaration with the smallest depth (the first one wins ties); the result is a LinkedHashMap artifact -> version ordered by first appearance |
| `DependencyMediation.java` — `highest` | `TODO(Day24-task02)` | empty list -> IllegalArgumentException; return the original string of the greatest MavenVersion |
| `DependencyMediation.java` — `satisfying` | `TODO(Day24-task02)` | keep versions for which range.contains(MavenVersion.parse(v)) and return them sorted ascending by MavenVersion |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_parsesValidVersions`, `r1_rejectsInvalidVersions`, `r1_nullIsRejected` |
| 2 | `r2_equalVersionsCompareEqualAndShareHashCodes`, `r2_sortingARealisticList` |
| 3 | `r3_rejectsMalformedRanges`, `r3_nullRangeIsRejected` |
| 4 | `r4_nearestWins`, `r4_firstDeclaredWinsOnTies`, `r4_directDeclarationBeatsEverything` |
| 5 | `r5_highestUsesVersionOrderingNotTextOrdering`, `r5_satisfyingFiltersAndSorts` |

## Edge cases to handle

- `1.10` vs `1.9`
- `1.0` vs `1.0.0`
- SNAPSHOT vs release vs rc
- unbounded ranges
- ties on depth

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 24: Maven Versions, Ranges, and Dependency Mediation`

## Hints (optional)

<details><summary>Hint 1</summary>

Normalize on parse (strip trailing zero components) so `equals`/`hashCode` can rely on the stored list.

</details>

<details><summary>Hint 2</summary>

Qualifier **rank** decides first, the qualifier **number** only breaks ties between the same qualifier (`rc1 < rc2`).

</details>

<details><summary>Hint 3</summary>

`Map.merge` with a pick-the-nearest function is a compact way to implement mediation while keeping first-seen order in a `LinkedHashMap`.

</details>
