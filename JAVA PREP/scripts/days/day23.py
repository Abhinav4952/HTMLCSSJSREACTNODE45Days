from gen_helpers import sec, task

DAY = dict(
    num=23,
    title="Testing in Depth: JUnit 5, Parameterized Tests, Mockito, TDD, the Test Pyramid, and JaCoCo",
    theme="Write fast, trustworthy tests: master JUnit 5 features, isolate collaborators with Mockito, drive design with TDD, balance the test pyramid, and measure coverage with JaCoCo.",
    objectives=[
        "Use the JUnit 5 (Jupiter) lifecycle, `@Nested`, `@DisplayName`, `assertAll`, `assertThrows`, and `@TempDir` effectively",
        "Write data-driven tests with `@ParameterizedTest` (`@ValueSource`, `@CsvSource`, `@MethodSource`, `@NullSource`)",
        "Create mocks and stubs with Mockito (`@Mock`, `when/thenReturn/thenThrow`, `verify`, `ArgumentCaptor`, `InOrder`, `never`) and know when *not* to mock",
        "Practise the TDD red-green-refactor loop and explain its benefits and limits",
        "Explain the test pyramid (unit, integration, end-to-end) and the cost/feedback trade-offs of each layer",
        "Generate and interpret a JaCoCo report (line vs branch coverage) without worshipping the percentage",
    ],
    prereqs=["Day 13 — exceptions", "Day 16 — lambdas and functional interfaces", "Day 21 — concurrency basics (for flaky-test reasoning)", "Day 24 preview — Maven phases (`test`, `verify`)"],
    overview="""Every day so far, a JUnit 5 test class told you whether your solution was right. Today you learn to **write** those tests. Good tests are *fast* (milliseconds), *independent* (any order, any machine), *repeatable* (no clock/network randomness), *self-validating* (pass/fail, no eyeballing logs), and *timely* (written with or before the code) - the **F.I.R.S.T.** principles.

**JUnit 5** is the platform (`junit-platform`), the programming model (`junit-jupiter`), and the legacy bridge (`vintage`). **Parameterized tests** remove copy-paste by running one test body against many inputs. **Mockito** replaces slow or non-deterministic collaborators (payment gateways, mail servers, clocks) with test doubles so you can verify *interactions*. **TDD** (red -> green -> refactor) uses tests as a design tool: the first failing test forces you to design the API from the caller's side. The **test pyramid** tells you where to invest: many fast unit tests, fewer integration tests, very few end-to-end tests. **JaCoCo** shows which lines and branches your tests actually executed - a map of what is *not* tested, not a certificate of quality. Interviews ask: *unit vs integration test*, *mock vs stub vs spy vs fake*, *what does 100% coverage prove (nothing)*, *how do you test time or randomness*, *how do you test private methods (you don't)*.""",
    sections=[
        sec(
            "JUnit 5: lifecycle, assertions, nested and parameterized tests",
            "JUnit 5 test classes are plain classes; any method annotated **`@Test`** runs, with a **new instance per test method** (default lifecycle) so state cannot leak between tests. Lifecycle hooks: `@BeforeAll` (static, once), `@BeforeEach`, `@AfterEach`, `@AfterAll`. Organize with **`@Nested`** inner classes (grouping by scenario, sharing the outer `@BeforeEach`) and **`@DisplayName`** for readable reports. Assertions: `assertEquals`, `assertTrue`, `assertThrows` (returns the exception for further checks), `assertAll` (reports *all* failures instead of the first), `assertTimeout`, and **AssertJ** (`assertThat(actual).isEqualTo(...)`, rich fluent matchers: `containsExactly`, `extracting`, `hasMessageContaining`, `assertThatThrownBy`). Controls: `@Disabled`, `@Tag`, `@Timeout`, `@RepeatedTest`, `@TempDir` (injects a fresh temporary directory), `Assumptions.assumeTrue`. **Parameterized tests** (`junit-jupiter-params`): `@ParameterizedTest` plus a source - `@ValueSource(ints/strings...)`, `@CsvSource({\"1,I\", \"4,IV\"})`, `@MethodSource(\"cases\")` (a static `Stream<Arguments>`), `@EnumSource`, `@NullSource`, `@EmptySource`, `@NullAndEmptySource`; customize names with `name = \"{0} -> {1}\"`.",
            "Tests are executable documentation and a safety net for refactoring. Parameterized tests make the *table of examples* the specification, so adding a case is one line, and nested classes make the structure mirror the behaviour (\"when stack is empty ...\", \"when stack is full ...\"). Using a fresh instance per test removes the largest cause of flaky suites: shared mutable state.",
            ["Fast feedback and a safety net for refactoring", "Clear, declarative test tables with parameterized tests", "Fresh instance per test isolates state; `@Nested` documents scenarios", "Extension model (`@ExtendWith`) powers Mockito, Spring, and custom behaviour"],
            ["Over-specified tests break on harmless refactors (testing implementation, not behaviour)", "Large parameter tables can hide *why* a case exists - name them", "Slow tests (I/O, sleeps) erode the habit of running them", "Assertions on exception messages are brittle"],
            "Without isolation, tests pass alone and fail together (static state, shared files, ordering). Without parameterization, edge cases are copy-pasted and quietly diverge. Assertions that only check *no exception was thrown* give false confidence. `Thread.sleep` in tests creates flakiness: prefer latches, `Awaitility`, or injected clocks. A test that asserts internal calls (`verify` everything) rather than outcomes pins the implementation and makes refactoring painful. Tests that depend on `HashMap` iteration order, the system clock, time zone, or locale fail randomly on another machine.",
            """- Structure: **Arrange - Act - Assert** (a.k.a. Given - When - Then); one logical behaviour per test; name tests by behaviour (`rejectsNegativeAmount`).
- `@Test void name() { ... }` - package-private is fine in Jupiter.
- Exceptions: `assertThrows(IllegalArgumentException.class, () -> f(-1))` or `assertThatThrownBy(() -> f(-1)).isInstanceOf(IAE.class).hasMessageContaining("negative")`.
- Grouped failures: `assertAll("fields", () -> assertEquals(..), () -> assertEquals(..))`.
- Parameterized: `@ParameterizedTest(name = "{0} -> {1}") @CsvSource({"1,I", "4,IV"}) void toRoman(int n, String expected) { ... }`; complex objects via `@MethodSource("cases")` returning `Stream<Arguments>`; `@NullSource` / `@EmptySource` for edge inputs.
- Nested: `@Nested class WhenEmpty { @BeforeEach void setUp() {...} @Test void ... }` (inner class, not static).
- Temp files: `void writes(@TempDir Path dir) { Files.writeString(dir.resolve("a.txt"), "x"); }`.
- Run: `mvn test`, one class `mvn -Dtest=MyTest test`, one method `mvn -Dtest=MyTest#name test`.""",
            [
                ("Tiny — assertThrows and assertAll", """@Test
void rejectsNegativeAges() {
    IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> new Person("Ada", -1));
    assertTrue(ex.getMessage().contains("age"));
}

@Test
void exposesAllFields() {
    Person p = new Person("Ada", 36);
    assertAll("person",
            () -> assertEquals("Ada", p.name()),
            () -> assertEquals(36, p.age()));
}"""),
                ("Tiny — one body, many rows", """@ParameterizedTest(name = "{0} -> {1}")
@CsvSource({"1,I", "4,IV", "9,IX", "14,XIV", "1994,MCMXCIV"})
void toRoman(int number, String expected) {
    assertEquals(expected, RomanNumerals.toRoman(number));
}

@ParameterizedTest
@ValueSource(ints = {0, -1, 4000})
void toRomanRejectsOutOfRange(int number) {
    assertThrows(IllegalArgumentException.class, () -> RomanNumerals.toRoman(number));
}"""),
                ("Medium — nested scenarios with a shared fixture", """import static org.junit.jupiter.api.Assertions.*;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.NoSuchElementException;
import org.junit.jupiter.api.*;

@DisplayName("A stack")
class StackTest {
    private Deque<String> stack;

    @BeforeEach
    void create() {
        stack = new ArrayDeque<>();
    }

    @Nested
    @DisplayName("when empty")
    class WhenEmpty {
        @Test
        void popFails() {
            assertThrows(NoSuchElementException.class, stack::pop);
        }
    }

    @Nested
    @DisplayName("after one push")
    class AfterPush {
        @BeforeEach
        void push() {
            stack.push("a");        // runs after the outer @BeforeEach
        }

        @Test
        void popReturnsTheElement() {
            assertEquals("a", stack.pop());
            assertTrue(stack.isEmpty());
        }
    }
}"""),
            ],
            [
                ("Why does JUnit 5 create a new test-class instance for every test method?", "To isolate tests: instance fields set by one test cannot leak into another (the default `Lifecycle.PER_METHOD`)."),
                ("What does `assertAll` give you over several plain assertions?", "It runs every assertion and reports all failures together instead of stopping at the first one."),
                ("Name three argument sources for `@ParameterizedTest`.", "`@ValueSource`, `@CsvSource`, `@MethodSource` (also `@EnumSource`, `@NullSource`, `@EmptySource`)."),
                ("How do you test that a method throws and inspect the exception?", "`assertThrows(Type.class, executable)` returns the exception; or AssertJ `assertThatThrownBy(...)`."),
            ],
        ),
        sec(
            "Mockito and test doubles: mock, stub, spy, fake",
            "A **test double** stands in for a real collaborator. Gerard Meszaros' taxonomy: a **dummy** fills a parameter list; a **stub** returns canned answers; a **mock** records interactions so the test can *verify* them; a **spy** wraps a real object and records calls; a **fake** is a lightweight working implementation (in-memory repository). **Mockito** creates mocks of interfaces and classes at runtime. `@ExtendWith(MockitoExtension.class)` initialises `@Mock`, `@Spy`, `@Captor`, and `@InjectMocks` fields and enables **strict stubs** (unused stubbings fail the test). Stub with `when(repo.find(1)).thenReturn(Optional.of(x))`, `thenThrow(...)`, `thenAnswer(inv -> ...)`; for `void` methods use `doThrow(...).when(mock).method()`. Verify with `verify(mock).send(\"a\")`, `verify(mock, times(2))`, `never()`, `atLeastOnce()`, `verifyNoInteractions(mock)`, `verifyNoMoreInteractions(mock)`, `inOrder(a, b).verify(...)`. **Argument matchers** (`any()`, `eq()`, `anyString()`, `argThat(...)`) must be used for *all* arguments of a call or none; **`ArgumentCaptor`** captures what was passed so you can assert on it. Mockito 5 uses the *inline* mock maker by default, so final classes and static methods (`mockStatic`) can be mocked, but you rarely should.",
            "Unit tests must be fast and deterministic, but real code talks to databases, payment providers, mail servers, and clocks. Test doubles let you (a) make the collaborator behave in ways that are hard to provoke (timeouts, declined payments), (b) assert that the right side effects happened (email sent exactly once, refund before restock), and (c) keep tests in-memory and parallelizable. Mocking at a **boundary you own** (an interface your code defines) also pushes you toward cleaner designs with injected dependencies.",
            ["Isolates the unit under test from slow or flaky dependencies", "Lets you provoke failures (exceptions, timeouts) on demand", "Verifies interactions that have no return value (events, notifications)", "Works great with constructor injection and small interfaces"],
            ["Over-mocking couples tests to implementation details; refactors break tests that still describe correct behaviour", "A mock can disagree with the real collaborator's behaviour, giving green tests and a broken system", "Mocking types you do not own (`ResultSet`, `HttpClient`) hides integration problems", "Strict stubs and verification make tests longer to read"],
            "A suite made only of mocks proves your code calls the mocks the way you *think* the real systems behave - bugs live in the gap, so you still need integration tests. `verify` of every call turns the test into a mirror of the code. `when(mock.method(any(), \"x\"))` mixing matchers and raw values throws `InvalidUseOfMatchersException`. Stubbing a method that the code never calls fails under strict stubs - useful feedback, not a nuisance. Mocking value objects, records, `String`, or collections is a smell: use real instances. Mocking `LocalDateTime.now()` through static mocking is brittle; inject a `java.time.Clock` instead.",
            """- Setup: `@ExtendWith(MockitoExtension.class) class OrderServiceTest { @Mock PaymentGateway gateway; @InjectMocks OrderService service; ... }` (constructor injection is attempted first).
- Stubbing: `when(gateway.charge("c1", 500L)).thenReturn(new PaymentResult(true, "p-1"));` / `when(repo.findById("x")).thenReturn(Optional.empty());` / `doThrow(new IllegalStateException("smtp down")).when(mailer).send(any(), any());`
- Consecutive answers: `when(clock.millis()).thenReturn(1L, 2L, 3L);`
- Verification: `verify(gateway).charge("c1", 500L)` (exactly once), `verify(gateway, never()).refund(any())`, `verifyNoInteractions(mailer)`, `InOrder order = inOrder(gateway, inventory); order.verify(gateway).refund("p-1"); order.verify(inventory).release("sku", 2);`.
- Captor: `ArgumentCaptor<String> msg = ArgumentCaptor.forClass(String.class); verify(mailer).send(eq("c1"), msg.capture()); assertThat(msg.getValue()).contains("confirmed");`
- Matchers: all-or-nothing: `verify(m).f(eq("a"), anyInt())` - never `f("a", anyInt())`.
- Prefer **fakes** (in-memory repo) for rich collaborators and **mocks** for outgoing commands (send mail, publish event).
- Inject time: `Clock.fixed(Instant.parse("2026-03-01T00:00:00Z"), ZoneOffset.UTC)`.""",
            [
                ("Tiny — stub and verify", """PaymentGateway gateway = mock(PaymentGateway.class);
when(gateway.charge("c1", 500L)).thenReturn(new PaymentResult(true, "p-1"));

PaymentResult result = gateway.charge("c1", 500L);

assertTrue(result.success());
verify(gateway).charge("c1", 500L);      // exactly once
verifyNoMoreInteractions(gateway);"""),
                ("Tiny — capture an argument and check call order", """ArgumentCaptor<String> message = ArgumentCaptor.forClass(String.class);
service.cancel("c1", "p-1", "sku-9", 2);

InOrder order = inOrder(gateway, inventory);
order.verify(gateway).refund("p-1");               // refund first ...
order.verify(inventory).release("sku-9", 2);        // ... then give the stock back
verify(notifier).send(eq("c1"), message.capture());
assertThat(message.getValue()).contains("cancelled");"""),
                ("Medium — failure injection with strict stubs", """@ExtendWith(MockitoExtension.class)
class CheckoutTest {
    @Mock PaymentGateway gateway;
    @Mock InventoryClient inventory;
    @Mock NotificationSender notifier;
    @InjectMocks OrderService service;          // constructor injection

    @Test
    void gatewayOutageReleasesStockAndReportsFailure() {
        when(inventory.reserve("sku-1", 2)).thenReturn(true);
        when(gateway.charge("c1", 2_000L)).thenThrow(new IllegalStateException("gateway down"));

        OrderService.Outcome outcome = service.placeOrder("c1", "sku-1", 2, 1_000L);

        assertEquals(OrderService.Outcome.PAYMENT_FAILED, outcome);
        verify(inventory).release("sku-1", 2);      // compensation happened
        verify(notifier).send(eq("c1"), contains("failed"));
    }
}"""),
            ],
            [
                ("Mock vs stub vs spy vs fake?", "A stub returns canned data, a mock additionally verifies interactions, a spy wraps a real object, a fake is a simple working implementation (e.g. in-memory repository)."),
                ("Why must matchers be used for all arguments of a call or none?", "Mockito records matchers separately from raw values; mixing them makes argument positions ambiguous, so it throws `InvalidUseOfMatchersException`."),
                ("When should you NOT mock a type?", "Value objects, records, strings and collections, and types you do not own - use real instances or a fake (and an integration test)."),
                ("How do you make code that reads the current time testable?", "Inject a `java.time.Clock` and use `Clock.fixed(...)` in tests."),
            ],
        ),
        sec(
            "TDD, the test pyramid, and JaCoCo coverage",
            "**Test-Driven Development** is the micro-cycle **Red -> Green -> Refactor**: write the smallest failing test (red), write the simplest code that passes it (green, even if ugly), then clean up the design with the safety net of passing tests (refactor). Repeat in steps of minutes. Variants: *classicist/Detroit* (real collaborators, state assertions) vs *mockist/London* (mocks, interaction assertions, outside-in). The **test pyramid** (Mike Cohn) recommends a wide base of **unit tests** (milliseconds, one class, no I/O), a middle layer of **integration tests** (real database via Testcontainers, HTTP slice, Spring context - seconds), and a small top of **end-to-end/UI tests** (minutes, brittle, expensive). Anti-pattern: the **ice-cream cone** (mostly manual/E2E, few unit tests). **JaCoCo** (Java Code Coverage) instruments bytecode through a Java agent: `prepare-agent` attaches it to the `test` phase, `report` writes `target/site/jacoco/index.html` (and `jacoco.xml`/`.csv`). It reports **instruction, line, branch, method, class, and cyclomatic complexity** coverage. **Branch coverage** (each `if`/`switch` outcome taken) is more telling than line coverage. `jacoco:check` can fail the build below a threshold (e.g. `BRANCH COVEREDRATIO >= 0.80`).",
            "TDD gives you executable specifications, small steps, and designs that are easy to test (small, decoupled units). The pyramid gives you a *budget*: cheap tests catch most bugs quickly; expensive tests confirm wiring. Coverage tools answer *what code never ran under test* - a fast way to find forgotten error paths and dead code.",
            ["TDD: immediate feedback, regression net, smaller and more cohesive units, API designed from the caller's view", "Pyramid: fast CI, cheap failures, precise diagnosis", "JaCoCo: objective view of untested branches; integrates with Maven, Gradle, and CI dashboards", "Coverage gates prevent silent erosion of test discipline"],
            ["TDD requires discipline and clear requirements; awkward for exploratory spikes and UI layout", "Heavily mocked pyramids miss wiring bugs; heavy E2E suites are slow and flaky", "**Coverage measures execution, not verification**: a test with no assertions still gives 100% coverage", "Chasing 100% leads to trivial tests (getters) and gaming; thresholds should be per-package and focus on branches"],
            "Skipping the *red* step means you never saw the test fail, so you do not know it can fail (a test that cannot fail is worthless). Skipping *refactor* leaves the first thing that passed. A team with only E2E tests waits an hour for CI and cannot tell which of 200 failures matters. A team that mandates 90% line coverage gets tests like `assertNotNull(new Foo())`. Without coverage at all, an entire `catch` block or an `else if` branch can ship that no test ever executed. Excluding generated code and simple DTOs from coverage (via plugin `<excludes>`) keeps the metric meaningful.",
            """- TDD loop: write a failing test -> run (red, verify the failure message is the one you expect) -> minimal implementation -> run (green) -> refactor -> run again. Commit on green.
- The three laws (Uncle Bob): no production code without a failing test; no more of a test than is sufficient to fail; no more production code than is sufficient to pass.
- Naming: `methodUnderTest_condition_expectedResult` or sentence-style names (`rejectsEmptyExpression`).
- Pyramid targets (rule of thumb): ~70% unit, ~20% integration, ~10% E2E; unit test < 100 ms each.
- JaCoCo Maven wiring: `org.jacoco:jacoco-maven-plugin:0.8.12` with goals `prepare-agent` (before tests) and `report` (bound to `test` or `verify`); open `target/site/jacoco/index.html`.
- Reading the report: green = covered, yellow = partially covered branch (diamond), red = not executed; drill from package to class to source.
- Gate example: `<rule><element>BUNDLE</element><limits><limit><counter>BRANCH</counter><value>COVEREDRATIO</value><minimum>0.80</minimum></limit></limits></rule>` with the `check` goal.
- Exclusions: `<excludes><exclude>**/generated/**</exclude></excludes>`.""",
            [
                ("Tiny — red, green, refactor on one function", """// RED: written first, fails with "cannot find symbol" then with a wrong result
@Test
void addsTwoNumbersInRpn() {
    assertEquals(5, new RpnCalculator(8).evaluate("2 3 +"));
}
// GREEN: simplest thing that passes
//   long evaluate(String s) { return 5; }        <- yes, really, then a second test forces generality
// REFACTOR: introduce a stack, token loop, operator switch - tests stay green"""),
                ("Tiny — what coverage does and does not tell you", """static int sign(int x) {
    if (x > 0) return 1;      // branch 1
    if (x < 0) return -1;     // branch 2
    return 0;                 // fall-through
}

@Test
void covers100PercentOfLinesButNothingIsChecked() {
    sign(5); sign(-5); sign(0);         // every line and branch executed, no assertion!
}"""),
                ("Medium — pom.xml fragment for JaCoCo with a branch-coverage gate", """<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <id>report</id>
      <phase>test</phase>
      <goals><goal>report</goal></goals>
    </execution>
    <execution>
      <id>gate</id>
      <phase>verify</phase>
      <goals><goal>check</goal></goals>
      <configuration>
        <rules>
          <rule>
            <element>BUNDLE</element>
            <limits>
              <limit>
                <counter>BRANCH</counter>
                <value>COVEREDRATIO</value>
                <minimum>0.80</minimum>
              </limit>
            </limits>
          </rule>
        </rules>
      </configuration>
    </execution>
  </executions>
</plugin>"""),
            ],
            [
                ("What is the purpose of seeing the test fail first (red)?", "It proves the test can fail and that it is testing the behaviour you think; a test that never failed may be vacuous."),
                ("Why is branch coverage more informative than line coverage?", "A single line like `a ? b : c` or a compound `if` can be executed while one outcome is never taken; branch coverage tracks each outcome."),
                ("What does the test pyramid recommend?", "Many fast unit tests at the base, fewer integration tests, and very few slow end-to-end tests at the top."),
                ("Can a suite with 100% coverage still miss bugs?", "Yes - coverage shows code was executed, not that results were asserted; missing requirements and wrong assertions are invisible to it."),
            ],
        ),
    ],
    interview=[
        ("Unit vs integration vs end-to-end tests?", "Unit tests exercise one class in isolation (fast, no I/O); integration tests exercise real collaborators like a database or HTTP layer; end-to-end tests drive the whole deployed system. Prefer many unit tests, fewer integration, very few E2E."),
        ("Mock vs stub vs spy vs fake?", "Stub: canned answers. Mock: stub plus interaction verification. Spy: real object with partial stubbing/recording. Fake: simplified working implementation such as an in-memory repository."),
        ("How do you test code that depends on time or randomness?", "Inject the dependency (`Clock`, `Random`/`Supplier`) and use a fixed clock or seeded/fake source in tests; never `Thread.sleep` to wait for time to pass."),
        ("How do you test private methods?", "You don't - test them through the public behaviour that uses them; if a private method is complex enough to need its own tests, extract it into its own class."),
        ("What is TDD and what are its benefits and costs?", "Red-green-refactor: write a failing test, make it pass simply, then refactor. Benefits: design feedback, regression safety, focus. Costs: initial speed, discipline, and tests that need maintenance."),
        ("Is 100% code coverage a good goal?", "No. It is a useful diagnostic for finding untested code, but it measures execution not correctness; aim for meaningful branch coverage on business logic and review gaps instead of chasing a number."),
        ("What are flaky tests and how do you fix them?", "Tests that sometimes pass and sometimes fail without code changes: caused by shared state, ordering, time, concurrency, or external services. Fix by isolating state, injecting clocks, using synchronization primitives instead of sleeps, and faking external systems."),
    ],
    mistakes=[
        "Asserting nothing (coverage without verification) or only `assertNotNull`.",
        "Sharing mutable static state between tests; relying on test execution order.",
        "Using `Thread.sleep` or the real clock in unit tests.",
        "Mocking everything, including value objects; verifying every call so refactoring breaks tests.",
        "Mixing raw values and matchers in one Mockito call.",
        "Committing tests that were never red (they may test nothing).",
        "Treating a coverage percentage as the goal; testing getters to raise the number.",
        "Letting the pyramid invert: slow E2E suites replacing fast unit tests.",
    ],
    reading=[
        "JUnit 5 User Guide (junit.org/junit5/docs/current/user-guide/) - writing tests, parameterized tests, nested tests, extensions",
        "Mockito documentation and Javadoc (javadoc.io/doc/org.mockito/mockito-core) - especially `Mockito` class docs and `MockitoExtension`",
        "AssertJ core documentation (assertj.github.io/doc/)",
        "Kent Beck, *Test-Driven Development: By Example*",
        "Martin Fowler, *The Practical Test Pyramid* (martinfowler.com/articles/practical-test-pyramid.html) and *Mocks Aren't Stubs*",
        "JaCoCo documentation: Maven plugin goals, counters, and report interpretation (jacoco.org/jacoco/trunk/doc/)",
    ],
    glossary=[
        ("SUT", "System under test: the class or unit being verified"),
        ("Test double", "Any stand-in for a real collaborator (dummy, stub, mock, spy, fake)"),
        ("Stub", "Double that returns canned answers"),
        ("Mock", "Double that records interactions so they can be verified"),
        ("Spy", "Wrapper around a real object that records calls"),
        ("Fake", "Simplified but working implementation (in-memory database)"),
        ("Red-Green-Refactor", "The TDD cycle: failing test, passing code, cleanup"),
        ("Test pyramid", "Model: many unit tests, fewer integration, fewest E2E"),
        ("Line coverage", "Share of executable lines run by tests"),
        ("Branch coverage", "Share of decision outcomes (true/false) exercised"),
        ("Flaky test", "Test with nondeterministic pass/fail"),
        ("Strict stubs", "Mockito mode that fails tests with unused stubbings"),
    ],
    tasks=[
        task(
            "parameterized-conversions", "Parameterized Conversions: Roman Numerals and Slugs", "Warm-up", "RomanNumerals",
            "Implement `RomanNumerals` (to/from Roman) and `Slugs.slugify`. The provided test classes demonstrate `@ParameterizedTest` with `@CsvSource`, `@ValueSource`, `@MethodSource`, `@NullAndEmptySource`, and a full round-trip property check - read them to learn the JUnit 5 style you will use for your own tests.",
            [
                "`toRoman(n)` converts 1..3999 to canonical Roman numerals using subtractive notation (`IV`, `IX`, `XL`, `XC`, `CD`, `CM`); outside the range -> `IllegalArgumentException`",
                "`fromRoman(text)` converts canonical numerals back to an int; lower case is accepted; null, blank, invalid characters, or **non-canonical** forms (`IIII`, `VX`, `IC`) -> `IllegalArgumentException`",
                "`Slugs.slugify(text)` lower-cases, strips accents (`Normalizer` NFD + remove combining marks), collapses every run of non-alphanumeric characters into a single `-`, and trims leading/trailing dashes; blank input -> empty string; `null` -> `IllegalArgumentException`",
                "`Slugs.isValidSlug(text)` is true for non-empty strings made of `[a-z0-9]` groups separated by single dashes",
            ],
            ["0, 4000, negative numbers", "non-canonical Roman strings", "accents, emoji, and punctuation only input", "leading/trailing/multiple separators"],
            {"RomanNumerals.java": r'''package @PKG@;

import java.util.Locale;

/** Roman numeral conversion. */
public final class RomanNumerals {

    private static final int[] VALUES = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
    private static final String[] SYMBOLS = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};

    private RomanNumerals() {
    }

    public static String toRoman(int number) {
        //@TODO toRoman | IllegalArgumentException outside 1..3999; greedily subtract the largest VALUES entry and append its SYMBOLS entry
        if (number < 1 || number > 3999) {
            throw new IllegalArgumentException("number out of range 1..3999: " + number);
        }
        StringBuilder sb = new StringBuilder();
        int remaining = number;
        for (int i = 0; i < VALUES.length; i++) {
            while (remaining >= VALUES[i]) {
                sb.append(SYMBOLS[i]);
                remaining -= VALUES[i];
            }
        }
        return sb.toString();
        //@END
    }

    public static int fromRoman(String text) {
        //@TODO fromRoman | null/blank -> IllegalArgumentException; upper-case (Locale.ROOT); parse greedily using SYMBOLS/VALUES; the leftover must be empty and toRoman(result) must equal the input (rejects IIII, VX, IC) otherwise IllegalArgumentException
        if (text == null || text.isBlank()) {
            throw new IllegalArgumentException("empty roman numeral");
        }
        String input = text.trim().toUpperCase(Locale.ROOT);
        int total = 0;
        int index = 0;
        for (int i = 0; i < SYMBOLS.length; i++) {
            while (input.startsWith(SYMBOLS[i], index)) {
                total += VALUES[i];
                index += SYMBOLS[i].length();
                if (total > 3999) {
                    throw new IllegalArgumentException("too large: " + text);
                }
            }
        }
        if (index != input.length() || total == 0 || !toRoman(total).equals(input)) {
            throw new IllegalArgumentException("not a canonical roman numeral: " + text);
        }
        return total;
        //@END
    }
}
''', "Slugs.java": r'''package @PKG@;

import java.text.Normalizer;
import java.util.Locale;
import java.util.regex.Pattern;

/** URL slug helpers. */
public final class Slugs {

    private static final Pattern COMBINING_MARKS = Pattern.compile("\\p{M}+");
    private static final Pattern NON_ALNUM = Pattern.compile("[^a-z0-9]+");
    private static final Pattern VALID = Pattern.compile("[a-z0-9]+(?:-[a-z0-9]+)*");

    private Slugs() {
    }

    public static String slugify(String text) {
        //@TODO slugify | null -> IllegalArgumentException; Normalizer.normalize(NFD), remove COMBINING_MARKS, toLowerCase(Locale.ROOT), replace NON_ALNUM runs with "-", strip leading/trailing "-"
        if (text == null) {
            throw new IllegalArgumentException("text is null");
        }
        String decomposed = Normalizer.normalize(text, Normalizer.Form.NFD);
        String plain = COMBINING_MARKS.matcher(decomposed).replaceAll("").toLowerCase(Locale.ROOT);
        String dashed = NON_ALNUM.matcher(plain).replaceAll("-");
        return dashed.replaceAll("^-+|-+$", "");
        //@END
    }

    public static boolean isValidSlug(String text) {
        //@TODO isValidSlug | true only for non-null text matching VALID (lowercase alphanumerics separated by single dashes)
        return text != null && VALID.matcher(text).matches();
        //@END
    }
}
'''},
            {"RomanNumeralsTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.stream.Stream;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.ValueSource;

@DisplayName("Roman numerals")
class RomanNumeralsTest {

    @ParameterizedTest(name = "{0} -> {1}")
    @CsvSource({"1,I", "2,II", "3,III", "4,IV", "5,V", "9,IX", "10,X", "14,XIV", "40,XL", "49,XLIX", "90,XC",
            "400,CD", "444,CDXLIV", "900,CM", "1994,MCMXCIV", "2024,MMXXIV", "3888,MMMDCCCLXXXVIII", "3999,MMMCMXCIX"})
    void r1_toRoman(int number, String expected) {
        assertEquals(expected, RomanNumerals.toRoman(number));
    }

    @ParameterizedTest
    @ValueSource(ints = {0, -1, -2024, 4000, Integer.MAX_VALUE, Integer.MIN_VALUE})
    void r1_toRomanRejectsOutOfRange(int number) {
        assertThatThrownBy(() -> RomanNumerals.toRoman(number)).isInstanceOf(IllegalArgumentException.class);
    }

    @ParameterizedTest(name = "{0} -> {1}")
    @CsvSource({"I,1", "IV,4", "ix,9", "xiv,14", "MCMXCIV,1994", "MMMCMXCIX,3999", "  XL  ,40"})
    void r2_fromRoman(String text, int expected) {
        assertEquals(expected, RomanNumerals.fromRoman(text));
    }

    @ParameterizedTest
    @ValueSource(strings = {"", " ", "IIII", "VX", "IC", "IIX", "MMMM", "ABC", "XXXX", "VV", "I I", "IXI"})
    void r2_fromRomanRejectsInvalid(String text) {
        assertThatThrownBy(() -> RomanNumerals.fromRoman(text)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r2_fromRomanRejectsNull() {
        assertThatThrownBy(() -> RomanNumerals.fromRoman(null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    @DisplayName("round trip for every supported number")
    void r2_roundTrip() {
        for (int n = 1; n <= 3999; n++) {
            int expected = n;
            String roman = RomanNumerals.toRoman(n);
            int back = RomanNumerals.fromRoman(roman);
            assertAll("n=" + n, () -> assertThat(back).isEqualTo(expected), () -> assertThat(roman).matches("[MDCLXVI]+"));
        }
    }

    static Stream<Arguments> uniqueness() {
        return Stream.of(Arguments.of(1, 2), Arguments.of(4, 6), Arguments.of(1999, 2000), Arguments.of(3998, 3999));
    }

    @ParameterizedTest
    @MethodSource("uniqueness")
    void r2_differentNumbersGiveDifferentNumerals(int a, int b) {
        assertThat(RomanNumerals.toRoman(a)).isNotEqualTo(RomanNumerals.toRoman(b));
    }
}
''', "SlugsTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.NullAndEmptySource;
import org.junit.jupiter.params.provider.ValueSource;

@DisplayName("Slugs")
class SlugsTest {

    @ParameterizedTest(name = "\"{0}\" -> \"{1}\"")
    @CsvSource(delimiter = '|', value = {
            "Hello World|hello-world",
            "  Hello   World  |hello-world",
            "Java 21: Virtual Threads!|java-21-virtual-threads",
            "Crème Brûlée à la façon|creme-brulee-a-la-facon",
            "Ünïcödé Tëst|unicode-test",
            "---already--dashed---|already-dashed",
            "snake_case_and.dots|snake-case-and-dots",
            "ALL CAPS|all-caps",
            "a|a",
            "!!!|",
            "x   |x"
    })
    void r3_slugify(String input, String expected) {
        assertThat(Slugs.slugify(input)).isEqualTo(expected == null ? "" : expected);
    }

    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {"   ", "\t\n"})
    void r3_blankOrEmptyBecomesEmptyExceptNull(String input) {
        if (input == null) {
            assertThatThrownBy(() -> Slugs.slugify(null)).isInstanceOf(IllegalArgumentException.class);
        } else {
            assertThat(Slugs.slugify(input)).isEmpty();
        }
    }

    @Test
    void r3_slugifyIsIdempotent() {
        String once = Slugs.slugify("  Déjà Vu -- Part 2!  ");
        assertThat(once).isEqualTo("deja-vu-part-2");
        assertThat(Slugs.slugify(once)).isEqualTo(once);
    }

    @ParameterizedTest
    @ValueSource(strings = {"a", "abc", "a-b", "hello-world-2", "123", "a1-b2-c3"})
    void r4_validSlugs(String slug) {
        assertThat(Slugs.isValidSlug(slug)).isTrue();
    }

    @ParameterizedTest
    @ValueSource(strings = {"", "-a", "a-", "a--b", "A", "a b", "a_b", "é"})
    void r4_invalidSlugs(String slug) {
        assertThat(Slugs.isValidSlug(slug)).isFalse();
    }

    @Test
    void r4_nullIsNotAValidSlug() {
        assertThat(Slugs.isValidSlug(null)).isFalse();
    }

    @Test
    void r4_everySlugifiedValueIsValidOrEmpty() {
        for (String s : new String[] {"Hello, World!", "Ça va?", "2026-10-16", "Zażółć gęślą jaźń", "   "}) {
            String slug = Slugs.slugify(s);
            assertThat(slug.isEmpty() || Slugs.isValidSlug(slug)).as(s).isTrue();
        }
    }
}
'''},
            ["Roman numerals: loop over parallel `VALUES`/`SYMBOLS` arrays from large to small.", "For `fromRoman`, a cheap way to reject non-canonical input is to convert back with `toRoman` and compare.", "`Normalizer.normalize(text, Normalizer.Form.NFD)` splits `é` into `e` + a combining mark that `\\p{M}` matches."],
            ["Edge cases are handled before the main algorithm", "No duplicated tables (single source of truth for symbols)", "`Locale.ROOT` used for case conversion"],
            constraints=["Use plain Java (`java.text.Normalizer`, `java.util.regex`) - no third-party libraries", "Do not edit the tests; read them as examples of parameterized testing"],
        ),
        task(
            "mockito-order-service", "Mockito: Order Service with Mocked Collaborators", "Core", "OrderService",
            "Implement `OrderService`, an order workflow orchestrating three collaborators (`InventoryClient`, `PaymentGateway`, `NotificationSender`). The tests use **Mockito** to stub outcomes, provoke gateway failures, capture notification messages, and verify call order and absence of interactions.",
            [
                "`placeOrder(customerId, sku, qty, unitPriceCents)` validates `qty > 0` and `unitPriceCents > 0` (otherwise `IllegalArgumentException` with **no** collaborator interaction)",
                "It reserves stock; when `reserve` returns false the outcome is `OUT_OF_STOCK` and **neither payment nor notification** is touched",
                "It charges `qty * unitPriceCents` (as `long`); an unsuccessful `PaymentResult` **or** a `RuntimeException` from the gateway releases the reserved stock, notifies `\"Payment failed: <sku>\"`, and returns `PAYMENT_FAILED`",
                "On success it notifies `\"Order confirmed: <sku> x<qty>\"` and returns `CONFIRMED`; a `RuntimeException` thrown by the notifier is swallowed (the order stays confirmed)",
                "`cancel(customerId, paymentId, sku, qty)` refunds the payment **first**, then releases the stock, then notifies `\"Order cancelled: <sku>\"`",
            ],
            ["reserve returns false", "gateway throws", "gateway declines", "notifier throws after a successful charge", "invalid quantity or price"],
            {"PaymentGateway.java": r'''package @PKG@;

/** Provided collaborator: charges and refunds payments. */
public interface PaymentGateway {

    /** Result of a charge attempt. */
    record PaymentResult(boolean success, String paymentId) {
    }

    PaymentResult charge(String customerId, long amountCents);

    void refund(String paymentId);
}
''', "InventoryClient.java": r'''package @PKG@;

/** Provided collaborator: stock reservation. */
public interface InventoryClient {

    boolean reserve(String sku, int quantity);

    void release(String sku, int quantity);
}
''', "NotificationSender.java": r'''package @PKG@;

/** Provided collaborator: customer notifications. */
public interface NotificationSender {

    void send(String customerId, String message);
}
''', "OrderService.java": r'''package @PKG@;

/** Orchestrates stock, payment, and notification. */
public final class OrderService {

    /** Result of {@link #placeOrder(String, String, int, long)}. */
    public enum Outcome { CONFIRMED, OUT_OF_STOCK, PAYMENT_FAILED }

    private final PaymentGateway payments;
    private final InventoryClient inventory;
    private final NotificationSender notifier;

    public OrderService(PaymentGateway payments, InventoryClient inventory, NotificationSender notifier) {
        this.payments = payments;
        this.inventory = inventory;
        this.notifier = notifier;
    }

    public Outcome placeOrder(String customerId, String sku, int quantity, long unitPriceCents) {
        //@TODO placeOrder | validate qty/price (IAE, no calls); reserve; false -> OUT_OF_STOCK; charge qty*price in try/catch(RuntimeException); failure/decline -> release stock + notify "Payment failed: <sku>" + PAYMENT_FAILED; success -> notify "Order confirmed: <sku> x<qty>" (swallow RuntimeException from notifier) + CONFIRMED
        if (quantity <= 0 || unitPriceCents <= 0) {
            throw new IllegalArgumentException("quantity and price must be positive");
        }
        if (!inventory.reserve(sku, quantity)) {
            return Outcome.OUT_OF_STOCK;
        }
        PaymentGateway.PaymentResult result;
        try {
            result = payments.charge(customerId, (long) quantity * unitPriceCents);
        } catch (RuntimeException e) {
            result = null;
        }
        if (result == null || !result.success()) {
            inventory.release(sku, quantity);
            notifySafely(customerId, "Payment failed: " + sku);
            return Outcome.PAYMENT_FAILED;
        }
        notifySafely(customerId, "Order confirmed: " + sku + " x" + quantity);
        return Outcome.CONFIRMED;
        //@END
    }

    public void cancel(String customerId, String paymentId, String sku, int quantity) {
        //@TODO cancel | payments.refund(paymentId); inventory.release(sku, quantity); notify "Order cancelled: <sku>" (in exactly this order)
        payments.refund(paymentId);
        inventory.release(sku, quantity);
        notifySafely(customerId, "Order cancelled: " + sku);
        //@END
    }

    private void notifySafely(String customerId, String message) {
        try {
            notifier.send(customerId, message);
        } catch (RuntimeException ignored) {
            // notification problems must never undo an order
        }
    }
}
'''},
            {"OrderServiceTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.inOrder;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.verifyNoMoreInteractions;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InOrder;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    PaymentGateway gateway;
    @Mock
    InventoryClient inventory;
    @Mock
    NotificationSender notifier;

    OrderService service;

    @BeforeEach
    void setUp() {
        service = new OrderService(gateway, inventory, notifier);
    }

    @Test
    void r1_invalidInputTouchesNoCollaborator() {
        assertThatThrownBy(() -> service.placeOrder("c1", "sku", 0, 100)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.placeOrder("c1", "sku", -3, 100)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.placeOrder("c1", "sku", 1, 0)).isInstanceOf(IllegalArgumentException.class);
        verifyNoInteractions(gateway, inventory, notifier);
    }

    @Test
    void r2_outOfStockDoesNotChargeOrNotify() {
        when(inventory.reserve("sku-1", 2)).thenReturn(false);

        assertThat(service.placeOrder("c1", "sku-1", 2, 1_000)).isEqualTo(OrderService.Outcome.OUT_OF_STOCK);

        verify(inventory).reserve("sku-1", 2);
        verifyNoMoreInteractions(inventory);
        verifyNoInteractions(gateway, notifier);
    }

    @Test
    void r3_chargesQuantityTimesPriceAndConfirms() {
        when(inventory.reserve("sku-1", 3)).thenReturn(true);
        when(gateway.charge("c1", 3_000_000_000L)).thenReturn(new PaymentGateway.PaymentResult(true, "p-1"));

        assertThat(service.placeOrder("c1", "sku-1", 3, 1_000_000_000L)).isEqualTo(OrderService.Outcome.CONFIRMED);

        ArgumentCaptor<String> message = ArgumentCaptor.forClass(String.class);
        verify(notifier).send(eq("c1"), message.capture());
        assertThat(message.getValue()).isEqualTo("Order confirmed: sku-1 x3");
        verify(inventory, never()).release(anyString(), anyInt());
    }

    @Test
    void r3_declinedPaymentReleasesStockAndNotifies() {
        when(inventory.reserve("sku-1", 2)).thenReturn(true);
        when(gateway.charge("c1", 2_000L)).thenReturn(new PaymentGateway.PaymentResult(false, null));

        assertThat(service.placeOrder("c1", "sku-1", 2, 1_000)).isEqualTo(OrderService.Outcome.PAYMENT_FAILED);

        verify(inventory).release("sku-1", 2);
        verify(notifier).send("c1", "Payment failed: sku-1");
    }

    @Test
    void r3_gatewayOutageIsTreatedAsPaymentFailure() {
        when(inventory.reserve("sku-1", 1)).thenReturn(true);
        when(gateway.charge(anyString(), anyLong())).thenThrow(new IllegalStateException("gateway down"));

        assertThat(service.placeOrder("c1", "sku-1", 1, 500)).isEqualTo(OrderService.Outcome.PAYMENT_FAILED);

        verify(inventory).release("sku-1", 1);
        verify(notifier).send("c1", "Payment failed: sku-1");
        verify(gateway, never()).refund(any());
    }

    @Test
    void r4_notificationFailureDoesNotUndoTheOrder() {
        when(inventory.reserve("sku-1", 1)).thenReturn(true);
        when(gateway.charge("c1", 500L)).thenReturn(new PaymentGateway.PaymentResult(true, "p-9"));
        doThrow(new IllegalStateException("smtp down")).when(notifier).send(anyString(), anyString());

        assertThat(service.placeOrder("c1", "sku-1", 1, 500)).isEqualTo(OrderService.Outcome.CONFIRMED);

        verify(inventory, never()).release(anyString(), anyInt());
        verify(gateway, never()).refund(any());
    }

    @Test
    void r4_stockIsReservedBeforeThePaymentIsTaken() {
        when(inventory.reserve("sku-1", 1)).thenReturn(true);
        when(gateway.charge("c1", 500L)).thenReturn(new PaymentGateway.PaymentResult(true, "p-9"));

        service.placeOrder("c1", "sku-1", 1, 500);

        InOrder order = inOrder(inventory, gateway, notifier);
        order.verify(inventory).reserve("sku-1", 1);
        order.verify(gateway).charge("c1", 500L);
        order.verify(notifier).send(eq("c1"), anyString());
    }

    @Test
    void r5_cancelRefundsThenReleasesThenNotifies() {
        service.cancel("c1", "p-77", "sku-9", 2);

        InOrder order = inOrder(gateway, inventory, notifier);
        order.verify(gateway).refund("p-77");
        order.verify(inventory).release("sku-9", 2);
        order.verify(notifier).send("c1", "Order cancelled: sku-9");
        verifyNoMoreInteractions(gateway, inventory, notifier);
    }
}
'''},
            ["Compute the amount as `(long) quantity * unitPriceCents` so large orders do not overflow `int`.", "Treat a thrown `RuntimeException` from the gateway and a `success == false` result with the same compensation path.", "Wrap the notification in its own try/catch - failing to notify must not roll back a paid order."],
            ["Compensation (release stock) happens on every failure path after reserve", "No collaborator calls on validation failure or out-of-stock", "Order of side effects is deliberate and tested"],
            constraints=["Constructor injection only; no static state; do not catch `Exception`/`Throwable` broadly (only `RuntimeException`)", "Do not edit the tests or the provided interfaces"],
            mockito=True,
        ),
        task(
            "tdd-rpn-calculator", "TDD: Reverse Polish Notation Calculator", "Stretch", "RpnCalculator",
            "Implement a bounded `Stack` and a Reverse Polish Notation (postfix) calculator **the TDD way**: the nested test classes describe the behaviour in the order you would have written them (stack basics -> arithmetic -> error handling). Run the tests, implement just enough for each group, and refactor.",
            [
                "`BoundedStack<T>(capacity)`: `push`, `pop`, `peek`, `size`, `isEmpty`, `capacity`; capacity must be > 0 (`IllegalArgumentException`); `push` on a full stack -> `IllegalStateException(\"stack full\")`; `pop`/`peek` on an empty stack -> `NoSuchElementException`",
                "`RpnCalculator(maxDepth)` evaluates whitespace-separated postfix expressions over `long` values with `+ - * /` (integer division truncating toward zero); `evaluate(\"3 4 + 2 *\")` = 14",
                "Errors: null/blank -> `IllegalArgumentException(\"empty expression\")`; unknown token -> `IllegalArgumentException(\"unknown token: x\")`; missing operands -> `IllegalArgumentException(\"not enough operands\")`; leftover values -> `IllegalArgumentException(\"too many operands\")`; `/` by zero -> `ArithmeticException(\"division by zero\")`; exceeding `maxDepth` -> `IllegalStateException`",
                "Arithmetic overflow is detected with `Math.addExact/subtractExact/multiplyExact` (`ArithmeticException`)",
            ],
            ["single number expression", "negative numbers (`-3` is a number, `-` is an operator)", "very long expressions vs `maxDepth`", "extra whitespace"],
            {"BoundedStack.java": r'''package @PKG@;

import java.util.NoSuchElementException;

/** Fixed-capacity LIFO stack. */
public final class BoundedStack<T> {

    private final Object[] items;
    private int size;

    public BoundedStack(int capacity) {
        //@TODO constructor | capacity <= 0 -> IllegalArgumentException; allocate the backing array
        if (capacity <= 0) {
            throw new IllegalArgumentException("capacity must be > 0");
        }
        this.items = new Object[capacity];
        //@END
    }

    public void push(T item) {
        //@TODO push | when size == capacity throw IllegalStateException("stack full"); otherwise store at items[size++]
        if (size == items.length) {
            throw new IllegalStateException("stack full");
        }
        items[size++] = item;
        //@END
    }

    @SuppressWarnings("unchecked")
    public T pop() {
        //@TODO pop | empty -> NoSuchElementException; otherwise return the top element and clear its slot (avoid keeping a reference)
        if (size == 0) {
            throw new NoSuchElementException("stack empty");
        }
        T top = (T) items[--size];
        items[size] = null;
        return top;
        //@END
    }

    @SuppressWarnings("unchecked")
    public T peek() {
        //@TODO peek | empty -> NoSuchElementException; otherwise return the top element without removing it
        if (size == 0) {
            throw new NoSuchElementException("stack empty");
        }
        return (T) items[size - 1];
        //@END
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public int capacity() {
        return items.length;
    }
}
''', "RpnCalculator.java": r'''package @PKG@;

/** Postfix calculator built on {@link BoundedStack}. */
public final class RpnCalculator {

    private final int maxDepth;

    public RpnCalculator(int maxDepth) {
        this.maxDepth = maxDepth;
    }

    public long evaluate(String expression) {
        //@TODO evaluate | null/blank -> IAE("empty expression"); split on whitespace; numbers (parse long) are pushed on a BoundedStack(maxDepth); + - * / pop right then left, apply (multiplyExact; "/" by zero -> ArithmeticException("division by zero")), push; too few operands -> IAE("not enough operands"); unknown token -> IAE("unknown token: x"); at the end exactly one value must remain else IAE("too many operands")
        if (expression == null || expression.isBlank()) {
            throw new IllegalArgumentException("empty expression");
        }
        BoundedStack<Long> stack = new BoundedStack<>(maxDepth);
        for (String token : expression.trim().split("\\s+")) {
            switch (token) {
                case "+", "-", "*", "/" -> {
                    if (stack.size() < 2) {
                        throw new IllegalArgumentException("not enough operands");
                    }
                    long right = stack.pop();
                    long left = stack.pop();
                    stack.push(apply(token, left, right));
                }
                default -> stack.push(parse(token));
            }
        }
        long result = stack.pop();
        if (!stack.isEmpty()) {
            throw new IllegalArgumentException("too many operands");
        }
        return result;
        //@END
    }

    private static long parse(String token) {
        try {
            return Long.parseLong(token);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("unknown token: " + token);
        }
    }

    private static long apply(String operator, long left, long right) {
        return switch (operator) {
            case "+" -> Math.addExact(left, right);
            case "-" -> Math.subtractExact(left, right);
            case "*" -> Math.multiplyExact(left, right);
            case "/" -> {
                if (right == 0) {
                    throw new ArithmeticException("division by zero");
                }
                yield left / right;
            }
            default -> throw new IllegalArgumentException("unknown token: " + operator);
        };
    }
}
'''},
            {"RpnCalculatorTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.NoSuchElementException;
import java.util.stream.Stream;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.ValueSource;

@DisplayName("RPN calculator, built test-first")
class RpnCalculatorTest {

    @Nested
    @DisplayName("BoundedStack")
    class StackBehaviour {
        private BoundedStack<String> stack;

        @BeforeEach
        void create() {
            stack = new BoundedStack<>(2);
        }

        @Test
        void r1_startsEmpty() {
            assertThat(stack.isEmpty()).isTrue();
            assertThat(stack.size()).isZero();
            assertThat(stack.capacity()).isEqualTo(2);
        }

        @Test
        void r1_isLastInFirstOut() {
            stack.push("a");
            stack.push("b");
            assertThat(stack.peek()).isEqualTo("b");
            assertThat(stack.size()).isEqualTo(2);
            assertThat(stack.pop()).isEqualTo("b");
            assertThat(stack.pop()).isEqualTo("a");
            assertThat(stack.isEmpty()).isTrue();
        }

        @Test
        void r1_rejectsPushWhenFull() {
            stack.push("a");
            stack.push("b");
            assertThatThrownBy(() -> stack.push("c")).isInstanceOf(IllegalStateException.class).hasMessageContaining("stack full");
            assertThat(stack.size()).isEqualTo(2);
        }

        @Test
        void r1_popAndPeekOnEmptyFail() {
            assertThatThrownBy(stack::pop).isInstanceOf(NoSuchElementException.class);
            assertThatThrownBy(stack::peek).isInstanceOf(NoSuchElementException.class);
        }

        @Test
        void r1_slotsAreReusableAfterPop() {
            stack.push("a");
            stack.push("b");
            stack.pop();
            stack.push("c");
            assertThat(stack.pop()).isEqualTo("c");
            assertThat(stack.pop()).isEqualTo("a");
        }

        @ParameterizedTest
        @ValueSource(ints = {0, -1})
        void r1_capacityMustBePositive(int capacity) {
            assertThatThrownBy(() -> new BoundedStack<String>(capacity)).isInstanceOf(IllegalArgumentException.class);
        }
    }

    @Nested
    @DisplayName("evaluate")
    class Arithmetic {
        private final RpnCalculator calculator = new RpnCalculator(16);

        @ParameterizedTest(name = "{0} = {1}")
        @CsvSource(delimiter = '|', value = {
                "42|42", "-7|-7", "2 3 +|5", "10 4 -|6", "6 7 *|42", "20 4 /|5", "7 2 /|3", "-7 2 /|-3",
                "3 4 + 2 *|14", "5 1 2 + 4 * + 3 -|14", "  2   3   +  |5", "2 3 4 * +|14", "100 10 / 5 /|2",
                "0 5 -|-5", "1 2 3 4 5 + + + +|15"
        })
        void r2_evaluates(String expression, long expected) {
            assertThat(calculator.evaluate(expression)).isEqualTo(expected);
        }

        @Test
        void r2_isReusableBetweenEvaluations() {
            assertThat(calculator.evaluate("1 1 +")).isEqualTo(2);
            assertThat(calculator.evaluate("2 2 *")).isEqualTo(4);
        }

        @Test
        void r2_detectsOverflow() {
            assertThatThrownBy(() -> calculator.evaluate("9223372036854775807 2 *")).isInstanceOf(ArithmeticException.class);
            assertThatThrownBy(() -> calculator.evaluate("9223372036854775807 1 +")).isInstanceOf(ArithmeticException.class);
        }
    }

    @Nested
    @DisplayName("errors")
    class Errors {
        private final RpnCalculator calculator = new RpnCalculator(3);

        @ParameterizedTest
        @ValueSource(strings = {"", "   ", "\t"})
        void r3_blankExpression(String expression) {
            assertThatThrownBy(() -> calculator.evaluate(expression)).isInstanceOf(IllegalArgumentException.class).hasMessage("empty expression");
        }

        @Test
        void r3_nullExpression() {
            assertThatThrownBy(() -> calculator.evaluate(null)).isInstanceOf(IllegalArgumentException.class).hasMessage("empty expression");
        }

        static Stream<Arguments> badInputs() {
            return Stream.of(
                    Arguments.of("1 +", IllegalArgumentException.class, "not enough operands"),
                    Arguments.of("+", IllegalArgumentException.class, "not enough operands"),
                    Arguments.of("1 2", IllegalArgumentException.class, "too many operands"),
                    Arguments.of("1 2 3 +", IllegalArgumentException.class, "too many operands"),
                    Arguments.of("1 x +", IllegalArgumentException.class, "unknown token: x"),
                    Arguments.of("2 3 ^", IllegalArgumentException.class, "unknown token: ^"),
                    Arguments.of("1 0 /", ArithmeticException.class, "division by zero"),
                    Arguments.of("1 2 3 4", IllegalStateException.class, "stack full"));
        }

        @ParameterizedTest
        @MethodSource("badInputs")
        void r3_reportsTheProblem(String expression, Class<? extends Throwable> type, String message) {
            assertThatThrownBy(() -> calculator.evaluate(expression)).isInstanceOf(type).hasMessageContaining(message);
        }
    }
}
'''},
            ["Start with the stack tests (small, no dependencies), then the happy-path arithmetic, then errors - exactly the order of the nested classes.", "Treat any token that is not an operator as a number first; a `NumberFormatException` becomes `unknown token`.", "Pop the **right** operand first - it matters for `-` and `/`."],
            ["Messages match the tests; exception types are intentional", "Stack slots cleared on pop (no lingering references)", "No duplicated operator logic"],
            constraints=["Use your `BoundedStack` inside the calculator", "Do not edit the tests"],
        ),
        task(
            "jacoco-loyalty-service", "Coverage Challenge: Loyalty Service with Mockito and a Fixed Clock", "Challenge", "LoyaltyService",
            "Implement a branch-heavy `LoyaltyService` (points earning, tier changes, redemption, expiry). The tests combine **Mockito** (`@Mock` repository, `ArgumentCaptor` for saved customers) with an injected **fixed `Clock`**, and exercise every branch - after the tests are green, open the **JaCoCo** report and confirm your implementation has no uncovered branch.",
            [
                "`earn(customerId, spendCents)`: `spendCents <= 0` -> `IllegalArgumentException`; unknown customer -> `NoSuchElementException(\"unknown customer: <id>\")`; points earned = `spendCents / 100 * tier.multiplier()`; new tier from the new total (`>= 1000` GOLD, `>= 500` SILVER, else BRONZE); `lastActivity` = today (from the injected `Clock`); the updated customer is saved once and returned",
                "`redeem(customerId, points)`: `points <= 0` -> `IllegalArgumentException`; unknown customer -> `NoSuchElementException`; if the customer has been inactive for **more than 365 days** -> `IllegalStateException(\"points expired\")`; not enough points -> `IllegalStateException(\"insufficient points\")`; otherwise deduct, recompute the tier, set `lastActivity` to today, save, return",
                "`expireInactive(ids)`: for each existing customer inactive for more than 365 days **and** holding points > 0, set points to 0 and tier to BRONZE and save; unknown ids and already-empty customers are skipped; returns the number of customers expired",
                "`tierFor(points)` static helper implements the thresholds above",
            ],
            ["exactly 365 days of inactivity (not expired) vs 366", "tier boundaries 499/500/999/1000", "redeeming exactly all points", "unknown ids in `expireInactive`", "customers with zero points"],
            {"CustomerRepository.java": r'''package @PKG@;

import java.util.Optional;

/** Provided collaborator: persistence of customers. */
public interface CustomerRepository {

    Optional<Customer> findById(String id);

    void save(Customer customer);
}
''', "Customer.java": r'''package @PKG@;

import java.time.LocalDate;

/** Provided immutable customer record with its loyalty tier. */
public record Customer(String id, int points, LocalDate lastActivity, Tier tier) {

    /** Loyalty tiers and their earning multipliers. */
    public enum Tier {
        BRONZE(1), SILVER(2), GOLD(3);

        private final int multiplier;

        Tier(int multiplier) {
            this.multiplier = multiplier;
        }

        public int multiplier() {
            return multiplier;
        }
    }
}
''', "LoyaltyService.java": r'''package @PKG@;

import java.time.Clock;
import java.time.LocalDate;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Optional;

/** Loyalty points business rules. */
public final class LoyaltyService {

    static final int INACTIVITY_DAYS = 365;

    private final CustomerRepository repository;
    private final Clock clock;

    public LoyaltyService(CustomerRepository repository, Clock clock) {
        this.repository = repository;
        this.clock = clock;
    }

    public static Customer.Tier tierFor(int points) {
        //@TODO tierFor | >= 1000 GOLD, >= 500 SILVER, otherwise BRONZE
        if (points >= 1000) {
            return Customer.Tier.GOLD;
        }
        if (points >= 500) {
            return Customer.Tier.SILVER;
        }
        return Customer.Tier.BRONZE;
        //@END
    }

    public Customer earn(String customerId, long spendCents) {
        //@TODO earn | spend <= 0 -> IAE; load customer or NoSuchElementException("unknown customer: id"); earned = spend/100 * tier multiplier; save and return a copy with new points, tierFor(newPoints) and lastActivity = LocalDate.now(clock)
        if (spendCents <= 0) {
            throw new IllegalArgumentException("spend must be positive");
        }
        Customer customer = load(customerId);
        int earned = (int) (spendCents / 100 * customer.tier().multiplier());
        int total = customer.points() + earned;
        Customer updated = new Customer(customer.id(), total, LocalDate.now(clock), tierFor(total));
        repository.save(updated);
        return updated;
        //@END
    }

    public Customer redeem(String customerId, int points) {
        //@TODO redeem | points <= 0 -> IAE; load customer; inactive > 365 days -> IllegalStateException("points expired"); points > balance -> IllegalStateException("insufficient points"); save and return the reduced customer with recomputed tier and lastActivity today
        if (points <= 0) {
            throw new IllegalArgumentException("points must be positive");
        }
        Customer customer = load(customerId);
        if (isInactive(customer)) {
            throw new IllegalStateException("points expired");
        }
        if (points > customer.points()) {
            throw new IllegalStateException("insufficient points");
        }
        int remaining = customer.points() - points;
        Customer updated = new Customer(customer.id(), remaining, LocalDate.now(clock), tierFor(remaining));
        repository.save(updated);
        return updated;
        //@END
    }

    public int expireInactive(List<String> customerIds) {
        //@TODO expireInactive | for every id: skip unknown customers, skip customers with 0 points or activity within 365 days; otherwise save points=0/BRONZE (lastActivity unchanged) and count it
        int expired = 0;
        for (String id : customerIds) {
            Optional<Customer> found = repository.findById(id);
            if (found.isEmpty()) {
                continue;
            }
            Customer customer = found.get();
            if (customer.points() > 0 && isInactive(customer)) {
                repository.save(new Customer(customer.id(), 0, customer.lastActivity(), Customer.Tier.BRONZE));
                expired++;
            }
        }
        return expired;
        //@END
    }

    private Customer load(String customerId) {
        return repository.findById(customerId)
                .orElseThrow(() -> new NoSuchElementException("unknown customer: " + customerId));
    }

    private boolean isInactive(Customer customer) {
        return customer.lastActivity().isBefore(LocalDate.now(clock).minusDays(INACTIVITY_DAYS));
    }
}
'''},
            {"LoyaltyServiceTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoMoreInteractions;
import static org.mockito.Mockito.when;

import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class LoyaltyServiceTest {

    private static final Clock CLOCK = Clock.fixed(Instant.parse("2026-03-01T10:00:00Z"), ZoneOffset.UTC);
    private static final LocalDate TODAY = LocalDate.of(2026, 3, 1);

    @Mock
    CustomerRepository repository;
    @Captor
    ArgumentCaptor<Customer> saved;

    LoyaltyService service;

    @BeforeEach
    void setUp() {
        service = new LoyaltyService(repository, CLOCK);
    }

    private static Customer customer(String id, int points, LocalDate last, Customer.Tier tier) {
        return new Customer(id, points, last, tier);
    }

    // ---------------------------------------------------------------- tierFor
    @ParameterizedTest
    @CsvSource({"0,BRONZE", "1,BRONZE", "499,BRONZE", "500,SILVER", "999,SILVER", "1000,GOLD", "50000,GOLD"})
    void r1_tierThresholds(int points, Customer.Tier expected) {
        assertThat(LoyaltyService.tierFor(points)).isEqualTo(expected);
    }

    // ---------------------------------------------------------------- earn
    @Test
    void r2_earnUsesTheTierMultiplierAndUpdatesActivity() {
        when(repository.findById("c1")).thenReturn(Optional.of(customer("c1", 100, TODAY.minusDays(10), Customer.Tier.BRONZE)));

        Customer result = service.earn("c1", 12_345);   // 123 * 1

        assertThat(result.points()).isEqualTo(223);
        assertThat(result.tier()).isEqualTo(Customer.Tier.BRONZE);
        assertThat(result.lastActivity()).isEqualTo(TODAY);
        verify(repository).save(saved.capture());
        assertThat(saved.getValue()).isEqualTo(result);
    }

    @Test
    void r2_goldEarnsTripleAndSilverDouble() {
        when(repository.findById("gold")).thenReturn(Optional.of(customer("gold", 1_000, TODAY, Customer.Tier.GOLD)));
        when(repository.findById("silver")).thenReturn(Optional.of(customer("silver", 500, TODAY, Customer.Tier.SILVER)));

        assertThat(service.earn("gold", 5_000).points()).isEqualTo(1_150);     // 50 * 3
        assertThat(service.earn("silver", 5_099).points()).isEqualTo(600);     // 50 * 2 (cents below 100 ignored)
    }

    @Test
    void r2_earnPromotesAcrossTierBoundaries() {
        when(repository.findById("a")).thenReturn(Optional.of(customer("a", 499, TODAY, Customer.Tier.BRONZE)));
        when(repository.findById("b")).thenReturn(Optional.of(customer("b", 998, TODAY, Customer.Tier.SILVER)));
        when(repository.findById("c")).thenReturn(Optional.of(customer("c", 0, TODAY, Customer.Tier.BRONZE)));

        assertThat(service.earn("a", 100).tier()).isEqualTo(Customer.Tier.SILVER);   // 500
        assertThat(service.earn("b", 100).tier()).isEqualTo(Customer.Tier.GOLD);     // 998 + 2 = 1000
        assertThat(service.earn("c", 99).points()).as("less than one whole currency unit").isZero();
    }

    @Test
    void r2_earnRejectsInvalidInput() {
        assertThatThrownBy(() -> service.earn("c1", 0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.earn("c1", -5)).isInstanceOf(IllegalArgumentException.class);
        when(repository.findById("ghost")).thenReturn(Optional.empty());
        assertThatThrownBy(() -> service.earn("ghost", 100))
                .isInstanceOf(NoSuchElementException.class)
                .hasMessage("unknown customer: ghost");
        verify(repository, never()).save(any());
    }

    // ---------------------------------------------------------------- redeem
    @Test
    void r3_redeemDeductsAndRecomputesTier() {
        when(repository.findById("c1")).thenReturn(Optional.of(customer("c1", 1_200, TODAY.minusDays(30), Customer.Tier.GOLD)));

        Customer result = service.redeem("c1", 300);

        assertThat(result.points()).isEqualTo(900);
        assertThat(result.tier()).isEqualTo(Customer.Tier.SILVER);
        assertThat(result.lastActivity()).isEqualTo(TODAY);
        verify(repository).save(saved.capture());
        assertThat(saved.getValue()).isEqualTo(result);
    }

    @Test
    void r3_redeemAllPointsIsAllowed() {
        when(repository.findById("c1")).thenReturn(Optional.of(customer("c1", 50, TODAY, Customer.Tier.BRONZE)));
        assertThat(service.redeem("c1", 50).points()).isZero();
    }

    @Test
    void r3_redeemMoreThanBalanceFails() {
        when(repository.findById("c1")).thenReturn(Optional.of(customer("c1", 50, TODAY, Customer.Tier.BRONZE)));
        assertThatThrownBy(() -> service.redeem("c1", 51))
                .isInstanceOf(IllegalStateException.class)
                .hasMessage("insufficient points");
        verify(repository, never()).save(any());
    }

    @Test
    void r3_exactly365DaysInactiveIsStillValidButOneMoreDayExpires() {
        when(repository.findById("edge")).thenReturn(Optional.of(customer("edge", 100, TODAY.minusDays(365), Customer.Tier.BRONZE)));
        when(repository.findById("old")).thenReturn(Optional.of(customer("old", 100, TODAY.minusDays(366), Customer.Tier.BRONZE)));

        assertThat(service.redeem("edge", 10).points()).isEqualTo(90);
        assertThatThrownBy(() -> service.redeem("old", 10))
                .isInstanceOf(IllegalStateException.class)
                .hasMessage("points expired");
        verify(repository, times(1)).save(any());
    }

    @Test
    void r3_redeemRejectsInvalidInput() {
        assertThatThrownBy(() -> service.redeem("c1", 0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.redeem("c1", -1)).isInstanceOf(IllegalArgumentException.class);
        when(repository.findById("ghost")).thenReturn(Optional.empty());
        assertThatThrownBy(() -> service.redeem("ghost", 5)).isInstanceOf(NoSuchElementException.class);
    }

    // ---------------------------------------------------------------- expireInactive
    @Test
    void r4_expireInactiveResetsOnlyStaleCustomersWithPoints() {
        LocalDate stale = TODAY.minusDays(400);
        when(repository.findById("stale-1")).thenReturn(Optional.of(customer("stale-1", 700, stale, Customer.Tier.SILVER)));
        when(repository.findById("stale-0")).thenReturn(Optional.of(customer("stale-0", 0, stale, Customer.Tier.BRONZE)));
        when(repository.findById("fresh")).thenReturn(Optional.of(customer("fresh", 900, TODAY.minusDays(365), Customer.Tier.SILVER)));
        when(repository.findById("missing")).thenReturn(Optional.empty());

        int expired = service.expireInactive(List.of("stale-1", "stale-0", "fresh", "missing"));

        assertThat(expired).isEqualTo(1);
        verify(repository).save(saved.capture());
        assertThat(saved.getValue()).isEqualTo(customer("stale-1", 0, stale, Customer.Tier.BRONZE));
        verify(repository, times(4)).findById(any());
        verifyNoMoreInteractions(repository);
    }

    @Test
    void r4_expireInactiveWithNoIdsDoesNothing() {
        assertThat(service.expireInactive(List.of())).isZero();
        verifyNoMoreInteractions(repository);
    }
}
'''},
            ["Keep the 365-day rule in one private helper so `redeem` and `expireInactive` agree on the boundary (`isBefore(today.minusDays(365))`).", "`LocalDate.now(clock)` makes time injectable - never call `LocalDate.now()` without the clock.", "After green: `mvn test`, then open `target/site/jacoco/index.html` and look for yellow/red diamonds."],
            ["Every branch of your implementation is exercised by the provided tests (JaCoCo branch coverage 100% on `LoyaltyService`)", "No hidden time dependency (`LocalDate.now()` without a clock)", "Repository is saved exactly when state changes"],
            constraints=["Use the injected `Clock`; no `LocalDate.now()` without it", "Do not edit the tests or the provided types"],
            mockito=True,
        ),
    ],
)
