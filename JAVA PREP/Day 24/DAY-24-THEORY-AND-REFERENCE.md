# Day 24 — Maven Lifecycle, Scopes & Plugins; Pattern Matching Recap; Core Java Review Challenge

**Phase:** Core Java  
**Primary theme:** Understand what `mvn` really does (lifecycle, scopes, mediation, plugins), consolidate modern Java pattern matching with sealed types and records, and prove your Core Java skills in a capstone challenge.  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-maven-lifecycle-and-scopes`, `task-02-maven-version-mediation`, `task-03-pattern-matching-expressions`, `task-04-core-java-inventory-challenge`  
**Instruction alignment:** Maps to the Day 24 entry of the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21 (no Spring today)

## Overview

Core Java ends today with three consolidating themes.

**Build tool literacy.** Every Day 13-23 task is a Maven project; you typed `mvn test` dozens of times. Today you learn *why* it works: Maven is a **plugin execution framework** driven by **lifecycles** made of ordered **phases**. Running `mvn package` does not "run package" - it runs every phase from `validate` up to `package`, and each phase executes the **plugin goals bound to it** (e.g. `compile` -> `maven-compiler-plugin:compile`, `test` -> `maven-surefire-plugin:test`, `package` -> `maven-jar-plugin:jar`). Dependencies are resolved **transitively** with **nearest-wins mediation**, filtered by **scope** (what lands on the compile, runtime, and test classpaths). Most "works on my machine" and "NoSuchMethodError in production" incidents are dependency-resolution problems, and `mvn dependency:tree` is the tool you reach for.

**Pattern matching recap.** Java 21 completes a decade-long push towards *data-oriented programming*: `instanceof` with binding variables (16), `record` types (16), `sealed` hierarchies (17), **pattern matching for `switch`** with guards and `case null` (21), and **record deconstruction patterns** (21). Together they let the compiler check that a switch over a sealed hierarchy is *exhaustive* - add a new subtype and every non-exhaustive switch stops compiling.

**Core Java review challenge.** Task 4 asks you to build a small inventory report: parse CSV safely (no exception-driven control flow), model results with sealed types and records, aggregate with streams and collectors, build an LRU cache from `LinkedHashMap`, and add up values in parallel on virtual threads. Interviewers frequently ask: *Maven lifecycle phases in order*, *scope `provided` vs `runtime`*, *how does Maven pick a version when two paths disagree*, *what is a BOM*, *what is exhaustiveness checking*, *when do you use a record*, plus a live coding exercise combining collections and streams.

## Day roadmap

1. Maven lifecycle, phases, goals, and plugins
2. Dependencies: scopes, transitivity, mediation, management
3. Pattern matching recap: instanceof, switch, records, and sealed types
4. Core Java review: how the pieces fit together
5. Interview angles
6. Common mistakes & debugging
7. Further reading, glossary, answers

### Maven lifecycle, phases, goals, and plugins

#### What it is

Maven has **three built-in lifecycles**: **clean** (`pre-clean`, `clean`, `post-clean`), **default/build** (23 phases: `validate`, `initialize`, `generate-sources`, `process-sources`, `generate-resources`, `process-resources`, `compile`, `process-classes`, `generate-test-sources`, `process-test-sources`, `generate-test-resources`, `process-test-resources`, `test-compile`, `process-test-classes`, `test`, `prepare-package`, `package`, `pre-integration-test`, `integration-test`, `post-integration-test`, `verify`, `install`, `deploy`), and **site** (`pre-site`, `site`, `post-site`, `site-deploy`). A **phase** is a named step; a **goal** is a task implemented by a **plugin** (`plugin:goal`, e.g. `compiler:compile`). Invoking a phase runs *all earlier phases of its lifecycle first*, then the goals bound to each. Bindings come from the **packaging** (`jar`, `war`, `pom`, ...): for `jar` packaging, `process-resources` -> `resources:resources`, `compile` -> `compiler:compile`, `process-test-resources` -> `resources:testResources`, `test-compile` -> `compiler:testCompile`, `test` -> `surefire:test`, `package` -> `jar:jar`, `install` -> `install:install`, `deploy` -> `deploy:deploy`. You can bind extra goals with `<executions>` (JaCoCo's `prepare-agent` and `report`) or call a goal directly (`mvn dependency:tree`, `mvn versions:display-dependency-updates`). The **POM** has coordinates (`groupId:artifactId:version`, `packaging`), `<properties>`, `<dependencies>`, `<dependencyManagement>`, `<build><plugins>` / `<pluginManagement>`, `<profiles>`, `<parent>` (inheritance), and `<modules>` (multi-module reactor). Artifacts are cached in the **local repository** (`~/.m2/repository`) and downloaded from **Maven Central** (or a corporate mirror configured in `settings.xml`). A `-SNAPSHOT` version means *work in progress that can change* and is refreshed; release versions are immutable.

#### Why it exists / why it matters

A standard lifecycle makes every Java project build the same way (`mvn verify`), so CI, IDEs, and new teammates need no project-specific scripts. **Convention over configuration** (`src/main/java`, `src/test/java`, `target/`) plus declared dependencies make builds reproducible. Knowing the phase order explains why `mvn test` compiles first, why `mvn package -DskipTests` still compiles tests, and why integration tests belong in `verify`, not `test`.

#### Pros and cons

**Pros**

- Uniform build interface (`mvn clean verify`) across all projects
- Declarative dependency management with automatic transitive resolution
- Huge plugin ecosystem (compiler, surefire/failsafe, JaCoCo, shade, enforcer, release)
- Multi-module reactors build modules in dependency order

**Cons / tradeoffs**

- XML is verbose; plugin configuration can be opaque
- Transitive dependency conflicts can silently change versions
- Slow startup compared to some tools; plugin version drift without pinning
- SNAPSHOT dependencies make builds non-reproducible

#### What happens without it / when misused

Without understanding phases, people run `mvn compile test package` redundantly, skip `clean` and test against stale classes, or put slow integration tests into the unit-test phase. Unpinned plugin versions let a new release change your build overnight (use `<pluginManagement>` and the Maven Enforcer `requireMavenVersion`). `mvn install` pollutes the local repository with half-baked artifacts; `mvn deploy` without checking the target is a classic accident. Using `-o` (offline) without a primed repository, or deleting `~/.m2` blindly, causes long re-downloads.

#### Syntax and rules

- Run a phase: `mvn compile`, `mvn test`, `mvn verify`, `mvn clean install`; several at once: `mvn clean package` (clean lifecycle up to `clean`, then default lifecycle up to `package`).
- Run a goal directly: `mvn dependency:tree`, `mvn help:effective-pom`, `mvn surefire:test`.
- Useful flags: `-q` (quiet), `-B` (batch), `-DskipTests` (compile tests, do not run), `-Dmaven.test.skip=true` (skip compiling too), `-pl module -am` (build module and what it needs), `-T 1C` (parallel build), `-o` (offline), `-U` (force snapshot update), `-Dtest=Class#method`.
- Bind a goal: `<plugin><artifactId>jacoco-maven-plugin</artifactId><executions><execution><phase>test</phase><goals><goal>report</goal></goals></execution></executions></plugin>`.
- Pin versions: `<pluginManagement><plugins>...</plugins></pluginManagement>` or Maven Wrapper (`./mvnw`).
- Profiles: `<profile><id>ci</id>...</profile>`, activate with `-Pci`.
- Java release: `<maven.compiler.release>21</maven.compiler.release>` (prefer `release` over `source/target`).
- Outputs: `target/classes`, `target/test-classes`, `target/surefire-reports`, `target/*.jar`.

