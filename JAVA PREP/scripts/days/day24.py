from gen_helpers import sec, task

DAY = dict(
    num=24,
    title="Maven Lifecycle, Scopes & Plugins; Pattern Matching Recap; Core Java Review Challenge",
    theme="Understand what `mvn` really does (lifecycle, scopes, mediation, plugins), consolidate modern Java pattern matching with sealed types and records, and prove your Core Java skills in a capstone challenge.",
    objectives=[
        "Explain Maven's three built-in lifecycles (clean, default, site), phases vs goals, and how plugin goals bind to phases for `jar` packaging",
        "Choose the right dependency scope (`compile`, `provided`, `runtime`, `test`, `system`/`import`) and predict which classpath each lands on",
        "Explain transitive dependencies, nearest-wins mediation, version ranges, exclusions, `dependencyManagement`, and BOM imports; inspect with `dependency:tree`",
        "Configure core plugins (compiler, surefire, failsafe, jar/shade, JaCoCo, enforcer) and profiles",
        "Use `instanceof` patterns, switch patterns with guards, record deconstruction patterns, and exhaustive switches over sealed hierarchies",
        "Combine records, streams, collections, generics, exceptions, `Optional`, and virtual threads in one coherent program",
    ],
    prereqs=["Day 13-21 — exceptions, collections, generics, streams, concurrency", "Day 22 — virtual threads", "Day 23 — JUnit 5 and JaCoCo", "Days 4-5 — records and sealed types (Core Java)"],
    overview="""Core Java ends today with three consolidating themes.

**Build tool literacy.** Every Day 13-23 task is a Maven project; you typed `mvn test` dozens of times. Today you learn *why* it works: Maven is a **plugin execution framework** driven by **lifecycles** made of ordered **phases**. Running `mvn package` does not "run package" - it runs every phase from `validate` up to `package`, and each phase executes the **plugin goals bound to it** (e.g. `compile` -> `maven-compiler-plugin:compile`, `test` -> `maven-surefire-plugin:test`, `package` -> `maven-jar-plugin:jar`). Dependencies are resolved **transitively** with **nearest-wins mediation**, filtered by **scope** (what lands on the compile, runtime, and test classpaths). Most "works on my machine" and "NoSuchMethodError in production" incidents are dependency-resolution problems, and `mvn dependency:tree` is the tool you reach for.

**Pattern matching recap.** Java 21 completes a decade-long push towards *data-oriented programming*: `instanceof` with binding variables (16), `record` types (16), `sealed` hierarchies (17), **pattern matching for `switch`** with guards and `case null` (21), and **record deconstruction patterns** (21). Together they let the compiler check that a switch over a sealed hierarchy is *exhaustive* - add a new subtype and every non-exhaustive switch stops compiling.

**Core Java review challenge.** Task 4 asks you to build a small inventory report: parse CSV safely (no exception-driven control flow), model results with sealed types and records, aggregate with streams and collectors, build an LRU cache from `LinkedHashMap`, and add up values in parallel on virtual threads. Interviewers frequently ask: *Maven lifecycle phases in order*, *scope `provided` vs `runtime`*, *how does Maven pick a version when two paths disagree*, *what is a BOM*, *what is exhaustiveness checking*, *when do you use a record*, plus a live coding exercise combining collections and streams.""",
    sections=[
        sec(
            "Maven lifecycle, phases, goals, and plugins",
            "Maven has **three built-in lifecycles**: **clean** (`pre-clean`, `clean`, `post-clean`), **default/build** (23 phases: `validate`, `initialize`, `generate-sources`, `process-sources`, `generate-resources`, `process-resources`, `compile`, `process-classes`, `generate-test-sources`, `process-test-sources`, `generate-test-resources`, `process-test-resources`, `test-compile`, `process-test-classes`, `test`, `prepare-package`, `package`, `pre-integration-test`, `integration-test`, `post-integration-test`, `verify`, `install`, `deploy`), and **site** (`pre-site`, `site`, `post-site`, `site-deploy`). A **phase** is a named step; a **goal** is a task implemented by a **plugin** (`plugin:goal`, e.g. `compiler:compile`). Invoking a phase runs *all earlier phases of its lifecycle first*, then the goals bound to each. Bindings come from the **packaging** (`jar`, `war`, `pom`, ...): for `jar` packaging, `process-resources` -> `resources:resources`, `compile` -> `compiler:compile`, `process-test-resources` -> `resources:testResources`, `test-compile` -> `compiler:testCompile`, `test` -> `surefire:test`, `package` -> `jar:jar`, `install` -> `install:install`, `deploy` -> `deploy:deploy`. You can bind extra goals with `<executions>` (JaCoCo's `prepare-agent` and `report`) or call a goal directly (`mvn dependency:tree`, `mvn versions:display-dependency-updates`). The **POM** has coordinates (`groupId:artifactId:version`, `packaging`), `<properties>`, `<dependencies>`, `<dependencyManagement>`, `<build><plugins>` / `<pluginManagement>`, `<profiles>`, `<parent>` (inheritance), and `<modules>` (multi-module reactor). Artifacts are cached in the **local repository** (`~/.m2/repository`) and downloaded from **Maven Central** (or a corporate mirror configured in `settings.xml`). A `-SNAPSHOT` version means *work in progress that can change* and is refreshed; release versions are immutable.",
            "A standard lifecycle makes every Java project build the same way (`mvn verify`), so CI, IDEs, and new teammates need no project-specific scripts. **Convention over configuration** (`src/main/java`, `src/test/java`, `target/`) plus declared dependencies make builds reproducible. Knowing the phase order explains why `mvn test` compiles first, why `mvn package -DskipTests` still compiles tests, and why integration tests belong in `verify`, not `test`.",
            ["Uniform build interface (`mvn clean verify`) across all projects", "Declarative dependency management with automatic transitive resolution", "Huge plugin ecosystem (compiler, surefire/failsafe, JaCoCo, shade, enforcer, release)", "Multi-module reactors build modules in dependency order"],
            ["XML is verbose; plugin configuration can be opaque", "Transitive dependency conflicts can silently change versions", "Slow startup compared to some tools; plugin version drift without pinning", "SNAPSHOT dependencies make builds non-reproducible"],
            "Without understanding phases, people run `mvn compile test package` redundantly, skip `clean` and test against stale classes, or put slow integration tests into the unit-test phase. Unpinned plugin versions let a new release change your build overnight (use `<pluginManagement>` and the Maven Enforcer `requireMavenVersion`). `mvn install` pollutes the local repository with half-baked artifacts; `mvn deploy` without checking the target is a classic accident. Using `-o` (offline) without a primed repository, or deleting `~/.m2` blindly, causes long re-downloads.",
            """- Run a phase: `mvn compile`, `mvn test`, `mvn verify`, `mvn clean install`; several at once: `mvn clean package` (clean lifecycle up to `clean`, then default lifecycle up to `package`).
- Run a goal directly: `mvn dependency:tree`, `mvn help:effective-pom`, `mvn surefire:test`.
- Useful flags: `-q` (quiet), `-B` (batch), `-DskipTests` (compile tests, do not run), `-Dmaven.test.skip=true` (skip compiling too), `-pl module -am` (build module and what it needs), `-T 1C` (parallel build), `-o` (offline), `-U` (force snapshot update), `-Dtest=Class#method`.
- Bind a goal: `<plugin><artifactId>jacoco-maven-plugin</artifactId><executions><execution><phase>test</phase><goals><goal>report</goal></goals></execution></executions></plugin>`.
- Pin versions: `<pluginManagement><plugins>...</plugins></pluginManagement>` or Maven Wrapper (`./mvnw`).
- Profiles: `<profile><id>ci</id>...</profile>`, activate with `-Pci`.
- Java release: `<maven.compiler.release>21</maven.compiler.release>` (prefer `release` over `source/target`).
- Outputs: `target/classes`, `target/test-classes`, `target/surefire-reports`, `target/*.jar`.""",
            [
                ("Tiny — what `mvn test` actually does", """$ mvn test
[INFO] --- resources:3.3.1:resources (default-resources) @ demo ---       # process-resources
[INFO] --- compiler:3.13.0:compile (default-compile) @ demo ---          # compile
[INFO] --- resources:3.3.1:testResources (default-testResources) @ demo ---
[INFO] --- compiler:3.13.0:testCompile (default-testCompile) @ demo ---  # test-compile
[INFO] --- surefire:3.5.2:test (default-test) @ demo ---                 # test
# (validate, initialize, ... phases without bound goals print nothing)"""),
                ("Tiny — which phases run for `mvn clean package`?", """clean lifecycle  : pre-clean -> clean
default lifecycle: validate -> initialize -> generate-sources -> process-sources -> generate-resources
                   -> process-resources -> compile -> process-classes -> generate-test-sources
                   -> process-test-sources -> generate-test-resources -> process-test-resources
                   -> test-compile -> process-test-classes -> test -> prepare-package -> package"""),
                ("Medium — a lean pom.xml with pinned plugins and a CI profile", """<project xmlns="http://maven.apache.org/POM/4.0.0">
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
</project>"""),
            ],
            [
                ("What does `mvn package` run?", "Every phase of the default lifecycle from `validate` through `package`, executing the plugin goals bound to each (compile, test-compile, test, jar)."),
                ("Phase vs goal?", "A phase is a named step in a lifecycle; a goal is a unit of work provided by a plugin and bound to a phase (or run directly with `plugin:goal`)."),
                ("Why do integration tests belong in `verify` rather than `test`?", "`test` is for fast unit tests; integration tests need the packaged artifact and run via failsafe in `integration-test`/`verify`, so slow tests do not block the quick feedback loop."),
                ("Difference between `-DskipTests` and `-Dmaven.test.skip=true`?", "The first compiles but does not run tests; the second skips both compiling and running them."),
            ],
        ),
        sec(
            "Dependencies: scopes, transitivity, mediation, management",
            "A **dependency** is identified by `groupId:artifactId:version` (plus `type` and `classifier`). Each has a **scope** that decides which classpaths it joins: **`compile`** (default; compile, test, runtime; propagated transitively), **`provided`** (needed to compile and test, supplied by the runtime container such as a servlet API, *not* packaged or transitive), **`runtime`** (not needed to compile, needed to run: JDBC drivers, logging backends), **`test`** (only test compile/run: JUnit, Mockito, AssertJ), **`system`** (a file on disk; discouraged), and **`import`** (only inside `dependencyManagement` of a `pom` type dependency to import a **BOM** - a Bill of Materials that manages versions). Maven resolves a **dependency graph**: if A depends on B and C, and both depend on different versions of D, **nearest definition wins** (shortest path from your project); on a tie, the **first declared** wins. A direct declaration always beats a transitive one. **Version ranges** (`[1.0,2.0)`, `(,1.5]`, `[1.5]`) exist but make builds non-reproducible, so use them rarely. `<dependencyManagement>` pins versions for the whole project/multi-module build without adding dependencies; `<exclusions>` cuts an unwanted transitive dependency. Versions are compared **component-wise** with qualifiers: `1.9 < 1.10`, and `1.0-alpha < 1.0-beta < 1.0-rc1 < 1.0-SNAPSHOT < 1.0`.",
            "Real applications have hundreds of transitive dependencies. Scopes keep test libraries out of production jars and keep container APIs out of your WAR; mediation rules make resolution deterministic; dependency management and BOMs (Spring Boot BOM, JUnit BOM, Mockito BOM) keep versions of related libraries consistent. This is the basis for Spring Boot's `spring-boot-starter-parent`, which you will use from Day 25 onward.",
            ["Declarative, automatic resolution of transitive libraries", "Scopes minimise artifact size and classpath leakage", "BOMs / dependencyManagement keep related versions aligned", "`dependency:tree`, `dependency:analyze`, and the enforcer plugin give visibility and guardrails"],
            ["Nearest-wins can silently downgrade a library below what a dependency needs", "Version ranges and SNAPSHOTs make builds irreproducible", "Large transitive graphs create \"jar hell\" (duplicate classes, conflicting versions)", "Wrong scopes cause `NoClassDefFoundError` at runtime or bloated artifacts"],
            "A `provided` servlet API declared as `compile` gets packaged into the WAR and conflicts with the container's copy. A JDBC driver declared as `test` works in tests and is missing in production (`No suitable driver`). Two transitive paths pulling `jackson-databind` 2.9 and 2.17 may resolve to the older one, causing `NoSuchMethodError` only at runtime. Declaring `LATEST`/`RELEASE` or ranges makes yesterday's green build red today. Forgetting that **dependency management does not add dependencies**, only fixes versions of those you (or your dependencies) already use, leads to confusion about why a library is missing.",
            """- Declare: `<dependency><groupId>org.slf4j</groupId><artifactId>slf4j-api</artifactId><version>2.0.16</version><scope>runtime</scope></dependency>` (scope omitted = `compile`).
- Scope -> classpath table: `compile`: compile+test+runtime; `provided`: compile+test; `runtime`: test+runtime; `test`: test only; `system`: like provided with an explicit `<systemPath>`.
- Inspect: `mvn dependency:tree` (`-Dincludes=groupId:artifactId` to filter, `-Dverbose` to see omitted conflicts), `mvn dependency:analyze` (used-undeclared / declared-unused), `mvn help:effective-pom`.
- Manage versions: `<dependencyManagement><dependencies><dependency>...<version>1.2.3</version></dependency></dependencies></dependencyManagement>`; import a BOM: `<dependency><groupId>org.junit</groupId><artifactId>junit-bom</artifactId><version>5.11.4</version><type>pom</type><scope>import</scope></dependency>`.
- Exclude: `<exclusions><exclusion><groupId>commons-logging</groupId><artifactId>commons-logging</artifactId></exclusion></exclusions>`.
- Ranges: `[1.0,2.0)` (1.0 inclusive, 2.0 exclusive), `[1.5]` exact, `(,1.0]` up to, `[1.0,)` from.
- Version order: numeric components compared as numbers; qualifier order `alpha < beta < milestone < rc < snapshot < (release)`.
- Conflict rule: nearest wins, first declaration wins ties, direct beats transitive. Fix by declaring the version you need directly or managing it.""",
            [
                ("Tiny — the same library reached by two paths", """your-app
├── lib-a 1.0
│   └── commons-codec 1.10          depth 2
└── lib-b 2.0
    └── util 1.0
        └── commons-codec 1.16      depth 3   (omitted for conflict with 1.10)
# nearest wins -> 1.10; to force 1.16 declare it directly in your pom or in dependencyManagement"""),
                ("Tiny — version comparison surprises", """1.9   <  1.10          // numeric components, not text
1.0-alpha < 1.0-rc1 < 1.0-SNAPSHOT < 1.0
1.0 == 1.0.0                      // trailing zeros are insignificant
// "1.10".compareTo("1.9") < 0 as Strings - never compare versions as text"""),
                ("Medium — importing a BOM and excluding a transitive dependency", """<dependencyManagement>
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
</dependencies>"""),
            ],
            [
                ("Which classpaths does a `provided` dependency appear on?", "Compile and test classpaths; not the runtime classpath and not packaged, because the container supplies it."),
                ("Two transitive paths bring different versions of a library. Which wins?", "The one nearest to your project in the dependency tree; ties go to the first declared. A direct declaration always wins."),
                ("What does `dependencyManagement` do?", "It fixes versions (and scopes/exclusions) for dependencies but does not add them to the classpath by itself."),
                ("Is `1.10` newer than `1.9` in Maven?", "Yes: components compare numerically (10 > 9)."),
            ],
        ),
        sec(
            "Pattern matching recap: instanceof, switch, records, and sealed types",
            "**Pattern matching** tests a value against a *pattern* and, on success, binds variables. Java 21 supports: **type patterns** (`o instanceof String s`), **record deconstruction patterns** (`o instanceof Point(int x, int y)`, nestable: `Line(Point(var x1, var y1), Point p2)`), and **pattern matching for `switch`** with **guards** (`case Integer i when i > 0 ->`), `case null`, and `default`. A **sealed** interface or class (`sealed interface Shape permits Circle, Square`) restricts its direct subtypes, which lets the compiler verify that a switch covers every subtype (**exhaustiveness**) without a `default`. **Records** are transparent immutable data carriers (`record Circle(double r) implements Shape {}`) with a generated canonical constructor, accessors, `equals`, `hashCode`, `toString`, and optional **compact constructors** for validation. Rules to remember: pattern variables are scoped to where the match is definitely true (`if (!(o instanceof String s)) return; s.length()` works); `case` labels are checked in order and the compiler rejects *dominated* labels (a general pattern before a specific one); a `switch` expression must be exhaustive and uses `yield` in block bodies; `case null` must be explicit or the switch throws `NullPointerException`.",
            "Before patterns, polymorphic dispatch required every behaviour to live in the type itself (visitor pattern boilerplate), and `instanceof` chains needed casts. Patterns plus sealed types support the opposite style - *data-oriented programming* - where data is a closed set of records and behaviour is a function over them. It is ideal for ASTs, events, commands, results (`Success | Failure`), and JSON-like trees, and the compiler guards you against forgetting a case when the hierarchy grows.",
            ["No casts; less boilerplate than `instanceof` + cast or visitors", "Exhaustiveness checking turns missing cases into compile errors", "Records give immutable value semantics with near-zero code", "Nested record patterns express structure + condition in one place"],
            ["Adding a subtype to a sealed hierarchy breaks every non-defaulted switch (a feature, but a migration cost)", "Overusing `default` disables the exhaustiveness safety net", "Guards and ordering rules can be subtle (dominance errors)", "Records are shallowly immutable: a `List` component can still be mutated unless copied (`List.copyOf` in the compact constructor)"],
            "Without sealed + patterns, an `if/else instanceof` chain over `Object` silently ignores new subtypes and fails at runtime far from the cause. A `default -> throw` branch added \"for safety\" hides the compiler's exhaustiveness check. Placing `case Object o` or `case Number n` before specific cases is a compile error (dominance); placing guarded cases in the wrong order changes behaviour. Forgetting `case null` in a switch over a nullable value produces `NullPointerException`. Records that expose mutable components (arrays, `ArrayList`) break the immutability that callers assume.",
            """- Type pattern: `if (o instanceof String s && !s.isBlank()) { use(s); }`.
- Record pattern: `if (shape instanceof Rect(double w, double h)) { area = w * h; }`; with `var`: `Rect(var w, var h)`.
- Switch expression with patterns: `return switch (o) { case null -> "null"; case Integer i when i < 0 -> "negative"; case Integer i -> "int"; case String s -> "string " + s.length(); case int[] a -> "ints"; default -> "other"; };`.
- Sealed hierarchy: `sealed interface Expr permits Num, Add {}` + `record Num(int v) implements Expr {}` + `record Add(Expr l, Expr r) implements Expr {}`; `switch (e) { case Num n -> ...; case Add a -> ...; }` needs no `default`.
- Nested deconstruction: `case Add(Num(var a), Num(var b)) -> a + b;`.
- Guards use `when`: `case Add(Expr l, Expr r) when l.equals(r) -> ...`.
- Record validation: `record Range(int lo, int hi) { Range { if (lo > hi) throw new IllegalArgumentException(...); } }`.
- Dominance: more specific cases first; compiler error otherwise.""",
            [
                ("Tiny — instanceof binding and a record pattern", """Object o = new Point(3, 4);
if (o instanceof Point(int x, int y) && x >= 0) {
    System.out.println(Math.hypot(x, y));      // 5.0
}
record Point(int x, int y) {}"""),
                ("Tiny — switch with guards, null, and a sealed result", """sealed interface Result permits Ok, Err {}
record Ok(int value) implements Result {}
record Err(String message) implements Result {}

static String show(Result r) {
    return switch (r) {                 // exhaustive: no default needed
        case Ok(int v) when v == 0 -> "zero";
        case Ok(int v)             -> "value " + v;
        case Err(String m)         -> "error: " + m;
    };
}"""),
                ("Medium — a tiny expression tree evaluated and printed with patterns", """sealed interface Expr permits Num, Add, Mul, Neg {}
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
// eval(new Add(new Num(2), new Mul(new Num(3), new Num(4)))) == 14"""),
            ],
            [
                ("Why can a switch over a sealed interface omit `default`?", "The compiler knows all permitted subtypes, so it can verify the switch covers every one (exhaustiveness)."),
                ("What is a dominated case label?", "A label that can never match because an earlier, more general pattern already covers it; it is a compile error."),
                ("What happens on `switch (o)` when `o` is null and there is no `case null`?", "`NullPointerException`."),
                ("Are records deeply immutable?", "No - fields are final, but a mutable component (like an `ArrayList`) can still be mutated; copy defensively in the compact constructor."),
            ],
        ),
        sec(
            "Core Java review: how the pieces fit together",
            "This section is the **checklist for the Core Java capstone**: *Data modelling* - use `record` for immutable values (validation in compact constructors), `enum`/sealed interfaces for closed alternatives, and `Optional` only as a **return type** for \"maybe absent\". *Collections* - pick by access pattern (`ArrayList` O(1) index, `HashMap` O(1) lookup, `TreeMap` sorted O(log n), `LinkedHashMap` insertion/access order; `ArrayDeque` for stacks/queues); keys need consistent `equals`/`hashCode`; return unmodifiable views/copies (`List.copyOf`). *Streams* - `filter/map/sorted/limit` and collectors (`groupingBy`, `summingLong`, `toMap`, `partitioningBy`), `Comparator.comparing(...).thenComparing(...)`; avoid side effects. *Generics* - bounded types, wildcards (PECS: producer `extends`, consumer `super`). *Exceptions* - exceptions for exceptional states; return a result type (`ParseResult`) when failure is an expected outcome of input validation; always preserve the cause; try-with-resources for `AutoCloseable`. *Concurrency* - prefer immutable data, executors, and higher-level utilities; use virtual threads for blocking tasks and a platform pool for CPU work. *Testing* - tests are the specification; one behaviour per test.",
            "Core Java is a vocabulary: individually simple features (records, streams, collections, exceptions, threads) combine into programs. Interviews and real code reviews test whether you can choose the *right* feature - e.g. a record instead of a mutable bean, a `LinkedHashMap` access-order map instead of hand-rolled LRU bookkeeping, a result type instead of exceptions for line-by-line validation, `computeIfAbsent` instead of check-then-put.",
            ["Small, orthogonal features that compose well", "Immutable data and pure functions are easy to test and parallelize", "Standard library covers most data-structure needs (no custom code needed)", "Strong static typing with modern inference (`var`, patterns, generics)"],
            ["Many ways to do the same thing - consistency matters in a codebase", "Streams can hurt readability when over-chained; debugging lambdas is harder", "Mutable shared state is easy to introduce accidentally", "Premature optimization (parallel streams, custom caches) often reduces clarity without measurable benefit"],
            "Typical review findings: public mutable fields; `null` returned for \"not found\" instead of `Optional` or an empty collection; `catch (Exception e) {}` swallowing failures; `equals` without `hashCode`; shared `SimpleDateFormat`/`HashMap` across threads; `List<Object>` and raw types; boxed `Integer` equality with `==`; exceptions used for normal control flow (`NumberFormatException` for every bad CSV line is acceptable only if converted into a result at the boundary); infinite caches. A capstone that mixes these correctly demonstrates the whole Core Java track.",
            """- Immutable value: `record Item(String sku, int qty) { Item { if (qty < 0) throw new IllegalArgumentException("qty"); } }`.
- Result instead of exception for expected failures: `sealed interface ParseResult permits Ok, Failed {}`.
- Group and sum: `items.stream().collect(Collectors.groupingBy(Item::category, TreeMap::new, Collectors.summingLong(Item::valueCents)))`.
- Top N: `items.stream().sorted(Comparator.comparingLong(Item::valueCents).reversed().thenComparing(Item::sku)).limit(n).toList()`.
- Optional: `stream.filter(...).min(comparator)` returns `Optional<T>`.
- LRU: `new LinkedHashMap<>(16, 0.75f, true) { protected boolean removeEldestEntry(Map.Entry<K,V> e) { return size() > capacity; } }`.
- Concurrency: `try (var ex = Executors.newVirtualThreadPerTaskExecutor()) { futures = batches.stream().map(b -> ex.submit(() -> sum(b))).toList(); }` then `get()` each.
- Text: `String.format(Locale.ROOT, "%-10s %10s", name, value)`; `text.lines()` to iterate lines; text blocks for multi-line literals.
- Review checklist: naming, immutability, null policy, exception policy, collection choice, thread-safety, tests for every branch.""",
            [
                ("Tiny — group, sum, and sort with collectors", """record Sale(String region, long cents) {}
List<Sale> sales = List.of(new Sale("EU", 500), new Sale("US", 300), new Sale("EU", 250));

Map<String, Long> byRegion = sales.stream()
        .collect(Collectors.groupingBy(Sale::region, TreeMap::new, Collectors.summingLong(Sale::cents)));
System.out.println(byRegion);       // {EU=750, US=300}"""),
                ("Tiny — expected failures as values, not exceptions", """sealed interface ParseResult permits Ok, Failed {}
record Ok(int value) implements ParseResult {}
record Failed(int line, String reason) implements ParseResult {}

static ParseResult parse(int line, String text) {
    try {
        return new Ok(Integer.parseInt(text.trim()));
    } catch (NumberFormatException e) {
        return new Failed(line, "not a number: " + text);
    }
}"""),
                ("Medium — an LRU cache from LinkedHashMap", """import java.util.*;

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
}"""),
            ],
            [
                ("When should a failure be a return value instead of an exception?", "When it is an expected outcome of validating external input (e.g. a bad CSV line) that the caller must handle routinely; exceptions are for unexpected or unrecoverable conditions."),
                ("Why must `equals` and `hashCode` be overridden together?", "Hash-based collections rely on the contract that equal objects have equal hash codes; breaking it makes lookups fail."),
                ("What does PECS stand for?", "Producer `extends`, Consumer `super`: use `? extends T` when reading from a structure and `? super T` when writing into it."),
                ("Why use `computeIfAbsent`/`merge` rather than `containsKey` + `put`?", "They are a single operation (atomic on `ConcurrentHashMap`) and avoid check-then-act races and double lookups."),
            ],
        ),
    ],
    interview=[
        ("List the Maven default lifecycle phases in order and say what `mvn clean install` does.", "validate, initialize, generate-sources, process-sources, generate-resources, process-resources, compile, process-classes, generate-test-sources, process-test-sources, generate-test-resources, process-test-resources, test-compile, process-test-classes, test, prepare-package, package, pre-integration-test, integration-test, post-integration-test, verify, install, deploy. `clean install` runs the clean lifecycle up to `clean`, then the default lifecycle up to `install`, copying the artifact to the local repository."),
        ("`provided` vs `runtime` vs `test` scope?", "`provided`: needed to compile and test, supplied at runtime by the container, not packaged. `runtime`: not needed to compile, needed to run and test (JDBC drivers). `test`: only on test classpaths (JUnit, Mockito)."),
        ("How does Maven resolve version conflicts between transitive dependencies?", "Nearest-wins (shortest path in the dependency tree), first declaration on ties; direct declarations always win. Control it with direct declarations, `dependencyManagement`, BOM imports, or exclusions; inspect with `mvn dependency:tree`."),
        ("What is a BOM and why use it?", "A Bill of Materials is a POM with a `dependencyManagement` section imported via `<scope>import</scope>` so that all related libraries (Spring Boot, JUnit, Jackson) use consistent, tested versions without repeating them."),
        ("Explain pattern matching for switch and exhaustiveness.", "A switch can test the runtime type (and structure of records) of a value with guards. For sealed hierarchies the compiler checks that all permitted subtypes are covered, so no `default` is needed, and adding a subtype produces compile errors where handling is missing."),
        ("When would you choose a record over a class?", "For immutable data carriers whose identity is their values: DTOs, value objects, map keys, results. Not for entities with mutable lifecycle or inheritance from another class."),
        ("How would you build an LRU cache in Java?", "Extend or wrap `LinkedHashMap` with `accessOrder=true` and override `removeEldestEntry` to evict when size exceeds capacity; for concurrency wrap with synchronization or use a library such as Caffeine."),
    ],
    mistakes=[
        "Running `mvn package` and expecting integration tests to run (they belong to `verify` with failsafe).",
        "Putting a runtime-only dependency (JDBC driver) in `test` scope or a container API in `compile` scope.",
        "Using `LATEST`/`RELEASE` or open version ranges, then wondering why builds differ day to day.",
        "Assuming `dependencyManagement` adds a dependency to the classpath.",
        "Comparing versions as strings (`\"1.10\" < \"1.9\"`).",
        "Adding `default` to every switch over a sealed type, silencing exhaustiveness checks.",
        "Returning mutable collections from records/classes; forgetting defensive copies.",
        "Using exceptions for expected input failures at scale, or swallowing exceptions with an empty `catch`.",
    ],
    reading=[
        "Maven documentation: *Introduction to the Build Lifecycle*, *Introduction to the Dependency Mechanism*, *POM Reference* (maven.apache.org/guides/)",
        "*Maven: The Complete Reference* chapters on lifecycle, dependencies, and profiles",
        "JEP 440 (Record Patterns), JEP 441 (Pattern Matching for switch), JEP 409 (Sealed Classes), JEP 395 (Records) on openjdk.org",
        "*Data-Oriented Programming in Java* - Brian Goetz, Inside Java / InfoQ",
        "*Effective Java* (Bloch), items on records, immutability, equals/hashCode, generics, and exceptions",
        "Oracle Java 21 Language Updates guide (docs.oracle.com/en/java/javase/21/language/)",
    ],
    glossary=[
        ("Lifecycle", "Ordered set of phases (clean, default, site)"),
        ("Phase", "Named step of a lifecycle; running it runs all earlier phases"),
        ("Goal", "Task implemented by a plugin (`compiler:compile`)"),
        ("Packaging", "Artifact type (`jar`, `war`, `pom`) that decides default plugin bindings"),
        ("Scope", "Controls which classpaths a dependency appears on"),
        ("Mediation", "Rule choosing one version when the graph has several (nearest wins)"),
        ("BOM", "Bill of Materials: a POM that manages versions of related artifacts"),
        ("Reactor", "Maven's multi-module build ordering mechanism"),
        ("Sealed type", "Class/interface with a closed set of permitted subtypes"),
        ("Record pattern", "Pattern that deconstructs a record's components"),
        ("Exhaustiveness", "Compiler guarantee that a switch covers all possible values"),
        ("LRU", "Least Recently Used eviction policy"),
    ],
    tasks=[
        task(
            "maven-lifecycle-and-scopes", "Maven Lifecycle Planner and POM Reader", "Warm-up", "MavenLifecycle",
            "Model Maven in code: compute which phases run for a command line (`mvn clean package`), look up the plugin goal bound to a phase for `jar`/`war`/`pom` packaging, parse the `<dependencies>` of a POM (resolving `${property}` versions and default `compile` scope), and decide which dependencies are on the compile, runtime, and test classpaths.",
            [
                "`MavenLifecycle.phasesUpTo(phase)` returns the lifecycle phases up to and including the named one, for the clean (`pre-clean`, `clean`, `post-clean`), default (23 phases), and site (`pre-site`, `site`, `post-site`, `site-deploy`) lifecycles; unknown/blank -> `IllegalArgumentException`",
                "`MavenLifecycle.plan(phases...)` concatenates `phasesUpTo` for each requested phase **without duplicates** keeping first-seen order (`plan(\"clean\", \"package\")` = clean lifecycle up to clean + default up to package); no arguments -> `IllegalArgumentException`",
                "`MavenLifecycle.boundGoal(packaging, phase)` returns the default plugin goal for `jar`, `war` (`package` -> `war:war`), or `pom` (only `install` and `deploy`) packaging in the default lifecycle; phases without a binding -> empty; unknown packaging or non-default phase -> `IllegalArgumentException`",
                "`PomReader.dependencies(xml)` returns the project's direct `<dependencies>` (not those inside `<dependencyManagement>`) with `${property}` references resolved from `<properties>` (and `project.version`); scope defaults to `compile`; a missing version is `null`; malformed XML or DOCTYPE declarations -> `IllegalArgumentException`",
                "`PomReader.onClasspath(scope, kind)` implements the scope table and `PomReader.classpath(deps, kind)` returns `groupId:artifactId:version` strings in declaration order for the dependencies on that classpath",
            ],
            ["unknown phase names", "dependencies inside `dependencyManagement` and `exclusions` must not leak into the result", "unresolvable `${property}` stays literally as written", "DOCTYPE/external entities must be rejected (XXE)"],
            {"MavenLifecycle.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;

/** Models Maven's built-in lifecycles. */
public final class MavenLifecycle {

    public static final List<String> CLEAN = List.of("pre-clean", "clean", "post-clean");

    public static final List<String> DEFAULT = List.of(
            "validate", "initialize", "generate-sources", "process-sources", "generate-resources", "process-resources",
            "compile", "process-classes", "generate-test-sources", "process-test-sources", "generate-test-resources",
            "process-test-resources", "test-compile", "process-test-classes", "test", "prepare-package", "package",
            "pre-integration-test", "integration-test", "post-integration-test", "verify", "install", "deploy");

    public static final List<String> SITE = List.of("pre-site", "site", "post-site", "site-deploy");

    private MavenLifecycle() {
    }

    public static List<String> phasesUpTo(String phase) {
        //@TODO phasesUpTo | null/blank/unknown -> IllegalArgumentException; find the lifecycle (CLEAN, DEFAULT, SITE) containing the phase and return a copy of its phases from the start up to and including it
        if (phase == null || phase.isBlank()) {
            throw new IllegalArgumentException("phase is blank");
        }
        for (List<String> lifecycle : List.of(CLEAN, DEFAULT, SITE)) {
            int index = lifecycle.indexOf(phase);
            if (index >= 0) {
                return new ArrayList<>(lifecycle.subList(0, index + 1));
            }
        }
        throw new IllegalArgumentException("unknown phase: " + phase);
        //@END
    }

    public static List<String> plan(String... phases) {
        //@TODO plan | no arguments -> IllegalArgumentException; for each requested phase add phasesUpTo(phase) to a LinkedHashSet (keeps order, drops duplicates); return it as a List
        if (phases == null || phases.length == 0) {
            throw new IllegalArgumentException("no phases requested");
        }
        Set<String> ordered = new LinkedHashSet<>();
        for (String phase : phases) {
            ordered.addAll(phasesUpTo(phase));
        }
        return new ArrayList<>(ordered);
        //@END
    }

    public static Optional<String> boundGoal(String packaging, String phase) {
        //@TODO boundGoal | packaging must be jar, war or pom and phase must be in DEFAULT (else IllegalArgumentException); pom binds only install:install and deploy:deploy; jar/war bind process-resources=resources:resources, compile=compiler:compile, process-test-resources=resources:testResources, test-compile=compiler:testCompile, test=surefire:test, package=jar:jar (war:war for war), install=install:install, deploy=deploy:deploy; everything else Optional.empty()
        if (packaging == null || !List.of("jar", "war", "pom").contains(packaging)) {
            throw new IllegalArgumentException("unsupported packaging: " + packaging);
        }
        if (phase == null || !DEFAULT.contains(phase)) {
            throw new IllegalArgumentException("not a default lifecycle phase: " + phase);
        }
        return switch (phase) {
            case "install" -> Optional.of("install:install");
            case "deploy" -> Optional.of("deploy:deploy");
            case "process-resources" -> packaging.equals("pom") ? Optional.empty() : Optional.of("resources:resources");
            case "compile" -> packaging.equals("pom") ? Optional.empty() : Optional.of("compiler:compile");
            case "process-test-resources" -> packaging.equals("pom") ? Optional.empty() : Optional.of("resources:testResources");
            case "test-compile" -> packaging.equals("pom") ? Optional.empty() : Optional.of("compiler:testCompile");
            case "test" -> packaging.equals("pom") ? Optional.empty() : Optional.of("surefire:test");
            case "package" -> switch (packaging) {
                case "jar" -> Optional.of("jar:jar");
                case "war" -> Optional.of("war:war");
                default -> Optional.empty();
            };
            default -> Optional.empty();
        };
        //@END
    }
}
''', "PomReader.java": r'''package @PKG@;

import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.xml.XMLConstants;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

/** Reads dependencies from a POM and applies scope rules. */
public final class PomReader {

    /** Which classpath is being computed. */
    public enum ClasspathKind { COMPILE, RUNTIME, TEST }

    /** A direct dependency as declared in the POM. */
    public record Dependency(String groupId, String artifactId, String version, String scope) {
        public String coordinates() {
            return groupId + ":" + artifactId + ":" + version;
        }
    }

    private static final Pattern PLACEHOLDER = Pattern.compile("\\$\\{([^}]+)}");

    private PomReader() {
    }

    public static List<Dependency> dependencies(String pomXml) {
        //@TODO dependencies | parse with a DocumentBuilderFactory that disallows DOCTYPE (feature http://apache.org/xml/features/disallow-doctype-decl) and wrap parser errors in IllegalArgumentException; collect <properties> children plus project.version; read ONLY project/dependencies/dependency (direct children) with groupId, artifactId, version (resolve ${...} via properties, unresolved stays as is, missing -> null) and scope (default compile)
        Document document = parse(pomXml);
        Element project = document.getDocumentElement();
        Map<String, String> properties = new HashMap<>();
        Element props = child(project, "properties");
        if (props != null) {
            for (Node n = props.getFirstChild(); n != null; n = n.getNextSibling()) {
                if (n instanceof Element e) {
                    properties.put(e.getTagName(), e.getTextContent().trim());
                }
            }
        }
        String projectVersion = childText(project, "version");
        if (projectVersion != null) {
            properties.put("project.version", projectVersion);
        }
        List<Dependency> result = new ArrayList<>();
        Element dependencies = child(project, "dependencies");
        if (dependencies == null) {
            return result;
        }
        for (Node n = dependencies.getFirstChild(); n != null; n = n.getNextSibling()) {
            if (n instanceof Element dep && dep.getTagName().equals("dependency")) {
                String version = childText(dep, "version");
                String scope = childText(dep, "scope");
                result.add(new Dependency(
                        childText(dep, "groupId"),
                        childText(dep, "artifactId"),
                        version == null ? null : resolve(version, properties),
                        scope == null ? "compile" : scope));
            }
        }
        return result;
        //@END
    }

    public static boolean onClasspath(String scope, ClasspathKind kind) {
        //@TODO onClasspath | compile: all three kinds; provided and system: COMPILE and TEST; runtime: RUNTIME and TEST; test: TEST only; null/unknown scope -> IllegalArgumentException
        if (scope == null) {
            throw new IllegalArgumentException("scope is null");
        }
        return switch (scope) {
            case "compile" -> true;
            case "provided", "system" -> kind == ClasspathKind.COMPILE || kind == ClasspathKind.TEST;
            case "runtime" -> kind == ClasspathKind.RUNTIME || kind == ClasspathKind.TEST;
            case "test" -> kind == ClasspathKind.TEST;
            default -> throw new IllegalArgumentException("unknown scope: " + scope);
        };
        //@END
    }

    public static List<String> classpath(List<Dependency> dependencies, ClasspathKind kind) {
        //@TODO classpath | keep the dependencies for which onClasspath(scope, kind) is true and return their coordinates() in declaration order
        List<String> result = new ArrayList<>();
        for (Dependency d : dependencies) {
            if (onClasspath(d.scope(), kind)) {
                result.add(d.coordinates());
            }
        }
        return result;
        //@END
    }

    // ---- helpers (provided) -------------------------------------------------------------

    private static Document parse(String xml) {
        if (xml == null || xml.isBlank()) {
            throw new IllegalArgumentException("empty pom");
        }
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
            factory.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
            factory.setXIncludeAware(false);
            factory.setExpandEntityReferences(false);
            DocumentBuilder builder = factory.newDocumentBuilder();
            builder.setErrorHandler(new org.xml.sax.helpers.DefaultHandler());   // no console noise; fatal errors still throw
            return builder.parse(new InputSource(new StringReader(xml)));
        } catch (ParserConfigurationException | SAXException | IOException e) {
            throw new IllegalArgumentException("cannot parse pom: " + e.getMessage(), e);
        }
    }

    private static Element child(Element parent, String name) {
        for (Node n = parent.getFirstChild(); n != null; n = n.getNextSibling()) {
            if (n instanceof Element e && e.getTagName().equals(name)) {
                return e;
            }
        }
        return null;
    }

    private static String childText(Element parent, String name) {
        Element e = child(parent, name);
        return e == null ? null : e.getTextContent().trim();
    }

    private static String resolve(String value, Map<String, String> properties) {
        Matcher m = PLACEHOLDER.matcher(value);
        StringBuilder sb = new StringBuilder();
        while (m.find()) {
            String replacement = properties.getOrDefault(m.group(1), m.group());
            m.appendReplacement(sb, Matcher.quoteReplacement(replacement));
        }
        m.appendTail(sb);
        return sb.toString();
    }
}
'''},
            {"MavenLifecycleTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

class MavenLifecycleTest {

    @Test
    void r1_defaultLifecycleHasTwentyThreePhasesInOrder() {
        assertThat(MavenLifecycle.DEFAULT).hasSize(23).startsWith("validate", "initialize").endsWith("verify", "install", "deploy");
        assertThat(MavenLifecycle.DEFAULT.indexOf("compile")).isLessThan(MavenLifecycle.DEFAULT.indexOf("test-compile"));
        assertThat(MavenLifecycle.DEFAULT.indexOf("test")).isLessThan(MavenLifecycle.DEFAULT.indexOf("package"));
    }

    @Test
    void r1_phasesUpToCompile() {
        assertThat(MavenLifecycle.phasesUpTo("compile")).containsExactly(
                "validate", "initialize", "generate-sources", "process-sources", "generate-resources", "process-resources", "compile");
    }

    @Test
    void r1_phasesUpToTestIncludesTestCompileButNotPackage() {
        List<String> phases = MavenLifecycle.phasesUpTo("test");
        assertThat(phases).hasSize(15).endsWith("test-compile", "process-test-classes", "test");
        assertThat(phases).doesNotContain("package", "prepare-package");
    }

    @Test
    void r1_otherLifecycles() {
        assertThat(MavenLifecycle.phasesUpTo("pre-clean")).containsExactly("pre-clean");
        assertThat(MavenLifecycle.phasesUpTo("clean")).containsExactly("pre-clean", "clean");
        assertThat(MavenLifecycle.phasesUpTo("post-clean")).containsExactly("pre-clean", "clean", "post-clean");
        assertThat(MavenLifecycle.phasesUpTo("site")).containsExactly("pre-site", "site");
        assertThat(MavenLifecycle.phasesUpTo("deploy")).hasSize(23);
    }

    @Test
    void r1_returnedListsAreIndependentCopies() {
        List<String> phases = MavenLifecycle.phasesUpTo("compile");
        phases.add("hack");
        assertThat(MavenLifecycle.phasesUpTo("compile")).doesNotContain("hack");
        assertThat(MavenLifecycle.DEFAULT).doesNotContain("hack");
    }

    @ParameterizedTest
    @ValueSource(strings = {"", " ", "build", "Compile", "run"})
    void r1_unknownPhasesAreRejected(String phase) {
        assertThatThrownBy(() -> MavenLifecycle.phasesUpTo(phase)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r1_nullPhaseIsRejected() {
        assertThatThrownBy(() -> MavenLifecycle.phasesUpTo(null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r2_cleanPackagePlan() {
        List<String> plan = MavenLifecycle.plan("clean", "package");
        assertThat(plan).hasSize(2 + 17).startsWith("pre-clean", "clean", "validate").endsWith("prepare-package", "package");
        assertThat(plan).doesNotHaveDuplicates();
    }

    @Test
    void r2_overlappingPhasesAreNotRepeated() {
        List<String> plan = MavenLifecycle.plan("package", "test", "compile");
        assertThat(plan).hasSize(17).endsWith("package");
        assertThat(plan).doesNotHaveDuplicates();
        assertThat(MavenLifecycle.plan("test", "package")).isEqualTo(MavenLifecycle.phasesUpTo("package"));
    }

    @Test
    void r2_orderFollowsTheCommandLine() {
        assertThat(MavenLifecycle.plan("site", "clean")).containsExactly("pre-site", "site", "pre-clean", "clean");
    }

    @Test
    void r2_planNeedsAtLeastOnePhase() {
        assertThatThrownBy(() -> MavenLifecycle.plan()).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> MavenLifecycle.plan("compile", "bogus")).isInstanceOf(IllegalArgumentException.class);
    }

    @ParameterizedTest(name = "jar: {0} -> {1}")
    @CsvSource({
            "process-resources,resources:resources",
            "compile,compiler:compile",
            "process-test-resources,resources:testResources",
            "test-compile,compiler:testCompile",
            "test,surefire:test",
            "package,jar:jar",
            "install,install:install",
            "deploy,deploy:deploy"
    })
    void r3_jarBindings(String phase, String goal) {
        assertThat(MavenLifecycle.boundGoal("jar", phase)).contains(goal);
    }

    @ParameterizedTest
    @ValueSource(strings = {"validate", "initialize", "generate-sources", "process-classes", "prepare-package", "integration-test", "verify"})
    void r3_phasesWithoutBindingsAreEmpty(String phase) {
        assertThat(MavenLifecycle.boundGoal("jar", phase)).isEqualTo(Optional.empty());
    }

    @Test
    void r3_warAndPomPackaging() {
        assertThat(MavenLifecycle.boundGoal("war", "package")).contains("war:war");
        assertThat(MavenLifecycle.boundGoal("war", "compile")).contains("compiler:compile");
        assertThat(MavenLifecycle.boundGoal("pom", "compile")).isEmpty();
        assertThat(MavenLifecycle.boundGoal("pom", "test")).isEmpty();
        assertThat(MavenLifecycle.boundGoal("pom", "package")).isEmpty();
        assertThat(MavenLifecycle.boundGoal("pom", "install")).contains("install:install");
        assertThat(MavenLifecycle.boundGoal("pom", "deploy")).contains("deploy:deploy");
    }

    @Test
    void r3_invalidArguments() {
        assertThatThrownBy(() -> MavenLifecycle.boundGoal("ear", "compile")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> MavenLifecycle.boundGoal(null, "compile")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> MavenLifecycle.boundGoal("jar", "clean")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> MavenLifecycle.boundGoal("jar", "nope")).isInstanceOf(IllegalArgumentException.class);
    }
}
''', "PomReaderTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class PomReaderTest {

    private static final String POM = """
            <project>
              <modelVersion>4.0.0</modelVersion>
              <groupId>com.acme</groupId>
              <artifactId>demo</artifactId>
              <version>1.2.0</version>
              <properties>
                <junit.version>5.11.4</junit.version>
                <slf4j.version>2.0.16</slf4j.version>
              </properties>
              <dependencyManagement>
                <dependencies>
                  <dependency>
                    <groupId>org.managed</groupId>
                    <artifactId>only-managed</artifactId>
                    <version>9.9.9</version>
                  </dependency>
                </dependencies>
              </dependencyManagement>
              <dependencies>
                <dependency>
                  <groupId>org.slf4j</groupId>
                  <artifactId>slf4j-api</artifactId>
                  <version>${slf4j.version}</version>
                </dependency>
                <dependency>
                  <groupId>org.junit.jupiter</groupId>
                  <artifactId>junit-jupiter</artifactId>
                  <version>${junit.version}</version>
                  <scope>test</scope>
                </dependency>
                <dependency>
                  <groupId>jakarta.servlet</groupId>
                  <artifactId>jakarta.servlet-api</artifactId>
                  <version>6.0.0</version>
                  <scope>provided</scope>
                </dependency>
                <dependency>
                  <groupId>org.postgresql</groupId>
                  <artifactId>postgresql</artifactId>
                  <version>42.7.4</version>
                  <scope>runtime</scope>
                </dependency>
                <dependency>
                  <groupId>com.acme</groupId>
                  <artifactId>shared-model</artifactId>
                  <version>${project.version}</version>
                  <exclusions>
                    <exclusion>
                      <groupId>commons-logging</groupId>
                      <artifactId>commons-logging</artifactId>
                    </exclusion>
                  </exclusions>
                </dependency>
                <dependency>
                  <groupId>org.unresolved</groupId>
                  <artifactId>mystery</artifactId>
                  <version>${no.such.property}</version>
                </dependency>
                <dependency>
                  <groupId>org.managed</groupId>
                  <artifactId>no-version-here</artifactId>
                </dependency>
              </dependencies>
            </project>
            """;

    @Test
    void r4_readsOnlyDirectDependenciesInOrder() {
        List<PomReader.Dependency> deps = PomReader.dependencies(POM);
        assertThat(deps).extracting(PomReader.Dependency::artifactId)
                .containsExactly("slf4j-api", "junit-jupiter", "jakarta.servlet-api", "postgresql", "shared-model", "mystery", "no-version-here");
    }

    @Test
    void r4_resolvesPropertiesAndDefaultsTheScope() {
        List<PomReader.Dependency> deps = PomReader.dependencies(POM);
        assertThat(deps.get(0)).isEqualTo(new PomReader.Dependency("org.slf4j", "slf4j-api", "2.0.16", "compile"));
        assertThat(deps.get(1)).isEqualTo(new PomReader.Dependency("org.junit.jupiter", "junit-jupiter", "5.11.4", "test"));
        assertThat(deps.get(2).scope()).isEqualTo("provided");
        assertThat(deps.get(3).scope()).isEqualTo("runtime");
        assertThat(deps.get(4).version()).as("project.version").isEqualTo("1.2.0");
        assertThat(deps.get(5).version()).as("unresolvable placeholder stays").isEqualTo("${no.such.property}");
        assertThat(deps.get(6).version()).isNull();
    }

    @Test
    void r4_exclusionsAndManagedDependenciesDoNotLeak() {
        List<PomReader.Dependency> deps = PomReader.dependencies(POM);
        assertThat(deps).extracting(PomReader.Dependency::artifactId).doesNotContain("commons-logging", "only-managed");
    }

    @Test
    void r4_pomWithoutDependenciesIsEmpty() {
        assertThat(PomReader.dependencies("<project><modelVersion>4.0.0</modelVersion></project>")).isEmpty();
    }

    @Test
    void r4_malformedAndHostileXmlIsRejected() {
        assertThatThrownBy(() -> PomReader.dependencies("<project><dependencies>")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> PomReader.dependencies("")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> PomReader.dependencies(null)).isInstanceOf(IllegalArgumentException.class);
        String xxe = "<?xml version=\"1.0\"?><!DOCTYPE project [<!ENTITY x SYSTEM \"file:///etc/passwd\">]><project><groupId>&x;</groupId></project>";
        assertThatThrownBy(() -> PomReader.dependencies(xxe)).isInstanceOf(IllegalArgumentException.class);
    }

    @ParameterizedTest(name = "{0} on {1} = {2}")
    @CsvSource({
            "compile,COMPILE,true", "compile,RUNTIME,true", "compile,TEST,true",
            "provided,COMPILE,true", "provided,RUNTIME,false", "provided,TEST,true",
            "runtime,COMPILE,false", "runtime,RUNTIME,true", "runtime,TEST,true",
            "test,COMPILE,false", "test,RUNTIME,false", "test,TEST,true",
            "system,COMPILE,true", "system,RUNTIME,false", "system,TEST,true"
    })
    void r5_scopeTable(String scope, PomReader.ClasspathKind kind, boolean expected) {
        assertThat(PomReader.onClasspath(scope, kind)).isEqualTo(expected);
    }

    @Test
    void r5_unknownScopeIsRejected() {
        assertThatThrownBy(() -> PomReader.onClasspath("import", PomReader.ClasspathKind.COMPILE)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> PomReader.onClasspath(null, PomReader.ClasspathKind.COMPILE)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r5_classpathsForThePom() {
        List<PomReader.Dependency> deps = PomReader.dependencies(POM);
        assertThat(PomReader.classpath(deps, PomReader.ClasspathKind.COMPILE)).containsExactly(
                "org.slf4j:slf4j-api:2.0.16",
                "jakarta.servlet:jakarta.servlet-api:6.0.0",
                "com.acme:shared-model:1.2.0",
                "org.unresolved:mystery:${no.such.property}",
                "org.managed:no-version-here:null");
        assertThat(PomReader.classpath(deps, PomReader.ClasspathKind.RUNTIME)).containsExactly(
                "org.slf4j:slf4j-api:2.0.16",
                "org.postgresql:postgresql:42.7.4",
                "com.acme:shared-model:1.2.0",
                "org.unresolved:mystery:${no.such.property}",
                "org.managed:no-version-here:null");
        assertThat(PomReader.classpath(deps, PomReader.ClasspathKind.TEST)).hasSize(7);
        assertThat(PomReader.classpath(List.of(), PomReader.ClasspathKind.TEST)).isEmpty();
    }
}
'''},
            ["Keep the three lifecycle lists as the single source of truth; `phasesUpTo` is just `subList(0, index + 1)` on the list that contains the phase.", "Walk the DOM with a helper that returns only **direct** children named X; `getElementsByTagName` would also find dependencies inside `dependencyManagement` and `exclusions`.", "`Matcher.appendReplacement` needs `Matcher.quoteReplacement` when the value contains `$` or `\\`.", "Disable DOCTYPE processing to block XXE; the provided `parse` helper already does it."],
            ["Lifecycle data is not duplicated or mutated", "Direct-children DOM traversal (no `getElementsByTagName` leaks)", "XXE hardening and clear exceptions for bad input"],
            constraints=["Use the JDK's `javax.xml` DOM API only; no third-party XML or Maven libraries", "Do not edit the tests or the provided helper methods in `PomReader`"],
        ),
        task(
            "maven-version-mediation", "Maven Versions, Ranges, and Dependency Mediation", "Core", "MavenVersion",
            "Implement Maven's version ordering (`1.9 < 1.10`, `1.0-alpha < 1.0-rc1 < 1.0-SNAPSHOT < 1.0`), version ranges (`[1.0,2.0)`), and the **nearest-wins** mediation rule used when two dependency paths disagree - the logic behind most 'works locally, `NoSuchMethodError` in prod' incidents.",
            [
                "`MavenVersion.parse(text)` accepts `N(.N)*` optionally followed by `-qualifier` where the qualifier is `alpha|beta|milestone|rc|cr|snapshot|ga|final` (case-insensitive) with an optional number (`rc1`, `rc.2`, `beta-3`); otherwise `IllegalArgumentException` (also for null/blank)",
                "`MavenVersion` implements `Comparable`: numeric components compare numerically with missing components treated as 0 (`1.0 == 1.0.0`), then qualifiers by rank `alpha < beta < milestone < rc(=cr) < snapshot < release(none/ga/final)`, then the qualifier number; `equals`/`hashCode` are consistent with `compareTo`",
                "`VersionRange.parse(spec)` supports `[a,b]`, `[a,b)`, `(a,b]`, `(a,b)`, `[a,)`, `(,b]` and the exact form `[a]`; anything else (plain `1.0`, empty bounds on both sides, lower > upper) -> `IllegalArgumentException`; `contains(version)` honours inclusive/exclusive bounds",
                "`DependencyMediation.resolve(declarations)` picks, for every `groupId:artifactId`, the declaration with the **smallest depth** (ties: first declared) and returns `artifact -> version` in order of first appearance",
                "`DependencyMediation.highest(versions)` returns the highest version string (by `MavenVersion` ordering; empty -> `IllegalArgumentException`) and `satisfying(range, versions)` returns the matching version strings sorted ascending",
            ],
            ["`1.10` vs `1.9`", "`1.0` vs `1.0.0`", "SNAPSHOT vs release vs rc", "unbounded ranges", "ties on depth"],
            {"MavenVersion.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Objects;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** A simplified Maven version with Maven's ordering rules. */
public final class MavenVersion implements Comparable<MavenVersion> {

    private static final Pattern FORMAT = Pattern.compile("(\\d+(?:\\.\\d+)*)(?:-(alpha|beta|milestone|rc|cr|snapshot|ga|final)(?:[.-]?(\\d+))?)?",
            Pattern.CASE_INSENSITIVE);

    private final String text;
    private final List<Integer> numbers;
    private final int rank;
    private final int qualifierNumber;

    private MavenVersion(String text, List<Integer> numbers, int rank, int qualifierNumber) {
        this.text = text;
        this.numbers = numbers;
        this.rank = rank;
        this.qualifierNumber = qualifierNumber;
    }

    public static MavenVersion parse(String text) {
        //@TODO parse | null/blank/non-matching -> IllegalArgumentException; split numeric parts (strip trailing zero components), qualifier rank (alpha 0, beta 1, milestone 2, rc/cr 3, snapshot 4, none/ga/final 5) and qualifier number (default 0)
        if (text == null || text.isBlank()) {
            throw new IllegalArgumentException("version is blank");
        }
        Matcher m = FORMAT.matcher(text.trim());
        if (!m.matches()) {
            throw new IllegalArgumentException("invalid version: " + text);
        }
        List<Integer> numbers = new ArrayList<>();
        for (String part : m.group(1).split("\\.")) {
            numbers.add(Integer.parseInt(part));
        }
        while (!numbers.isEmpty() && numbers.get(numbers.size() - 1) == 0) {
            numbers.remove(numbers.size() - 1);
        }
        int rank = 5;
        if (m.group(2) != null) {
            rank = switch (m.group(2).toLowerCase(Locale.ROOT)) {
                case "alpha" -> 0;
                case "beta" -> 1;
                case "milestone" -> 2;
                case "rc", "cr" -> 3;
                case "snapshot" -> 4;
                default -> 5;
            };
        }
        int qualifierNumber = m.group(3) == null ? 0 : Integer.parseInt(m.group(3));
        return new MavenVersion(text.trim(), List.copyOf(numbers), rank, qualifierNumber);
        //@END
    }

    @Override
    public int compareTo(MavenVersion other) {
        //@TODO compareTo | compare numeric components pairwise (missing = 0), then rank, then qualifierNumber
        int size = Math.max(numbers.size(), other.numbers.size());
        for (int i = 0; i < size; i++) {
            int a = i < numbers.size() ? numbers.get(i) : 0;
            int b = i < other.numbers.size() ? other.numbers.get(i) : 0;
            if (a != b) {
                return Integer.compare(a, b);
            }
        }
        if (rank != other.rank) {
            return Integer.compare(rank, other.rank);
        }
        return Integer.compare(qualifierNumber, other.qualifierNumber);
        //@END
    }

    @Override
    public boolean equals(Object o) {
        return o instanceof MavenVersion other && compareTo(other) == 0;
    }

    @Override
    public int hashCode() {
        return Objects.hash(numbers, rank, qualifierNumber);
    }

    @Override
    public String toString() {
        return text;
    }
}
''', "VersionRange.java": r'''package @PKG@;

/** A Maven version range such as [1.0,2.0). */
public final class VersionRange {

    private final MavenVersion lower;
    private final boolean lowerInclusive;
    private final MavenVersion upper;
    private final boolean upperInclusive;

    private VersionRange(MavenVersion lower, boolean lowerInclusive, MavenVersion upper, boolean upperInclusive) {
        this.lower = lower;
        this.lowerInclusive = lowerInclusive;
        this.upper = upper;
        this.upperInclusive = upperInclusive;
    }

    public static VersionRange parse(String spec) {
        //@TODO parse | null/short/no brackets -> IllegalArgumentException; strip the brackets; no comma means exact [a] (both brackets must be square); otherwise exactly two parts split on the comma, blank part = unbounded, both blank -> IAE, lower > upper -> IAE; remember inclusive ('[' / ']') vs exclusive ('(' / ')')
        if (spec == null || spec.length() < 3) {
            throw new IllegalArgumentException("not a range: " + spec);
        }
        String s = spec.trim();
        char open = s.charAt(0);
        char close = s.charAt(s.length() - 1);
        if ((open != '[' && open != '(') || (close != ']' && close != ')')) {
            throw new IllegalArgumentException("not a range: " + spec);
        }
        String inner = s.substring(1, s.length() - 1);
        if (!inner.contains(",")) {
            if (open != '[' || close != ']') {
                throw new IllegalArgumentException("exact range needs square brackets: " + spec);
            }
            MavenVersion exact = MavenVersion.parse(inner);
            return new VersionRange(exact, true, exact, true);
        }
        String[] parts = inner.split(",", -1);
        if (parts.length != 2) {
            throw new IllegalArgumentException("too many commas: " + spec);
        }
        MavenVersion lo = parts[0].isBlank() ? null : MavenVersion.parse(parts[0]);
        MavenVersion hi = parts[1].isBlank() ? null : MavenVersion.parse(parts[1]);
        if (lo == null && hi == null) {
            throw new IllegalArgumentException("unbounded range: " + spec);
        }
        if (lo != null && hi != null && lo.compareTo(hi) > 0) {
            throw new IllegalArgumentException("lower bound above upper bound: " + spec);
        }
        return new VersionRange(lo, open == '[', hi, close == ']');
        //@END
    }

    public boolean contains(MavenVersion version) {
        //@TODO contains | lower bound (when present): version >= lower if inclusive else > lower; upper bound (when present): version <= upper if inclusive else < upper
        if (lower != null) {
            int cmp = version.compareTo(lower);
            if (lowerInclusive ? cmp < 0 : cmp <= 0) {
                return false;
            }
        }
        if (upper != null) {
            int cmp = version.compareTo(upper);
            if (upperInclusive ? cmp > 0 : cmp >= 0) {
                return false;
            }
        }
        return true;
        //@END
    }
}
''', "DependencyMediation.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Nearest-wins dependency mediation. */
public final class DependencyMediation {

    /** One occurrence of an artifact in the dependency tree. */
    public record Declaration(String artifact, String version, int depth) {
    }

    private DependencyMediation() {
    }

    public static Map<String, String> resolve(List<Declaration> declarations) {
        //@TODO resolve | for every artifact keep the declaration with the smallest depth (the first one wins ties); the result is a LinkedHashMap artifact -> version ordered by first appearance
        Map<String, Declaration> winners = new LinkedHashMap<>();
        for (Declaration d : declarations) {
            winners.merge(d.artifact(), d, (current, candidate) -> candidate.depth() < current.depth() ? candidate : current);
        }
        Map<String, String> result = new LinkedHashMap<>();
        winners.forEach((artifact, d) -> result.put(artifact, d.version()));
        return result;
        //@END
    }

    public static String highest(List<String> versions) {
        //@TODO highest | empty list -> IllegalArgumentException; return the original string of the greatest MavenVersion
        if (versions.isEmpty()) {
            throw new IllegalArgumentException("no versions");
        }
        return versions.stream()
                .max(Comparator.comparing(MavenVersion::parse))
                .orElseThrow();
        //@END
    }

    public static List<String> satisfying(VersionRange range, List<String> versions) {
        //@TODO satisfying | keep versions for which range.contains(MavenVersion.parse(v)) and return them sorted ascending by MavenVersion
        List<String> matching = new ArrayList<>();
        for (String v : versions) {
            if (range.contains(MavenVersion.parse(v))) {
                matching.add(v);
            }
        }
        matching.sort(Comparator.comparing(MavenVersion::parse));
        return matching;
        //@END
    }
}
'''},
            {"MavenVersionTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

class MavenVersionTest {

    private static int cmp(String a, String b) {
        return Integer.signum(MavenVersion.parse(a).compareTo(MavenVersion.parse(b)));
    }

    // ------------------------------------------------------------------ r1 parsing
    @ParameterizedTest
    @ValueSource(strings = {"1", "1.0", "1.0.0", "2.10.3", "1.0-SNAPSHOT", "1.0-alpha", "1.0-alpha2", "1.0-beta-3", "2.0-RC1", "2.0-rc.2", "1.0-GA", "3.1.4-final", "1.0-milestone1", "1.0-cr1"})
    void r1_parsesValidVersions(String text) {
        assertThat(MavenVersion.parse(text)).hasToString(text);
    }

    @ParameterizedTest
    @ValueSource(strings = {"", " ", "abc", "1.", ".1", "1..2", "1.0-", "1.0-foo", "v1.0", "1.0-SNAPSHOT-2x", "1,0"})
    void r1_rejectsInvalidVersions(String text) {
        assertThatThrownBy(() -> MavenVersion.parse(text)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r1_nullIsRejected() {
        assertThatThrownBy(() -> MavenVersion.parse(null)).isInstanceOf(IllegalArgumentException.class);
    }

    // ------------------------------------------------------------------ r2 ordering
    @ParameterizedTest(name = "{0} < {1}")
    @CsvSource({
            "1.9,1.10", "1.2.3,1.2.4", "1.0,1.0.1", "1.99,2.0", "0.9,1",
            "1.0-alpha,1.0-beta", "1.0-beta,1.0-milestone1", "1.0-milestone1,1.0-rc1", "1.0-rc1,1.0-SNAPSHOT",
            "1.0-SNAPSHOT,1.0", "1.0-alpha,1.0", "1.0-rc1,1.0-rc2", "1.0-rc,1.0-rc1", "1.0-beta2,1.0-beta10",
            "1.0-rc1,1.0.1-alpha", "1.0-SNAPSHOT,1.0.1-SNAPSHOT"
    })
    void r2_isOrdered(String lower, String higher) {
        assertThat(cmp(lower, higher)).isEqualTo(-1);
        assertThat(cmp(higher, lower)).isEqualTo(1);
    }

    @ParameterizedTest(name = "{0} == {1}")
    @CsvSource({"1,1.0", "1.0,1.0.0", "1.0.0,1", "2.0-GA,2.0", "2.0-final,2.0", "1.0-rc1,1.0-cr1", "1.0-SNAPSHOT,1.0-snapshot"})
    void r2_equalVersionsCompareEqualAndShareHashCodes(String a, String b) {
        MavenVersion va = MavenVersion.parse(a);
        MavenVersion vb = MavenVersion.parse(b);
        assertThat(va.compareTo(vb)).isZero();
        assertThat(va).isEqualTo(vb);
        assertThat(va.hashCode()).isEqualTo(vb.hashCode());
    }

    @Test
    void r2_sortingARealisticList() {
        List<String> versions = new ArrayList<>(List.of("1.10", "1.9", "1.0-SNAPSHOT", "1.0", "1.0-rc1", "1.0-beta1", "1.0-alpha", "1.2", "1.10-SNAPSHOT", "1.1"));
        Collections.sort(versions, (a, b) -> MavenVersion.parse(a).compareTo(MavenVersion.parse(b)));
        assertThat(versions).containsExactly("1.0-alpha", "1.0-beta1", "1.0-rc1", "1.0-SNAPSHOT", "1.0", "1.1", "1.2", "1.9", "1.10-SNAPSHOT", "1.10");
    }

    // ------------------------------------------------------------------ r3 ranges
    private static boolean in(String range, String version) {
        return VersionRange.parse(range).contains(MavenVersion.parse(version));
    }

    @ParameterizedTest(name = "{0} contains {1} = {2}")
    @CsvSource({
            "'[1.0,2.0)',1.0,true", "'[1.0,2.0)',1.5,true", "'[1.0,2.0)',2.0,false", "'[1.0,2.0)',0.9,false", "'[1.0,2.0)',1.99,true",
            "'(1.0,2.0]',1.0,false", "'(1.0,2.0]',2.0,true", "'(1.0,2.0]',2.1,false",
            "'[1.0,2.0]',1.0,true", "'[1.0,2.0]',2.0,true", "'(1.0,2.0)',1.0,false", "'(1.0,2.0)',2.0,false",
            "'[1.5,)',1.5,true", "'[1.5,)',99.0,true", "'[1.5,)',1.4,false", "'(,1.5]',0.1,true", "'(,1.5]',1.5,true", "'(,1.5]',1.6,false",
            "'(,1.5)',1.5,false", "'[1.5]',1.5,true", "'[1.5]',1.5.0,true", "'[1.5]',1.6,false", "'[1.10,2.0)',1.9,false", "'[1.9,2.0)',1.10,true"
    })
    void r3_contains(String range, String version, boolean expected) {
        assertThat(in(range, version)).isEqualTo(expected);
    }

    @ParameterizedTest
    @ValueSource(strings = {"1.0", "", "[]", "[,]", "(1.0)", "[2.0,1.0]", "[1.0,2.0", "1.0,2.0]", "[1.0,2.0,3.0]", "[x,y]"})
    void r3_rejectsMalformedRanges(String spec) {
        assertThatThrownBy(() -> VersionRange.parse(spec)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r3_nullRangeIsRejected() {
        assertThatThrownBy(() -> VersionRange.parse(null)).isInstanceOf(IllegalArgumentException.class);
    }

    // ------------------------------------------------------------------ r4 mediation
    @Test
    void r4_nearestWins() {
        var result = DependencyMediation.resolve(List.of(
                new DependencyMediation.Declaration("commons-codec:commons-codec", "1.16", 3),
                new DependencyMediation.Declaration("commons-codec:commons-codec", "1.10", 2),
                new DependencyMediation.Declaration("org.slf4j:slf4j-api", "2.0.16", 1)));
        assertThat(result).containsExactly(
                Map.entry("commons-codec:commons-codec", "1.10"),
                Map.entry("org.slf4j:slf4j-api", "2.0.16"));
    }

    @Test
    void r4_firstDeclaredWinsOnTies() {
        var result = DependencyMediation.resolve(List.of(
                new DependencyMediation.Declaration("g:a", "1.0", 2),
                new DependencyMediation.Declaration("g:b", "5.0", 1),
                new DependencyMediation.Declaration("g:a", "2.0", 2),
                new DependencyMediation.Declaration("g:a", "3.0", 4)));
        assertThat(result).containsExactly(Map.entry("g:a", "1.0"), Map.entry("g:b", "5.0"));
    }

    @Test
    void r4_directDeclarationBeatsEverything() {
        var result = DependencyMediation.resolve(List.of(
                new DependencyMediation.Declaration("g:a", "9.9", 2),
                new DependencyMediation.Declaration("g:a", "1.0", 0)));
        assertThat(result.get("g:a")).isEqualTo("1.0");
        assertThat(DependencyMediation.resolve(List.of())).isEmpty();
    }

    // ------------------------------------------------------------------ r5 helpers
    @Test
    void r5_highestUsesVersionOrderingNotTextOrdering() {
        assertThat(DependencyMediation.highest(List.of("1.9", "1.10", "1.2"))).isEqualTo("1.10");
        assertThat(DependencyMediation.highest(List.of("2.0-SNAPSHOT", "2.0-rc1", "1.9"))).isEqualTo("2.0-SNAPSHOT");
        assertThat(DependencyMediation.highest(List.of("2.0", "2.0-SNAPSHOT"))).isEqualTo("2.0");
        assertThat(DependencyMediation.highest(List.of("7"))).isEqualTo("7");
        assertThatThrownBy(() -> DependencyMediation.highest(List.of())).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r5_satisfyingFiltersAndSorts() {
        List<String> available = List.of("2.0", "1.10", "1.2", "1.9", "1.0-SNAPSHOT", "0.9", "1.0", "3.0");
        assertThat(DependencyMediation.satisfying(VersionRange.parse("[1.0,2.0)"), available))
                .containsExactly("1.0", "1.2", "1.9", "1.10");
        assertThat(DependencyMediation.satisfying(VersionRange.parse("(,1.0)"), available))
                .containsExactly("0.9", "1.0-SNAPSHOT");
        assertThat(DependencyMediation.satisfying(VersionRange.parse("[5.0,)"), available)).isEmpty();
        assertThat(Set.copyOf(DependencyMediation.satisfying(VersionRange.parse("[1.0]"), available))).containsExactly("1.0");
    }
}
'''},
            ["Normalize on parse (strip trailing zero components) so `equals`/`hashCode` can rely on the stored list.", "Qualifier **rank** decides first, the qualifier **number** only breaks ties between the same qualifier (`rc1 < rc2`).", "`Map.merge` with a pick-the-nearest function is a compact way to implement mediation while keeping first-seen order in a `LinkedHashMap`."],
            ["`compareTo` is consistent with `equals` and `hashCode`", "Range bounds handle unbounded sides without special-casing callers", "Mediation is deterministic (stable ties)"],
            constraints=["No Maven libraries (`maven-artifact`, etc.) - implement the rules yourself", "Do not edit the tests"],
        ),
        task(
            "pattern-matching-expressions", "Pattern Matching over a Sealed Expression Tree", "Stretch", "PatternLab",
            "Use Java 21 pattern matching end to end: evaluate, print, simplify, and analyse an expression tree built from sealed records with **record deconstruction patterns**, guards, and exhaustive switches; plus a `describe(Object)` method using type patterns, `case null`, array patterns, and `when` guards.",
            [
                "`eval(expr, env)` evaluates `Num`, `Var` (looked up in `env`; unbound -> `IllegalArgumentException(\"unbound variable: x\")`), `Add`, `Mul`, and `Neg` with an **exhaustive switch without `default`**",
                "`show(expr)` renders `Num` (negative numbers in parentheses: `(-3)`), `Var` (its name), `Add` as `(l + r)`, `Mul` as `(l * r)`, and `Neg` as `-` + operand; use a guard (`when`) for negative numbers",
                "`simplify(expr)` simplifies **bottom-up**: constant folding for `Add`/`Mul` of two numbers, `0 + x = x`, `x + 0 = x`, `1 * x = x`, `x * 1 = x`, `0 * x = 0`, `x * 0 = 0`, `-(-x) = x`, `-(Num n) = Num(-n)`",
                "`variables(expr)` returns the sorted set of variable names used in the tree",
                "`describe(object)` returns: `null` -> `\"null\"`; negative `Integer` -> `\"negative int <n>\"`; other `Integer` -> `\"int <n>\"`; blank `String` -> `\"blank string\"`; other `String` -> `\"string of length <n>\"`; `int[]` -> `\"int array of <n>\"`; empty `List` -> `\"empty list\"`; other `List` -> `\"list of <n>\"`; `Expr` -> `\"expression \"` + `show(expr)`; anything else -> `\"other: <SimpleName>\"`",
            ],
            ["unbound variables", "nested negation", "simplification that cascades (a rule enabling another)", "guard order (specific before general)", "null input to `describe`"],
            {"Expr.java": r'''package @PKG@;

/** Provided: a closed expression language. */
public sealed interface Expr permits Expr.Num, Expr.Var, Expr.Add, Expr.Mul, Expr.Neg {

    record Num(int value) implements Expr {
    }

    record Var(String name) implements Expr {
    }

    record Add(Expr left, Expr right) implements Expr {
    }

    record Mul(Expr left, Expr right) implements Expr {
    }

    record Neg(Expr inner) implements Expr {
    }
}
''', "PatternLab.java": r'''package @PKG@;

import @PKG@.Expr.Add;
import @PKG@.Expr.Mul;
import @PKG@.Expr.Neg;
import @PKG@.Expr.Num;
import @PKG@.Expr.Var;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

/** Pattern matching exercises. */
public final class PatternLab {

    private PatternLab() {
    }

    public static int eval(Expr expr, Map<String, Integer> env) {
        //@TODO eval | exhaustive switch (no default) with record patterns: Num -> value; Var -> env lookup or IllegalArgumentException("unbound variable: <name>"); Add -> sum; Mul -> product; Neg -> negation
        return switch (expr) {
            case Num(int value) -> value;
            case Var(String name) -> {
                Integer value = env.get(name);
                if (value == null) {
                    throw new IllegalArgumentException("unbound variable: " + name);
                }
                yield value;
            }
            case Add(Expr left, Expr right) -> eval(left, env) + eval(right, env);
            case Mul(Expr left, Expr right) -> eval(left, env) * eval(right, env);
            case Neg(Expr inner) -> -eval(inner, env);
        };
        //@END
    }

    public static String show(Expr expr) {
        //@TODO show | Num with a guard (negative -> "(-3)"), Num -> digits, Var -> name, Add -> "(l + r)", Mul -> "(l * r)", Neg -> "-" + show(inner)
        return switch (expr) {
            case Num(int value) when value < 0 -> "(" + value + ")";
            case Num(int value) -> Integer.toString(value);
            case Var(String name) -> name;
            case Add(Expr left, Expr right) -> "(" + show(left) + " + " + show(right) + ")";
            case Mul(Expr left, Expr right) -> "(" + show(left) + " * " + show(right) + ")";
            case Neg(Expr inner) -> "-" + show(inner);
        };
        //@END
    }

    public static Expr simplify(Expr expr) {
        //@TODO simplify | bottom-up: simplify the children first, then apply: Add/Mul of two Num folds; 0+x=x, x+0=x, 1*x=x, x*1=x, 0*x=0, x*0=0; Neg(Num n)=Num(-n); Neg(Neg x)=x; otherwise rebuild the node
        return switch (expr) {
            case Num n -> n;
            case Var v -> v;
            case Neg(Expr inner) -> {
                Expr s = simplify(inner);
                if (s instanceof Num(int v)) {
                    yield new Num(-v);
                }
                if (s instanceof Neg(Expr x)) {
                    yield x;
                }
                yield new Neg(s);
            }
            case Add(Expr left, Expr right) -> {
                Expr a = simplify(left);
                Expr b = simplify(right);
                if (a instanceof Num(int x) && b instanceof Num(int y)) {
                    yield new Num(x + y);
                }
                if (isNum(a, 0)) {
                    yield b;
                }
                if (isNum(b, 0)) {
                    yield a;
                }
                yield new Add(a, b);
            }
            case Mul(Expr left, Expr right) -> {
                Expr a = simplify(left);
                Expr b = simplify(right);
                if (a instanceof Num(int x) && b instanceof Num(int y)) {
                    yield new Num(x * y);
                }
                if (isNum(a, 0) || isNum(b, 0)) {
                    yield new Num(0);
                }
                if (isNum(a, 1)) {
                    yield b;
                }
                if (isNum(b, 1)) {
                    yield a;
                }
                yield new Mul(a, b);
            }
        };
        //@END
    }

    public static Set<String> variables(Expr expr) {
        //@TODO variables | collect Var names recursively into a TreeSet (sorted)
        Set<String> names = new TreeSet<>();
        collect(expr, names);
        return names;
        //@END
    }

    public static String describe(Object value) {
        //@TODO describe | switch with patterns in this order: null, negative Integer (guard), Integer, blank String (guard), String, int[], empty List (guard), List, Expr (use show), default "other: " + simple class name
        return switch (value) {
            case null -> "null";
            case Integer i when i < 0 -> "negative int " + i;
            case Integer i -> "int " + i;
            case String s when s.isBlank() -> "blank string";
            case String s -> "string of length " + s.length();
            case int[] array -> "int array of " + array.length;
            case List<?> list when list.isEmpty() -> "empty list";
            case List<?> list -> "list of " + list.size();
            case Expr expr -> "expression " + show(expr);
            default -> "other: " + value.getClass().getSimpleName();
        };
        //@END
    }

    private static boolean isNum(Expr expr, int expected) {
        return expr instanceof Num(int value) && value == expected;
    }

    private static void collect(Expr expr, Set<String> names) {
        switch (expr) {
            case Var(String name) -> names.add(name);
            case Num n -> { }
            case Add(Expr left, Expr right) -> {
                collect(left, names);
                collect(right, names);
            }
            case Mul(Expr left, Expr right) -> {
                collect(left, names);
                collect(right, names);
            }
            case Neg(Expr inner) -> collect(inner, names);
        }
    }
}
'''},
            {"PatternLabTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import @PKG@.Expr.Add;
import @PKG@.Expr.Mul;
import @PKG@.Expr.Neg;
import @PKG@.Expr.Num;
import @PKG@.Expr.Var;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class PatternLabTest {

    private static Num n(int v) {
        return new Num(v);
    }

    private static Var v(String name) {
        return new Var(name);
    }

    // ------------------------------------------------------------------ r1 eval
    @Test
    void r1_evaluatesNestedExpressions() {
        Expr e = new Add(n(2), new Mul(v("x"), n(3)));        // 2 + x * 3
        assertThat(PatternLab.eval(e, Map.of("x", 4))).isEqualTo(14);
        assertThat(PatternLab.eval(new Neg(e), Map.of("x", 4))).isEqualTo(-14);
        assertThat(PatternLab.eval(new Neg(new Neg(n(5))), Map.of())).isEqualTo(5);
        assertThat(PatternLab.eval(n(-9), Map.of())).isEqualTo(-9);
    }

    @Test
    void r1_usesTheEnvironmentForEveryVariable() {
        Expr e = new Add(v("a"), new Mul(v("b"), v("a")));
        assertThat(PatternLab.eval(e, Map.of("a", 2, "b", 5))).isEqualTo(12);
        assertThat(PatternLab.eval(e, Map.of("a", 1, "b", 1))).isEqualTo(2);
    }

    @Test
    void r1_unboundVariableIsReported() {
        assertThatThrownBy(() -> PatternLab.eval(new Add(n(1), v("y")), Map.of("x", 1)))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("unbound variable: y");
    }

    // ------------------------------------------------------------------ r2 show
    @Test
    void r2_rendersInfixWithParentheses() {
        assertThat(PatternLab.show(n(3))).isEqualTo("3");
        assertThat(PatternLab.show(v("x"))).isEqualTo("x");
        assertThat(PatternLab.show(new Add(n(1), n(2)))).isEqualTo("(1 + 2)");
        assertThat(PatternLab.show(new Mul(new Add(n(1), v("x")), n(3)))).isEqualTo("((1 + x) * 3)");
    }

    @Test
    void r2_negativeNumbersAndNegation() {
        assertThat(PatternLab.show(n(-3))).isEqualTo("(-3)");
        assertThat(PatternLab.show(new Neg(v("x")))).isEqualTo("-x");
        assertThat(PatternLab.show(new Neg(new Add(v("x"), n(-1))))).isEqualTo("-(x + (-1))");
        assertThat(PatternLab.show(new Neg(new Neg(n(2))))).isEqualTo("--2");
    }

    // ------------------------------------------------------------------ r3 simplify
    @Test
    void r3_constantFolding() {
        assertThat(PatternLab.simplify(new Add(n(2), n(3)))).isEqualTo(n(5));
        assertThat(PatternLab.simplify(new Mul(n(4), n(5)))).isEqualTo(n(20));
        assertThat(PatternLab.simplify(new Add(new Mul(n(2), n(3)), new Neg(n(1))))).isEqualTo(n(5));
    }

    @Test
    void r3_identities() {
        assertThat(PatternLab.simplify(new Add(n(0), v("x")))).isEqualTo(v("x"));
        assertThat(PatternLab.simplify(new Add(v("x"), n(0)))).isEqualTo(v("x"));
        assertThat(PatternLab.simplify(new Mul(n(1), v("y")))).isEqualTo(v("y"));
        assertThat(PatternLab.simplify(new Mul(v("y"), n(1)))).isEqualTo(v("y"));
        assertThat(PatternLab.simplify(new Mul(n(0), v("x")))).isEqualTo(n(0));
        assertThat(PatternLab.simplify(new Mul(v("x"), n(0)))).isEqualTo(n(0));
    }

    @Test
    void r3_negation() {
        assertThat(PatternLab.simplify(new Neg(n(5)))).isEqualTo(n(-5));
        assertThat(PatternLab.simplify(new Neg(new Neg(v("x"))))).isEqualTo(v("x"));
        assertThat(PatternLab.simplify(new Neg(new Neg(new Neg(v("x")))))).isEqualTo(new Neg(v("x")));
        assertThat(PatternLab.simplify(new Neg(new Add(n(1), n(-1))))).isEqualTo(n(0));
    }

    @Test
    void r3_rulesCascadeBottomUp() {
        // (1 * x) + (0 * y)  ->  x + 0  ->  x
        Expr e = new Add(new Mul(n(1), v("x")), new Mul(n(0), v("y")));
        assertThat(PatternLab.simplify(e)).isEqualTo(v("x"));
        // 2 * ((3 + -3) + x)  ->  2 * x
        Expr f = new Mul(n(2), new Add(new Add(n(3), n(-3)), v("x")));
        assertThat(PatternLab.simplify(f)).isEqualTo(new Mul(n(2), v("x")));
    }

    @Test
    void r3_unsimplifiableTreesAreRebuiltEqual() {
        Expr e = new Add(v("a"), new Mul(v("b"), v("c")));
        assertThat(PatternLab.simplify(e)).isEqualTo(e);
        assertThat(PatternLab.simplify(v("z"))).isEqualTo(v("z"));
    }

    @Test
    void r3_simplifyPreservesTheValue() {
        Expr e = new Add(new Mul(n(1), new Add(v("x"), n(0))), new Neg(new Neg(new Mul(v("y"), n(3)))));
        Map<String, Integer> env = Map.of("x", 7, "y", -2);
        assertThat(PatternLab.eval(PatternLab.simplify(e), env)).isEqualTo(PatternLab.eval(e, env));
        assertThat(PatternLab.simplify(e)).isEqualTo(new Add(v("x"), new Mul(v("y"), n(3))));
    }

    // ------------------------------------------------------------------ r4 variables
    @Test
    void r4_collectsSortedVariableNames() {
        Expr e = new Add(new Mul(v("zeta"), v("alpha")), new Neg(new Add(v("beta"), new Add(n(1), v("alpha")))));
        assertThat(PatternLab.variables(e)).containsExactly("alpha", "beta", "zeta");
        assertThat(PatternLab.variables(new Add(n(1), n(2)))).isEmpty();
    }

    // ------------------------------------------------------------------ r5 describe
    @Test
    void r5_describesNullAndNumbers() {
        assertThat(PatternLab.describe(null)).isEqualTo("null");
        assertThat(PatternLab.describe(-5)).isEqualTo("negative int -5");
        assertThat(PatternLab.describe(0)).isEqualTo("int 0");
        assertThat(PatternLab.describe(42)).isEqualTo("int 42");
    }

    @ParameterizedTest
    @ValueSource(strings = {"", " ", "\t\n"})
    void r5_blankStrings(String s) {
        assertThat(PatternLab.describe(s)).isEqualTo("blank string");
    }

    @Test
    void r5_stringsArraysAndLists() {
        assertThat(PatternLab.describe("hello")).isEqualTo("string of length 5");
        assertThat(PatternLab.describe(new int[] {1, 2, 3})).isEqualTo("int array of 3");
        assertThat(PatternLab.describe(new int[0])).isEqualTo("int array of 0");
        assertThat(PatternLab.describe(List.of())).isEqualTo("empty list");
        assertThat(PatternLab.describe(new ArrayList<>())).isEqualTo("empty list");
        assertThat(PatternLab.describe(List.of(1, 2))).isEqualTo("list of 2");
    }

    @Test
    void r5_expressionsAndOtherTypes() {
        assertThat(PatternLab.describe(new Add(n(1), v("x")))).isEqualTo("expression (1 + x)");
        assertThat(PatternLab.describe(3.5)).isEqualTo("other: Double");
        assertThat(PatternLab.describe(new StringBuilder("x"))).isEqualTo("other: StringBuilder");
        assertThat(PatternLab.describe(new long[] {1})).isEqualTo("other: long[]");
    }
}
'''},
            ["Order matters in a pattern switch: put guarded cases (`when`) **before** the unguarded case of the same type.", "In `simplify`, always simplify children **first**, then look at the simplified children - that is what makes the rules cascade.", "A sealed hierarchy lets the switch be exhaustive without `default`; try adding a new record to `Expr` and watch the compiler point at every switch you must update (then remove it again).", "`record` patterns bind components directly: `case Add(Expr left, Expr right)` - no casts, no accessor calls."],
            ["No `default` in the switches over `Expr` (exhaustiveness checking is intentional)", "No `instanceof` + cast chains where a pattern fits", "Guards and case order are deliberate"],
            constraints=["Do not edit `Expr` or the tests", "No visitor pattern, no `instanceof` + explicit casts"],
        ),
        task(
            "core-java-inventory-challenge", "Core Java Capstone: Inventory Import and Report", "Challenge", "InventoryReport",
            "Pull the track together: validate data with a `record`, model parse outcomes with a sealed `ParseResult` (no exceptions escaping for bad lines), aggregate with streams and collectors, query with `Optional`, evict with a `LinkedHashMap`-based LRU cache, sum in parallel on **virtual threads**, and format a text report.",
            [
                "`Item` validation: `sku`/`category` non-blank (trimmed), `qty >= 0`, `priceCents >= 0`, otherwise `IllegalArgumentException` with a descriptive message; `valueCents()` is `qty * priceCents` as `long` (provided)",
                "`InventoryReport.parseLine(lineNo, line)` splits `sku,category,qty,priceCents` (keeping empty fields) and returns `Ok(item)` or `Failed(lineNo, reason)` - reasons: `expected 4 fields but found N`, `invalid number: ...`, or the validation message; it never throws",
                "`InventoryReport.parse(csv)` numbers lines from 1, skips blank lines, `#` comment lines, and a header line starting with `sku,`, and returns one `ParseResult` per remaining line in order",
                "`valueByCategory(items)` returns a sorted map category -> total `valueCents`; `topN(items, n)` returns the `n` items with the highest value (ties by `sku`), `n < 0` -> `IllegalArgumentException`",
                "`cheapestInStock(items, category)` returns the lowest-priced item of that category (case-insensitive) with `qty > 0`; ties by `sku`; empty `Optional` if none",
                "`parallelTotal(items, batchSize)` sums `valueCents` of all items by splitting them into batches processed on a virtual-thread-per-task executor; `batchSize <= 0` -> `IllegalArgumentException`",
                "`money(cents)` formats as `$1,234.56` (negative: `-$0.05`) and `render(totals)` prints one `name` + right-aligned money row per category (name left-aligned in 10 chars, one space, money right-aligned in 10) followed by a `TOTAL` row",
                "`LruCache<K,V>(capacity)`: `get` (null when absent, marks as recently used), `put`, `size`, `keys()` eldest to newest; capacity <= 0 -> `IllegalArgumentException`; the eldest entry is evicted when capacity is exceeded",
            ],
            ["blank lines, comments, header", "line with too many/few fields", "non-numeric and negative quantities", "zero-quantity items for `cheapestInStock`", "empty collections", "LRU refresh on `get` and on overwriting `put`"],
            {"Item.java": r'''package @PKG@;

/** An inventory line. */
public record Item(String sku, String category, int qty, long priceCents) {

    public Item {
        //@TODO validation | sku and category must be non-null and non-blank (IllegalArgumentException with a message naming the field); qty >= 0; priceCents >= 0; store the trimmed sku and category
        if (sku == null || sku.isBlank()) {
            throw new IllegalArgumentException("sku must not be blank");
        }
        if (category == null || category.isBlank()) {
            throw new IllegalArgumentException("category must not be blank");
        }
        if (qty < 0) {
            throw new IllegalArgumentException("qty must be >= 0 but was " + qty);
        }
        if (priceCents < 0) {
            throw new IllegalArgumentException("priceCents must be >= 0 but was " + priceCents);
        }
        sku = sku.trim();
        category = category.trim();
        //@END
    }

    public long valueCents() {
        return (long) qty * priceCents;
    }
}
''', "ParseResult.java": r'''package @PKG@;

/** Provided: outcome of parsing one CSV line. */
public sealed interface ParseResult {

    /** A valid item. */
    record Ok(Item item) implements ParseResult {
    }

    /** A rejected line with the reason. */
    record Failed(int lineNumber, String reason) implements ParseResult {
    }
}
''', "LruCache.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Least-recently-used cache built on an access-ordered LinkedHashMap. */
public final class LruCache<K, V> {

    private final Map<K, V> map;

    public LruCache(int capacity) {
        //@TODO constructor | capacity <= 0 -> IllegalArgumentException; create new LinkedHashMap<>(16, 0.75f, true) overriding removeEldestEntry to evict when size() > capacity
        if (capacity <= 0) {
            throw new IllegalArgumentException("capacity must be > 0");
        }
        this.map = new LinkedHashMap<>(16, 0.75f, true) {
            @Override
            protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
                return size() > capacity;
            }
        };
        //@END
    }

    public V get(K key) {
        //@TODO get | return map.get(key) (null when absent); access order makes it the most recently used
        return map.get(key);
        //@END
    }

    public void put(K key, V value) {
        //@TODO put | map.put(key, value); an overwrite also refreshes the key
        map.put(key, value);
        //@END
    }

    public int size() {
        return map.size();
    }

    public List<K> keys() {
        //@TODO keys | a new ArrayList of the key set: eldest (least recently used) first
        return new ArrayList<>(map.keySet());
        //@END
    }
}
''', "InventoryReport.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.TreeMap;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.stream.Collectors;

/** CSV import and reporting. */
public final class InventoryReport {

    private InventoryReport() {
    }

    public static ParseResult parseLine(int lineNumber, String line) {
        //@TODO parseLine | split(",", -1); length != 4 -> Failed(line, "expected 4 fields but found N"); parse qty (int) and priceCents (long) - NumberFormatException -> Failed(line, "invalid number: " + message); IllegalArgumentException from Item -> Failed(line, its message); success -> Ok(item); never throw
        String[] fields = line.split(",", -1);
        if (fields.length != 4) {
            return new ParseResult.Failed(lineNumber, "expected 4 fields but found " + fields.length);
        }
        try {
            Item item = new Item(fields[0], fields[1], Integer.parseInt(fields[2].trim()), Long.parseLong(fields[3].trim()));
            return new ParseResult.Ok(item);
        } catch (NumberFormatException e) {
            return new ParseResult.Failed(lineNumber, "invalid number: " + e.getMessage());
        } catch (IllegalArgumentException e) {
            return new ParseResult.Failed(lineNumber, e.getMessage());
        }
        //@END
    }

    public static List<ParseResult> parse(String csv) {
        //@TODO parse | iterate csv.lines() with a 1-based counter; skip blank lines, lines starting with # and a header starting with "sku,"; every other line becomes parseLine(counter, line); null csv -> empty list
        List<ParseResult> results = new ArrayList<>();
        if (csv == null) {
            return results;
        }
        List<String> lines = csv.lines().toList();
        for (int index = 0; index < lines.size(); index++) {
            int lineNumber = index + 1;
            String line = lines.get(index);
            String trimmed = line.trim();
            if (trimmed.isEmpty() || trimmed.startsWith("#") || trimmed.toLowerCase(Locale.ROOT).startsWith("sku,")) {
                continue;
            }
            results.add(parseLine(lineNumber, line));
        }
        return results;
        //@END
    }

    public static Map<String, Long> valueByCategory(List<Item> items) {
        //@TODO valueByCategory | Collectors.groupingBy(Item::category, TreeMap::new, Collectors.summingLong(Item::valueCents))
        return items.stream().collect(Collectors.groupingBy(Item::category, TreeMap::new, Collectors.summingLong(Item::valueCents)));
        //@END
    }

    public static List<Item> topN(List<Item> items, int n) {
        //@TODO topN | n < 0 -> IllegalArgumentException; sort by valueCents descending then sku ascending; limit(n); toList()
        if (n < 0) {
            throw new IllegalArgumentException("n must be >= 0");
        }
        return items.stream()
                .sorted(Comparator.comparingLong(Item::valueCents).reversed().thenComparing(Item::sku))
                .limit(n)
                .toList();
        //@END
    }

    public static Optional<Item> cheapestInStock(List<Item> items, String category) {
        //@TODO cheapestInStock | filter category equalsIgnoreCase and qty > 0; min by priceCents then sku
        return items.stream()
                .filter(i -> i.category().equalsIgnoreCase(category) && i.qty() > 0)
                .min(Comparator.comparingLong(Item::priceCents).thenComparing(Item::sku));
        //@END
    }

    public static long parallelTotal(List<Item> items, int batchSize) {
        //@TODO parallelTotal | batchSize <= 0 -> IllegalArgumentException; split into subList batches; try-with-resources Executors.newVirtualThreadPerTaskExecutor(); submit one Callable<Long> per batch; add up future.get(); wrap ExecutionException in IllegalStateException and restore the interrupt flag on InterruptedException
        if (batchSize <= 0) {
            throw new IllegalArgumentException("batchSize must be > 0");
        }
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            List<Future<Long>> futures = new ArrayList<>();
            for (int start = 0; start < items.size(); start += batchSize) {
                List<Item> batch = items.subList(start, Math.min(items.size(), start + batchSize));
                Callable<Long> task = () -> batch.stream().mapToLong(Item::valueCents).sum();
                futures.add(executor.submit(task));
            }
            long total = 0;
            for (Future<Long> future : futures) {
                total += future.get();
            }
            return total;
        } catch (ExecutionException e) {
            throw new IllegalStateException("batch failed", e.getCause());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("interrupted", e);
        }
        //@END
    }

    public static String money(long cents) {
        //@TODO money | "$" + dollars with thousands separators (Locale.ROOT, ",") + "." + two-digit cents; negative values get a leading "-" before the "$"
        long abs = Math.abs(cents);
        String sign = cents < 0 ? "-" : "";
        return String.format(Locale.ROOT, "%s$%,d.%02d", sign, abs / 100, abs % 100);
        //@END
    }

    public static String render(Map<String, Long> totals) {
        //@TODO render | one row per entry in map order: String.format(Locale.ROOT, "%-10s %10s", name, money(value)); then a last row "TOTAL" with the sum; rows joined with \n (no trailing newline)
        List<String> rows = new ArrayList<>();
        long sum = 0;
        for (Map.Entry<String, Long> e : totals.entrySet()) {
            rows.add(String.format(Locale.ROOT, "%-10s %10s", e.getKey(), money(e.getValue())));
            sum += e.getValue();
        }
        rows.add(String.format(Locale.ROOT, "%-10s %10s", "TOTAL", money(sum)));
        return String.join("\n", rows);
        //@END
    }
}
'''},
            {"InventoryReportTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.IntStream;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

@Timeout(30)
class InventoryReportTest {

    private static final String CSV = """
            sku,category,qty,priceCents
            # seasonal stock
            A-1,books,10,1050
            A-2, toys ,5,250

            bad line
            A-3,toys,x,100
            A-4,books,-1,100
            ,books,1,100
            A-5,games,0,5999
            A-6,games,2,1,extra
            """;

    private static Item item(String sku, String category, int qty, long price) {
        return new Item(sku, category, qty, price);
    }

    // ------------------------------------------------------------------ r1 Item
    @Test
    void r1_itemTrimsAndComputesValue() {
        Item i = item("  X-1 ", " books ", 3, 1_000);
        assertThat(i.sku()).isEqualTo("X-1");
        assertThat(i.category()).isEqualTo("books");
        assertThat(i.valueCents()).isEqualTo(3_000L);
        assertThat(item("big", "c", Integer.MAX_VALUE, 1_000).valueCents()).isEqualTo(Integer.MAX_VALUE * 1_000L);
        assertThat(item("a", "b", 1, 1)).isEqualTo(item("a", "b", 1, 1));
    }

    @Test
    void r1_itemValidation() {
        assertThatThrownBy(() -> item(null, "c", 1, 1)).isInstanceOf(IllegalArgumentException.class).hasMessageContaining("sku");
        assertThatThrownBy(() -> item(" ", "c", 1, 1)).isInstanceOf(IllegalArgumentException.class).hasMessageContaining("sku");
        assertThatThrownBy(() -> item("a", null, 1, 1)).isInstanceOf(IllegalArgumentException.class).hasMessageContaining("category");
        assertThatThrownBy(() -> item("a", "", 1, 1)).isInstanceOf(IllegalArgumentException.class).hasMessageContaining("category");
        assertThatThrownBy(() -> item("a", "c", -1, 1)).isInstanceOf(IllegalArgumentException.class).hasMessageContaining("qty");
        assertThatThrownBy(() -> item("a", "c", 1, -1)).isInstanceOf(IllegalArgumentException.class).hasMessageContaining("price");
        assertThat(item("a", "c", 0, 0).valueCents()).isZero();
    }

    // ------------------------------------------------------------------ r2 parseLine / parse
    @Test
    void r2_parseLineSuccess() {
        assertThat(InventoryReport.parseLine(7, "A-1,books,10,1050")).isEqualTo(new ParseResult.Ok(item("A-1", "books", 10, 1050)));
        assertThat(InventoryReport.parseLine(7, " B , c , 1 , 2 ")).isEqualTo(new ParseResult.Ok(item("B", "c", 1, 2)));
    }

    @Test
    void r2_parseLineFailuresNeverThrow() {
        ParseResult fields = InventoryReport.parseLine(5, "bad line");
        assertThat(fields).isEqualTo(new ParseResult.Failed(5, "expected 4 fields but found 1"));
        assertThat(InventoryReport.parseLine(6, "a,b,1,2,3")).isEqualTo(new ParseResult.Failed(6, "expected 4 fields but found 5"));

        assertThat(InventoryReport.parseLine(1, "a,b,x,2")).isInstanceOfSatisfying(ParseResult.Failed.class,
                f -> assertThat(f.reason()).startsWith("invalid number"));
        assertThat(InventoryReport.parseLine(1, "a,b,1,2.5")).isInstanceOf(ParseResult.Failed.class);
        assertThat(InventoryReport.parseLine(1, "a,b,99999999999,2")).isInstanceOf(ParseResult.Failed.class);
        assertThat(InventoryReport.parseLine(2, "a,b,-1,2")).isInstanceOfSatisfying(ParseResult.Failed.class,
                f -> assertThat(f.reason()).contains("qty"));
        assertThat(InventoryReport.parseLine(3, ",b,1,2")).isInstanceOfSatisfying(ParseResult.Failed.class,
                f -> assertThat(f.reason()).contains("sku"));
    }

    @Test
    void r2_parseSkipsNoiseAndNumbersPhysicalLines() {
        List<ParseResult> results = InventoryReport.parse(CSV);
        assertThat(results).hasSize(8);
        assertThat(results.get(0)).isEqualTo(new ParseResult.Ok(item("A-1", "books", 10, 1050)));
        assertThat(results.get(1)).isEqualTo(new ParseResult.Ok(item("A-2", "toys", 5, 250)));
        assertThat(results.get(2)).isEqualTo(new ParseResult.Failed(6, "expected 4 fields but found 1"));
        assertThat(results.get(3)).isInstanceOfSatisfying(ParseResult.Failed.class, f -> assertThat(f.lineNumber()).isEqualTo(7));
        assertThat(results.get(4)).isInstanceOfSatisfying(ParseResult.Failed.class, f -> assertThat(f.lineNumber()).isEqualTo(8));
        assertThat(results.get(5)).isInstanceOfSatisfying(ParseResult.Failed.class, f -> assertThat(f.lineNumber()).isEqualTo(9));
        assertThat(results.get(6)).isEqualTo(new ParseResult.Ok(item("A-5", "games", 0, 5999)));
        assertThat(results.get(7)).isEqualTo(new ParseResult.Failed(11, "expected 4 fields but found 5"));
    }

    @Test
    void r2_parseHandlesEmptyInput() {
        assertThat(InventoryReport.parse("")).isEmpty();
        assertThat(InventoryReport.parse(null)).isEmpty();
        assertThat(InventoryReport.parse("sku,category,qty,priceCents\n# only comments\n\n")).isEmpty();
    }

    // ------------------------------------------------------------------ r3 aggregation
    private static List<Item> sample() {
        return List.of(
                item("A-1", "books", 10, 1050),   // 10500
                item("A-2", "toys", 5, 250),      // 1250
                item("A-5", "games", 0, 5999),    // 0
                item("A-7", "books", 1, 9500),    // 9500
                item("A-8", "toys", 4, 250),      // 1000
                item("A-9", "toys", 1, 100));     // 100
    }

    @Test
    void r3_valueByCategoryIsSorted() {
        assertThat(InventoryReport.valueByCategory(sample())).containsExactly(
                Map.entry("books", 20_000L), Map.entry("games", 0L), Map.entry("toys", 2_350L));
        assertThat(InventoryReport.valueByCategory(List.of())).isEmpty();
    }

    @Test
    void r3_topNOrdersByValueThenSku() {
        assertThat(InventoryReport.topN(sample(), 3)).extracting(Item::sku).containsExactly("A-1", "A-7", "A-2");
        assertThat(InventoryReport.topN(sample(), 0)).isEmpty();
        assertThat(InventoryReport.topN(sample(), 100)).hasSize(6);
        List<Item> ties = List.of(item("b", "c", 1, 10), item("a", "c", 1, 10), item("c", "c", 2, 5));
        assertThat(InventoryReport.topN(ties, 3)).extracting(Item::sku).containsExactly("a", "b", "c");
        assertThatThrownBy(() -> InventoryReport.topN(sample(), -1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r3_cheapestInStockIgnoresEmptyShelvesAndCase() {
        assertThat(InventoryReport.cheapestInStock(sample(), "TOYS")).map(Item::sku).contains("A-9");
        assertThat(InventoryReport.cheapestInStock(sample(), "books")).map(Item::sku).contains("A-1");
        assertThat(InventoryReport.cheapestInStock(sample(), "games")).as("only an out-of-stock item").isEmpty();
        assertThat(InventoryReport.cheapestInStock(sample(), "garden")).isEmpty();
        List<Item> tie = List.of(item("z", "c", 1, 5), item("m", "c", 1, 5));
        assertThat(InventoryReport.cheapestInStock(tie, "c")).map(Item::sku).contains("m");
    }

    // ------------------------------------------------------------------ r4 parallel total
    @Test
    void r4_parallelTotalMatchesSequentialSum() {
        List<Item> items = IntStream.range(0, 1_000).mapToObj(i -> item("sku-" + i, "c" + (i % 5), i, 3)).toList();
        long expected = items.stream().mapToLong(Item::valueCents).sum();
        assertThat(InventoryReport.parallelTotal(items, 7)).isEqualTo(expected);
        assertThat(InventoryReport.parallelTotal(items, 1)).isEqualTo(expected);
        assertThat(InventoryReport.parallelTotal(items, 5_000)).isEqualTo(expected);
        assertThat(InventoryReport.parallelTotal(List.of(), 3)).isZero();
    }

    @Test
    void r4_parallelTotalRejectsBadBatchSize() {
        assertThatThrownBy(() -> InventoryReport.parallelTotal(sample(), 0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> InventoryReport.parallelTotal(sample(), -3)).isInstanceOf(IllegalArgumentException.class);
    }

    // ------------------------------------------------------------------ r5 formatting
    @ParameterizedTest(name = "{0} -> {1}")
    @CsvSource(delimiter = '|', value = {
            "0|$0.00", "5|$0.05", "99|$0.99", "100|$1.00", "1050|$10.50", "123456|$1,234.56", "123456789|$1,234,567.89",
            "-5|-$0.05", "-123456|-$1,234.56"
    })
    void r5_money(long cents, String expected) {
        assertThat(InventoryReport.money(cents)).isEqualTo(expected);
    }

    private static String row(String name, String money) {
        return name + " ".repeat(21 - name.length() - money.length()) + money;
    }

    @Test
    void r5_renderTable() {
        Map<String, Long> totals = new LinkedHashMap<>();
        totals.put("books", 1050L);
        totals.put("toys", 250L);
        assertThat(InventoryReport.render(totals)).isEqualTo(row("books", "$10.50") + "\n" + row("toys", "$2.50") + "\n" + row("TOTAL", "$13.00"));
        assertThat(InventoryReport.render(Map.of())).isEqualTo(row("TOTAL", "$0.00"));
    }

    @Test
    void r5_endToEnd() {
        List<Item> items = new ArrayList<>();
        for (ParseResult r : InventoryReport.parse(CSV)) {
            if (r instanceof ParseResult.Ok ok) {
                items.add(ok.item());
            }
        }
        assertThat(items).extracting(Item::sku).containsExactly("A-1", "A-2", "A-5");
        assertThat(InventoryReport.render(InventoryReport.valueByCategory(items)))
                .isEqualTo(row("books", "$105.00") + "\n" + row("games", "$0.00") + "\n" + row("toys", "$12.50") + "\n" + row("TOTAL", "$117.50"));
    }

    // ------------------------------------------------------------------ r6 LRU cache
    @Test
    void r6_evictsTheLeastRecentlyUsedEntry() {
        LruCache<String, Integer> cache = new LruCache<>(2);
        cache.put("a", 1);
        cache.put("b", 2);
        assertThat(cache.get("a")).isEqualTo(1);       // a is now most recently used
        cache.put("c", 3);                              // evicts b
        assertThat(cache.get("b")).isNull();
        assertThat(cache.keys()).containsExactly("a", "c");
        assertThat(cache.size()).isEqualTo(2);
    }

    @Test
    void r6_overwritingRefreshesAndKeepsSize() {
        LruCache<String, String> cache = new LruCache<>(3);
        cache.put("x", "1");
        cache.put("y", "2");
        cache.put("z", "3");
        cache.put("x", "one");                          // refresh x
        assertThat(cache.keys()).containsExactly("y", "z", "x");
        cache.put("w", "4");                            // evicts y
        assertThat(cache.keys()).containsExactly("z", "x", "w");
        assertThat(cache.get("x")).isEqualTo("one");
        assertThat(cache.get("missing")).isNull();
        assertThat(cache.keys()).containsExactly("z", "w", "x");
    }

    @Test
    void r6_keysReturnsASnapshot() {
        LruCache<Integer, Integer> cache = new LruCache<>(5);
        cache.put(1, 1);
        List<Integer> keys = cache.keys();
        keys.add(99);
        assertThat(cache.keys()).containsExactly(1);
        assertThat(cache.size()).isEqualTo(1);
    }

    @Test
    void r6_invalidCapacity() {
        assertThatThrownBy(() -> new LruCache<String, String>(0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new LruCache<String, String>(-4)).isInstanceOf(IllegalArgumentException.class);
        LruCache<String, String> one = new LruCache<>(1);
        one.put("a", "1");
        one.put("b", "2");
        assertThat(one.keys()).containsExactly("b");
    }
}
'''},
            ["Parse in two layers: `parseLine` turns *any* string into a `ParseResult`; `parse` only handles line numbering and skipping.", "`Collectors.groupingBy(classifier, TreeMap::new, downstream)` gives you a sorted map directly.", "For `parallelTotal`, submit batches to `Executors.newVirtualThreadPerTaskExecutor()` in a try-with-resources; `subList` views are fine to read from several threads because nothing mutates the list.", "`Comparator.comparingLong(Item::valueCents).reversed().thenComparing(Item::sku)` - reversal applies only to what came before it."],
            ["Bad input never throws out of `parseLine`/`parse`", "Immutable data (records) and unmodifiable results; no shared mutable state in the parallel code", "Streams used for aggregation but loops where they are clearer", "No resource leaks (executor closed, interrupt flag restored)"],
            constraints=["Use records and the sealed `ParseResult`; do not return `null` for missing values (use `Optional`)", "No parallel streams: use virtual threads for `parallelTotal`", "Do not edit the tests or `ParseResult`"],
        ),
    ],
)