#### Examples

**Example 1.1 — Tiny — what `mvn test` actually does**

```java
$ mvn test
[INFO] --- resources:3.3.1:resources (default-resources) @ demo ---       # process-resources
[INFO] --- compiler:3.13.0:compile (default-compile) @ demo ---          # compile
[INFO] --- resources:3.3.1:testResources (default-testResources) @ demo ---
[INFO] --- compiler:3.13.0:testCompile (default-testCompile) @ demo ---  # test-compile
[INFO] --- surefire:3.5.2:test (default-test) @ demo ---                 # test
# (validate, initialize, ... phases without bound goals print nothing)
```

**Example 1.2 — Tiny — which phases run for `mvn clean package`?**

```java
clean lifecycle  : pre-clean -> clean
default lifecycle: validate -> initialize -> generate-sources -> process-sources -> generate-resources
                   -> process-resources -> compile -> process-classes -> generate-test-sources
                   -> process-test-sources -> generate-test-resources -> process-test-resources
                   -> test-compile -> process-test-classes -> test -> prepare-package -> package
```

**Example 1.3 — Medium — a lean pom.xml with pinned plugins and a CI profile**

```java
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.acme</groupId>
  <artifactId>orders</artifactId>
  <version>1.4.0-SNAPSHOT</version>
  <packaging>jar</packaging>

  <properties>
    <maven.compiler.release>21</maven.compiler.release>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <junit.version>5.11.4</junit.version>
  </properties>

  <dependencies>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>${junit.version}</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <pluginManagement>
      <plugins>
        <plugin>
          <artifactId>maven-surefire-plugin</artifactId>
          <version>3.5.2</version>
        </plugin>
      </plugins>
    </pluginManagement>
  </build>

  <profiles>
    <profile>
      <id>ci</id>
      <build>
        <plugins>
          <plugin>
            <artifactId>maven-surefire-plugin</artifactId>
            <configuration><failIfNoTests>true</failIfNoTests></configuration>
          </plugin>
        </plugins>
      </build>
    </profile>
  </profiles>
</project>
```

#### Quick checks

1. What does `mvn package` run?
2. Phase vs goal?
3. Why do integration tests belong in `verify` rather than `test`?
4. Difference between `-DskipTests` and `-Dmaven.test.skip=true`?

### Dependencies: scopes, transitivity, mediation, management

#### What it is

A **dependency** is identified by `groupId:artifactId:version` (plus `type` and `classifier`). Each has a **scope** that decides which classpaths it joins: **`compile`** (default; compile, test, runtime; propagated transitively), **`provided`** (needed to compile and test, supplied by the runtime container such as a servlet API, *not* packaged or transitive), **`runtime`** (not needed to compile, needed to run: JDBC drivers, logging backends), **`test`** (only test compile/run: JUnit, Mockito, AssertJ), **`system`** (a file on disk; discouraged), and **`import`** (only inside `dependencyManagement` of a `pom` type dependency to import a **BOM** - a Bill of Materials that manages versions). Maven resolves a **dependency graph**: if A depends on B and C, and both depend on different versions of D, **nearest definition wins** (shortest path from your project); on a tie, the **first declared** wins. A direct declaration always beats a transitive one. **Version ranges** (`[1.0,2.0)`, `(,1.5]`, `[1.5]`) exist but make builds non-reproducible, so use them rarely. `<dependencyManagement>` pins versions for the whole project/multi-module build without adding dependencies; `<exclusions>` cuts an unwanted transitive dependency. Versions are compared **component-wise** with qualifiers: `1.9 < 1.10`, and `1.0-alpha < 1.0-beta < 1.0-rc1 < 1.0-SNAPSHOT < 1.0`.

#### Why it exists / why it matters

Real applications have hundreds of transitive dependencies. Scopes keep test libraries out of production jars and keep container APIs out of your WAR; mediation rules make resolution deterministic; dependency management and BOMs (Spring Boot BOM, JUnit BOM, Mockito BOM) keep versions of related libraries consistent. This is the basis for Spring Boot's `spring-boot-starter-parent`, which you will use from Day 25 onward.

#### Pros and cons

**Pros**

- Declarative, automatic resolution of transitive libraries
- Scopes minimise artifact size and classpath leakage
- BOMs / dependencyManagement keep related versions aligned
- `dependency:tree`, `dependency:analyze`, and the enforcer plugin give visibility and guardrails

**Cons / tradeoffs**

- Nearest-wins can silently downgrade a library below what a dependency needs
- Version ranges and SNAPSHOTs make builds irreproducible
- Large transitive graphs create "jar hell" (duplicate classes, conflicting versions)
- Wrong scopes cause `NoClassDefFoundError` at runtime or bloated artifacts

#### What happens without it / when misused

A `provided` servlet API declared as `compile` gets packaged into the WAR and conflicts with the container's copy. A JDBC driver declared as `test` works in tests and is missing in production (`No suitable driver`). Two transitive paths pulling `jackson-databind` 2.9 and 2.17 may resolve to the older one, causing `NoSuchMethodError` only at runtime. Declaring `LATEST`/`RELEASE` or ranges makes yesterday's green build red today. Forgetting that **dependency management does not add dependencies**, only fixes versions of those you (or your dependencies) already use, leads to confusion about why a library is missing.

#### Syntax and rules

- Declare: `<dependency><groupId>org.slf4j</groupId><artifactId>slf4j-api</artifactId><version>2.0.16</version><scope>runtime</scope></dependency>` (scope omitted = `compile`).
- Scope -> classpath table: `compile`: compile+test+runtime; `provided`: compile+test; `runtime`: test+runtime; `test`: test only; `system`: like provided with an explicit `<systemPath>`.
- Inspect: `mvn dependency:tree` (`-Dincludes=groupId:artifactId` to filter, `-Dverbose` to see omitted conflicts), `mvn dependency:analyze` (used-undeclared / declared-unused), `mvn help:effective-pom`.
- Manage versions: `<dependencyManagement><dependencies><dependency>...<version>1.2.3</version></dependency></dependencies></dependencyManagement>`; import a BOM: `<dependency><groupId>org.junit</groupId><artifactId>junit-bom</artifactId><version>5.11.4</version><type>pom</type><scope>import</scope></dependency>`.
- Exclude: `<exclusions><exclusion><groupId>commons-logging</groupId><artifactId>commons-logging</artifactId></exclusion></exclusions>`.
- Ranges: `[1.0,2.0)` (1.0 inclusive, 2.0 exclusive), `[1.5]` exact, `(,1.0]` up to, `[1.0,)` from.
- Version order: numeric components compared as numbers; qualifier order `alpha < beta < milestone < rc < snapshot < (release)`.
- Conflict rule: nearest wins, first declaration wins ties, direct beats transitive. Fix by declaring the version you need directly or managing it.

#### Examples

**Example 2.1 — Tiny — the same library reached by two paths**

```java
your-app
├── lib-a 1.0
│   └── commons-codec 1.10          depth 2
└── lib-b 2.0
    └── util 1.0
        └── commons-codec 1.16      depth 3   (omitted for conflict with 1.10)
# nearest wins -> 1.10; to force 1.16 declare it directly in your pom or in dependencyManagement
```

**Example 2.2 — Tiny — version comparison surprises**

```java
1.9   <  1.10          // numeric components, not text
1.0-alpha < 1.0-rc1 < 1.0-SNAPSHOT < 1.0
1.0 == 1.0.0                      // trailing zeros are insignificant
// "1.10".compareTo("1.9") < 0 as Strings - never compare versions as text
```

**Example 2.3 — Medium — importing a BOM and excluding a transitive dependency**

```java
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.junit</groupId>
      <artifactId>junit-bom</artifactId>
      <version>5.11.4</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<dependencies>
  <dependency>                      <!-- version comes from the BOM -->
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
  </dependency>
  <dependency>
    <groupId>com.example</groupId>
    <artifactId>legacy-client</artifactId>
    <version>3.2.0</version>
    <exclusions>
      <exclusion>
        <groupId>commons-logging</groupId>
        <artifactId>commons-logging</artifactId>
      </exclusion>
    </exclusions>
  </dependency>
</dependencies>
```

#### Quick checks

1. Which classpaths does a `provided` dependency appear on?
2. Two transitive paths bring different versions of a library. Which wins?
3. What does `dependencyManagement` do?
4. Is `1.10` newer than `1.9` in Maven?

### Pattern matching recap: instanceof, switch, records, and sealed types

#### What it is

**Pattern matching** tests a value against a *pattern* and, on success, binds variables. Java 21 supports: **type patterns** (`o instanceof String s`), **record deconstruction patterns** (`o instanceof Point(int x, int y)`, nestable: `Line(Point(var x1, var y1), Point p2)`), and **pattern matching for `switch`** with **guards** (`case Integer i when i > 0 ->`), `case null`, and `default`. A **sealed** interface or class (`sealed interface Shape permits Circle, Square`) restricts its direct subtypes, which lets the compiler verify that a switch covers every subtype (**exhaustiveness**) without a `default`. **Records** are transparent immutable data carriers (`record Circle(double r) implements Shape {}`) with a generated canonical constructor, accessors, `equals`, `hashCode`, `toString`, and optional **compact constructors** for validation. Rules to remember: pattern variables are scoped to where the match is definitely true (`if (!(o instanceof String s)) return; s.length()` works); `case` labels are checked in order and the compiler rejects *dominated* labels (a general pattern before a specific one); a `switch` expression must be exhaustive and uses `yield` in block bodies; `case null` must be explicit or the switch throws `NullPointerException`.

#### Why it exists / why it matters

Before patterns, polymorphic dispatch required every behaviour to live in the type itself (visitor pattern boilerplate), and `instanceof` chains needed casts. Patterns plus sealed types support the opposite style - *data-oriented programming* - where data is a closed set of records and behaviour is a function over them. It is ideal for ASTs, events, commands, results (`Success | Failure`), and JSON-like trees, and the compiler guards you against forgetting a case when the hierarchy grows.

#### Pros and cons

**Pros**

- No casts; less boilerplate than `instanceof` + cast or visitors
- Exhaustiveness checking turns missing cases into compile errors
- Records give immutable value semantics with near-zero code
- Nested record patterns express structure + condition in one place

**Cons / tradeoffs**

- Adding a subtype to a sealed hierarchy breaks every non-defaulted switch (a feature, but a migration cost)
- Overusing `default` disables the exhaustiveness safety net
- Guards and ordering rules can be subtle (dominance errors)
- Records are shallowly immutable: a `List` component can still be mutated unless copied (`List.copyOf` in the compact constructor)

#### What happens without it / when misused

Without sealed + patterns, an `if/else instanceof` chain over `Object` silently ignores new subtypes and fails at runtime far from the cause. A `default -> throw` branch added "for safety" hides the compiler's exhaustiveness check. Placing `case Object o` or `case Number n` before specific cases is a compile error (dominance); placing guarded cases in the wrong order changes behaviour. Forgetting `case null` in a switch over a nullable value produces `NullPointerException`. Records that expose mutable components (arrays, `ArrayList`) break the immutability that callers assume.

#### Syntax and rules

- Type pattern: `if (o instanceof String s && !s.isBlank()) { use(s); }`.
- Record pattern: `if (shape instanceof Rect(double w, double h)) { area = w * h; }`; with `var`: `Rect(var w, var h)`.
- Switch expression with patterns: `return switch (o) { case null -> "null"; case Integer i when i < 0 -> "negative"; case Integer i -> "int"; case String s -> "string " + s.length(); case int[] a -> "ints"; default -> "other"; };`.
- Sealed hierarchy: `sealed interface Expr permits Num, Add {}` + `record Num(int v) implements Expr {}` + `record Add(Expr l, Expr r) implements Expr {}`; `switch (e) { case Num n -> ...; case Add a -> ...; }` needs no `default`.
- Nested deconstruction: `case Add(Num(var a), Num(var b)) -> a + b;`.
- Guards use `when`: `case Add(Expr l, Expr r) when l.equals(r) -> ...`.
- Record validation: `record Range(int lo, int hi) { Range { if (lo > hi) throw new IllegalArgumentException(...); } }`.
- Dominance: more specific cases first; compiler error otherwise.

#### Examples

**Example 3.1 — Tiny — instanceof binding and a record pattern**

```java
Object o = new Point(3, 4);
if (o instanceof Point(int x, int y) && x >= 0) {
    System.out.println(Math.hypot(x, y));      // 5.0
}
record Point(int x, int y) {}
```

**Example 3.2 — Tiny — switch with guards, null, and a sealed result**

```java
sealed interface Result permits Ok, Err {}
record Ok(int value) implements Result {}
record Err(String message) implements Result {}

static String show(Result r) {
    return switch (r) {                 // exhaustive: no default needed
        case Ok(int v) when v == 0 -> "zero";
        case Ok(int v)             -> "value " + v;
        case Err(String m)         -> "error: " + m;
    };
}
```

**Example 3.3 — Medium — a tiny expression tree evaluated and printed with patterns**

```java
sealed interface Expr permits Num, Add, Mul, Neg {}
record Num(int value) implements Expr {}
record Add(Expr left, Expr right) implements Expr {}
record Mul(Expr left, Expr right) implements Expr {}
record Neg(Expr inner) implements Expr {}

static int eval(Expr e) {
    return switch (e) {
        case Num(int v)           -> v;
        case Add(Expr l, Expr r)  -> eval(l) + eval(r);
        case Mul(Expr l, Expr r)  -> eval(l) * eval(r);
        case Neg(Expr inner)      -> -eval(inner);
    };
}

static String show(Expr e) {
    return switch (e) {
        case Num(int v)           -> Integer.toString(v);
        case Add(Expr l, Expr r)  -> "(" + show(l) + " + " + show(r) + ")";
        case Mul(Expr l, Expr r)  -> "(" + show(l) + " * " + show(r) + ")";
        case Neg(Expr inner)      -> "-" + show(inner);
    };
}
// eval(new Add(new Num(2), new Mul(new Num(3), new Num(4)))) == 14
```

#### Quick checks

1. Why can a switch over a sealed interface omit `default`?
2. What is a dominated case label?
3. What happens on `switch (o)` when `o` is null and there is no `case null`?
4. Are records deeply immutable?

### Core Java review: how the pieces fit together

#### What it is

This section is the **checklist for the Core Java capstone**: *Data modelling* - use `record` for immutable values (validation in compact constructors), `enum`/sealed interfaces for closed alternatives, and `Optional` only as a **return type** for "maybe absent". *Collections* - pick by access pattern (`ArrayList` O(1) index, `HashMap` O(1) lookup, `TreeMap` sorted O(log n), `LinkedHashMap` insertion/access order; `ArrayDeque` for stacks/queues); keys need consistent `equals`/`hashCode`; return unmodifiable views/copies (`List.copyOf`). *Streams* - `filter/map/sorted/limit` and collectors (`groupingBy`, `summingLong`, `toMap`, `partitioningBy`), `Comparator.comparing(...).thenComparing(...)`; avoid side effects. *Generics* - bounded types, wildcards (PECS: producer `extends`, consumer `super`). *Exceptions* - exceptions for exceptional states; return a result type (`ParseResult`) when failure is an expected outcome of input validation; always preserve the cause; try-with-resources for `AutoCloseable`. *Concurrency* - prefer immutable data, executors, and higher-level utilities; use virtual threads for blocking tasks and a platform pool for CPU work. *Testing* - tests are the specification; one behaviour per test.

#### Why it exists / why it matters

Core Java is a vocabulary: individually simple features (records, streams, collections, exceptions, threads) combine into programs. Interviews and real code reviews test whether you can choose the *right* feature - e.g. a record instead of a mutable bean, a `LinkedHashMap` access-order map instead of hand-rolled LRU bookkeeping, a result type instead of exceptions for line-by-line validation, `computeIfAbsent` instead of check-then-put.

#### Pros and cons

**Pros**

- Small, orthogonal features that compose well
- Immutable data and pure functions are easy to test and parallelize
- Standard library covers most data-structure needs (no custom code needed)
- Strong static typing with modern inference (`var`, patterns, generics)

**Cons / tradeoffs**

- Many ways to do the same thing - consistency matters in a codebase
- Streams can hurt readability when over-chained; debugging lambdas is harder
- Mutable shared state is easy to introduce accidentally
- Premature optimization (parallel streams, custom caches) often reduces clarity without measurable benefit

#### What happens without it / when misused

Typical review findings: public mutable fields; `null` returned for "not found" instead of `Optional` or an empty collection; `catch (Exception e) {}` swallowing failures; `equals` without `hashCode`; shared `SimpleDateFormat`/`HashMap` across threads; `List<Object>` and raw types; boxed `Integer` equality with `==`; exceptions used for normal control flow (`NumberFormatException` for every bad CSV line is acceptable only if converted into a result at the boundary); infinite caches. A capstone that mixes these correctly demonstrates the whole Core Java track.

#### Syntax and rules

- Immutable value: `record Item(String sku, int qty) { Item { if (qty < 0) throw new IllegalArgumentException("qty"); } }`.
- Result instead of exception for expected failures: `sealed interface ParseResult permits Ok, Failed {}`.
- Group and sum: `items.stream().collect(Collectors.groupingBy(Item::category, TreeMap::new, Collectors.summingLong(Item::valueCents)))`.
- Top N: `items.stream().sorted(Comparator.comparingLong(Item::valueCents).reversed().thenComparing(Item::sku)).limit(n).toList()`.
- Optional: `stream.filter(...).min(comparator)` returns `Optional<T>`.
- LRU: `new LinkedHashMap<>(16, 0.75f, true) { protected boolean removeEldestEntry(Map.Entry<K,V> e) { return size() > capacity; } }`.
- Concurrency: `try (var ex = Executors.newVirtualThreadPerTaskExecutor()) { futures = batches.stream().map(b -> ex.submit(() -> sum(b))).toList(); }` then `get()` each.
- Text: `String.format(Locale.ROOT, "%-10s %10s", name, value)`; `text.lines()` to iterate lines; text blocks for multi-line literals.
- Review checklist: naming, immutability, null policy, exception policy, collection choice, thread-safety, tests for every branch.

#### Examples

**Example 4.1 — Tiny — group, sum, and sort with collectors**

```java
record Sale(String region, long cents) {}
List<Sale> sales = List.of(new Sale("EU", 500), new Sale("US", 300), new Sale("EU", 250));

Map<String, Long> byRegion = sales.stream()
        .collect(Collectors.groupingBy(Sale::region, TreeMap::new, Collectors.summingLong(Sale::cents)));
System.out.println(byRegion);       // {EU=750, US=300}
```

**Example 4.2 — Tiny — expected failures as values, not exceptions**

```java
sealed interface ParseResult permits Ok, Failed {}
record Ok(int value) implements ParseResult {}
record Failed(int line, String reason) implements ParseResult {}

static ParseResult parse(int line, String text) {
    try {
        return new Ok(Integer.parseInt(text.trim()));
    } catch (NumberFormatException e) {
        return new Failed(line, "not a number: " + text);
    }
}
```

**Example 4.3 — Medium — an LRU cache from LinkedHashMap**

```java
import java.util.*;

public final class Lru<K, V> {
    private final Map<K, V> map;

    public Lru(int capacity) {
        this.map = new LinkedHashMap<>(16, 0.75f, true) {          // accessOrder = true
            @Override
            protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
                return size() > capacity;                            // evict least recently used
            }
        };
    }

    public V get(K key) { return map.get(key); }                     // marks the key as recently used
    public void put(K key, V value) { map.put(key, value); }
    public List<K> keys() { return new ArrayList<>(map.keySet()); }  // eldest -> newest
}
```

#### Quick checks

1. When should a failure be a return value instead of an exception?
2. Why must `equals` and `hashCode` be overridden together?
3. What does PECS stand for?
4. Why use `computeIfAbsent`/`merge` rather than `containsKey` + `put`?

## Interview angles

**Q: List the Maven default lifecycle phases in order and say what `mvn clean install` does.**

validate, initialize, generate-sources, process-sources, generate-resources, process-resources, compile, process-classes, generate-test-sources, process-test-sources, generate-test-resources, process-test-resources, test-compile, process-test-classes, test, prepare-package, package, pre-integration-test, integration-test, post-integration-test, verify, install, deploy. `clean install` runs the clean lifecycle up to `clean`, then the default lifecycle up to `install`, copying the artifact to the local repository.

**Q: `provided` vs `runtime` vs `test` scope?**

`provided`: needed to compile and test, supplied at runtime by the container, not packaged. `runtime`: not needed to compile, needed to run and test (JDBC drivers). `test`: only on test classpaths (JUnit, Mockito).

**Q: How does Maven resolve version conflicts between transitive dependencies?**

Nearest-wins (shortest path in the dependency tree), first declaration on ties; direct declarations always win. Control it with direct declarations, `dependencyManagement`, BOM imports, or exclusions; inspect with `mvn dependency:tree`.

**Q: What is a BOM and why use it?**

A Bill of Materials is a POM with a `dependencyManagement` section imported via `<scope>import</scope>` so that all related libraries (Spring Boot, JUnit, Jackson) use consistent, tested versions without repeating them.

**Q: Explain pattern matching for switch and exhaustiveness.**

A switch can test the runtime type (and structure of records) of a value with guards. For sealed hierarchies the compiler checks that all permitted subtypes are covered, so no `default` is needed, and adding a subtype produces compile errors where handling is missing.

**Q: When would you choose a record over a class?**

For immutable data carriers whose identity is their values: DTOs, value objects, map keys, results. Not for entities with mutable lifecycle or inheritance from another class.

**Q: How would you build an LRU cache in Java?**

Extend or wrap `LinkedHashMap` with `accessOrder=true` and override `removeEldestEntry` to evict when size exceeds capacity; for concurrency wrap with synchronization or use a library such as Caffeine.

## Common mistakes & debugging

- Running `mvn package` and expecting integration tests to run (they belong to `verify` with failsafe).
- Putting a runtime-only dependency (JDBC driver) in `test` scope or a container API in `compile` scope.
- Using `LATEST`/`RELEASE` or open version ranges, then wondering why builds differ day to day.
- Assuming `dependencyManagement` adds a dependency to the classpath.
- Comparing versions as strings (`"1.10" < "1.9"`).
- Adding `default` to every switch over a sealed type, silencing exhaustiveness checks.
- Returning mutable collections from records/classes; forgetting defensive copies.
- Using exceptions for expected input failures at scale, or swallowing exceptions with an empty `catch`.

## Further reading

- Maven documentation: *Introduction to the Build Lifecycle*, *Introduction to the Dependency Mechanism*, *POM Reference* (maven.apache.org/guides/)
- *Maven: The Complete Reference* chapters on lifecycle, dependencies, and profiles
- JEP 440 (Record Patterns), JEP 441 (Pattern Matching for switch), JEP 409 (Sealed Classes), JEP 395 (Records) on openjdk.org
- *Data-Oriented Programming in Java* - Brian Goetz, Inside Java / InfoQ
- *Effective Java* (Bloch), items on records, immutability, equals/hashCode, generics, and exceptions
- Oracle Java 21 Language Updates guide (docs.oracle.com/en/java/javase/21/language/)

## Glossary

| Term | Meaning |
|------|---------|
| Lifecycle | Ordered set of phases (clean, default, site) |
| Phase | Named step of a lifecycle; running it runs all earlier phases |
| Goal | Task implemented by a plugin (`compiler:compile`) |
| Packaging | Artifact type (`jar`, `war`, `pom`) that decides default plugin bindings |
| Scope | Controls which classpaths a dependency appears on |
| Mediation | Rule choosing one version when the graph has several (nearest wins) |
| BOM | Bill of Materials: a POM that manages versions of related artifacts |
| Reactor | Maven's multi-module build ordering mechanism |
| Sealed type | Class/interface with a closed set of permitted subtypes |
| Record pattern | Pattern that deconstructs a record's components |
| Exhaustiveness | Compiler guarantee that a switch covers all possible values |
| LRU | Least Recently Used eviction policy |

## Answers

Answers to every **Quick check** above (numbered `section.question`).

- **1.1** — What does `mvn package` run?  
  Every phase of the default lifecycle from `validate` through `package`, executing the plugin goals bound to each (compile, test-compile, test, jar).

- **1.2** — Phase vs goal?  
  A phase is a named step in a lifecycle; a goal is a unit of work provided by a plugin and bound to a phase (or run directly with `plugin:goal`).

- **1.3** — Why do integration tests belong in `verify` rather than `test`?  
  `test` is for fast unit tests; integration tests need the packaged artifact and run via failsafe in `integration-test`/`verify`, so slow tests do not block the quick feedback loop.

- **1.4** — Difference between `-DskipTests` and `-Dmaven.test.skip=true`?  
  The first compiles but does not run tests; the second skips both compiling and running them.

- **2.1** — Which classpaths does a `provided` dependency appear on?  
  Compile and test classpaths; not the runtime classpath and not packaged, because the container supplies it.

- **2.2** — Two transitive paths bring different versions of a library. Which wins?  
  The one nearest to your project in the dependency tree; ties go to the first declared. A direct declaration always wins.

- **2.3** — What does `dependencyManagement` do?  
  It fixes versions (and scopes/exclusions) for dependencies but does not add them to the classpath by itself.

- **2.4** — Is `1.10` newer than `1.9` in Maven?  
  Yes: components compare numerically (10 > 9).

- **3.1** — Why can a switch over a sealed interface omit `default`?  
  The compiler knows all permitted subtypes, so it can verify the switch covers every one (exhaustiveness).

- **3.2** — What is a dominated case label?  
  A label that can never match because an earlier, more general pattern already covers it; it is a compile error.

- **3.3** — What happens on `switch (o)` when `o` is null and there is no `case null`?  
  `NullPointerException`.

- **3.4** — Are records deeply immutable?  
  No - fields are final, but a mutable component (like an `ArrayList`) can still be mutated; copy defensively in the compact constructor.

- **4.1** — When should a failure be a return value instead of an exception?  
  When it is an expected outcome of validating external input (e.g. a bad CSV line) that the caller must handle routinely; exceptions are for unexpected or unrecoverable conditions.

- **4.2** — Why must `equals` and `hashCode` be overridden together?  
  Hash-based collections rely on the contract that equal objects have equal hash codes; breaking it makes lookups fail.

- **4.3** — What does PECS stand for?  
  Producer `extends`, Consumer `super`: use `? extends T` when reading from a structure and `? super T` when writing into it.

- **4.4** — Why use `computeIfAbsent`/`merge` rather than `containsKey` + `put`?  
  They are a single operation (atomic on `ConcurrentHashMap`) and avoid check-then-act races and double lookups.
