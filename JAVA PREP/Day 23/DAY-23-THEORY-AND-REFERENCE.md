# Day 23 — Testing in Depth: JUnit 5, Parameterized Tests, Mockito, TDD, the Test Pyramid, and JaCoCo

**Phase:** Core Java  
**Primary theme:** Write fast, trustworthy tests: master JUnit 5 features, isolate collaborators with Mockito, drive design with TDD, balance the test pyramid, and measure coverage with JaCoCo.  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-parameterized-conversions`, `task-02-mockito-order-service`, `task-03-tdd-rpn-calculator`, `task-04-jacoco-loyalty-service`  
**Instruction alignment:** Maps to the Day 23 entry of the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21 (no Spring today)

## Overview

Every day so far, a JUnit 5 test class told you whether your solution was right. Today you learn to **write** those tests. Good tests are *fast* (milliseconds), *independent* (any order, any machine), *repeatable* (no clock/network randomness), *self-validating* (pass/fail, no eyeballing logs), and *timely* (written with or before the code) - the **F.I.R.S.T.** principles.

**JUnit 5** is the platform (`junit-platform`), the programming model (`junit-jupiter`), and the legacy bridge (`vintage`). **Parameterized tests** remove copy-paste by running one test body against many inputs. **Mockito** replaces slow or non-deterministic collaborators (payment gateways, mail servers, clocks) with test doubles so you can verify *interactions*. **TDD** (red -> green -> refactor) uses tests as a design tool: the first failing test forces you to design the API from the caller's side. The **test pyramid** tells you where to invest: many fast unit tests, fewer integration tests, very few end-to-end tests. **JaCoCo** shows which lines and branches your tests actually executed - a map of what is *not* tested, not a certificate of quality. Interviews ask: *unit vs integration test*, *mock vs stub vs spy vs fake*, *what does 100% coverage prove (nothing)*, *how do you test time or randomness*, *how do you test private methods (you don't)*.

## Day roadmap

1. JUnit 5: lifecycle, assertions, nested and parameterized tests
2. Mockito and test doubles: mock, stub, spy, fake
3. TDD, the test pyramid, and JaCoCo coverage
4. Interview angles
5. Common mistakes & debugging
6. Further reading, glossary, answers

### JUnit 5: lifecycle, assertions, nested and parameterized tests

#### What it is

JUnit 5 test classes are plain classes; any method annotated **`@Test`** runs, with a **new instance per test method** (default lifecycle) so state cannot leak between tests. Lifecycle hooks: `@BeforeAll` (static, once), `@BeforeEach`, `@AfterEach`, `@AfterAll`. Organize with **`@Nested`** inner classes (grouping by scenario, sharing the outer `@BeforeEach`) and **`@DisplayName`** for readable reports. Assertions: `assertEquals`, `assertTrue`, `assertThrows` (returns the exception for further checks), `assertAll` (reports *all* failures instead of the first), `assertTimeout`, and **AssertJ** (`assertThat(actual).isEqualTo(...)`, rich fluent matchers: `containsExactly`, `extracting`, `hasMessageContaining`, `assertThatThrownBy`). Controls: `@Disabled`, `@Tag`, `@Timeout`, `@RepeatedTest`, `@TempDir` (injects a fresh temporary directory), `Assumptions.assumeTrue`. **Parameterized tests** (`junit-jupiter-params`): `@ParameterizedTest` plus a source - `@ValueSource(ints/strings...)`, `@CsvSource({"1,I", "4,IV"})`, `@MethodSource("cases")` (a static `Stream<Arguments>`), `@EnumSource`, `@NullSource`, `@EmptySource`, `@NullAndEmptySource`; customize names with `name = "{0} -> {1}"`.

#### Why it exists / why it matters

Tests are executable documentation and a safety net for refactoring. Parameterized tests make the *table of examples* the specification, so adding a case is one line, and nested classes make the structure mirror the behaviour ("when stack is empty ...", "when stack is full ..."). Using a fresh instance per test removes the largest cause of flaky suites: shared mutable state.

#### Pros and cons

**Pros**

- Fast feedback and a safety net for refactoring
- Clear, declarative test tables with parameterized tests
- Fresh instance per test isolates state; `@Nested` documents scenarios
- Extension model (`@ExtendWith`) powers Mockito, Spring, and custom behaviour

**Cons / tradeoffs**

- Over-specified tests break on harmless refactors (testing implementation, not behaviour)
- Large parameter tables can hide *why* a case exists - name them
- Slow tests (I/O, sleeps) erode the habit of running them
- Assertions on exception messages are brittle

#### What happens without it / when misused

Without isolation, tests pass alone and fail together (static state, shared files, ordering). Without parameterization, edge cases are copy-pasted and quietly diverge. Assertions that only check *no exception was thrown* give false confidence. `Thread.sleep` in tests creates flakiness: prefer latches, `Awaitility`, or injected clocks. A test that asserts internal calls (`verify` everything) rather than outcomes pins the implementation and makes refactoring painful. Tests that depend on `HashMap` iteration order, the system clock, time zone, or locale fail randomly on another machine.

#### Syntax and rules

- Structure: **Arrange - Act - Assert** (a.k.a. Given - When - Then); one logical behaviour per test; name tests by behaviour (`rejectsNegativeAmount`).
- `@Test void name() { ... }` - package-private is fine in Jupiter.
- Exceptions: `assertThrows(IllegalArgumentException.class, () -> f(-1))` or `assertThatThrownBy(() -> f(-1)).isInstanceOf(IAE.class).hasMessageContaining("negative")`.
- Grouped failures: `assertAll("fields", () -> assertEquals(..), () -> assertEquals(..))`.
- Parameterized: `@ParameterizedTest(name = "{0} -> {1}") @CsvSource({"1,I", "4,IV"}) void toRoman(int n, String expected) { ... }`; complex objects via `@MethodSource("cases")` returning `Stream<Arguments>`; `@NullSource` / `@EmptySource` for edge inputs.
- Nested: `@Nested class WhenEmpty { @BeforeEach void setUp() {...} @Test void ... }` (inner class, not static).
- Temp files: `void writes(@TempDir Path dir) { Files.writeString(dir.resolve("a.txt"), "x"); }`.
- Run: `mvn test`, one class `mvn -Dtest=MyTest test`, one method `mvn -Dtest=MyTest#name test`.

#### Examples

**Example 1.1 — Tiny — assertThrows and assertAll**

```java
@Test
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
}
```

**Example 1.2 — Tiny — one body, many rows**

```java
@ParameterizedTest(name = "{0} -> {1}")
@CsvSource({"1,I", "4,IV", "9,IX", "14,XIV", "1994,MCMXCIV"})
void toRoman(int number, String expected) {
    assertEquals(expected, RomanNumerals.toRoman(number));
}

@ParameterizedTest
@ValueSource(ints = {0, -1, 4000})
void toRomanRejectsOutOfRange(int number) {
    assertThrows(IllegalArgumentException.class, () -> RomanNumerals.toRoman(number));
}
```

**Example 1.3 — Medium — nested scenarios with a shared fixture**

```java
import static org.junit.jupiter.api.Assertions.*;

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
}
```

#### Quick checks

1. Why does JUnit 5 create a new test-class instance for every test method?
2. What does `assertAll` give you over several plain assertions?
3. Name three argument sources for `@ParameterizedTest`.
4. How do you test that a method throws and inspect the exception?

### Mockito and test doubles: mock, stub, spy, fake

#### What it is

A **test double** stands in for a real collaborator. Gerard Meszaros' taxonomy: a **dummy** fills a parameter list; a **stub** returns canned answers; a **mock** records interactions so the test can *verify* them; a **spy** wraps a real object and records calls; a **fake** is a lightweight working implementation (in-memory repository). **Mockito** creates mocks of interfaces and classes at runtime. `@ExtendWith(MockitoExtension.class)` initialises `@Mock`, `@Spy`, `@Captor`, and `@InjectMocks` fields and enables **strict stubs** (unused stubbings fail the test). Stub with `when(repo.find(1)).thenReturn(Optional.of(x))`, `thenThrow(...)`, `thenAnswer(inv -> ...)`; for `void` methods use `doThrow(...).when(mock).method()`. Verify with `verify(mock).send("a")`, `verify(mock, times(2))`, `never()`, `atLeastOnce()`, `verifyNoInteractions(mock)`, `verifyNoMoreInteractions(mock)`, `inOrder(a, b).verify(...)`. **Argument matchers** (`any()`, `eq()`, `anyString()`, `argThat(...)`) must be used for *all* arguments of a call or none; **`ArgumentCaptor`** captures what was passed so you can assert on it. Mockito 5 uses the *inline* mock maker by default, so final classes and static methods (`mockStatic`) can be mocked, but you rarely should.

#### Why it exists / why it matters

Unit tests must be fast and deterministic, but real code talks to databases, payment providers, mail servers, and clocks. Test doubles let you (a) make the collaborator behave in ways that are hard to provoke (timeouts, declined payments), (b) assert that the right side effects happened (email sent exactly once, refund before restock), and (c) keep tests in-memory and parallelizable. Mocking at a **boundary you own** (an interface your code defines) also pushes you toward cleaner designs with injected dependencies.

#### Pros and cons

**Pros**

- Isolates the unit under test from slow or flaky dependencies
- Lets you provoke failures (exceptions, timeouts) on demand
- Verifies interactions that have no return value (events, notifications)
- Works great with constructor injection and small interfaces

**Cons / tradeoffs**

- Over-mocking couples tests to implementation details; refactors break tests that still describe correct behaviour
- A mock can disagree with the real collaborator's behaviour, giving green tests and a broken system
- Mocking types you do not own (`ResultSet`, `HttpClient`) hides integration problems
- Strict stubs and verification make tests longer to read

#### What happens without it / when misused

A suite made only of mocks proves your code calls the mocks the way you *think* the real systems behave - bugs live in the gap, so you still need integration tests. `verify` of every call turns the test into a mirror of the code. `when(mock.method(any(), "x"))` mixing matchers and raw values throws `InvalidUseOfMatchersException`. Stubbing a method that the code never calls fails under strict stubs - useful feedback, not a nuisance. Mocking value objects, records, `String`, or collections is a smell: use real instances. Mocking `LocalDateTime.now()` through static mocking is brittle; inject a `java.time.Clock` instead.

#### Syntax and rules

- Setup: `@ExtendWith(MockitoExtension.class) class OrderServiceTest { @Mock PaymentGateway gateway; @InjectMocks OrderService service; ... }` (constructor injection is attempted first).
- Stubbing: `when(gateway.charge("c1", 500L)).thenReturn(new PaymentResult(true, "p-1"));` / `when(repo.findById("x")).thenReturn(Optional.empty());` / `doThrow(new IllegalStateException("smtp down")).when(mailer).send(any(), any());`
- Consecutive answers: `when(clock.millis()).thenReturn(1L, 2L, 3L);`
- Verification: `verify(gateway).charge("c1", 500L)` (exactly once), `verify(gateway, never()).refund(any())`, `verifyNoInteractions(mailer)`, `InOrder order = inOrder(gateway, inventory); order.verify(gateway).refund("p-1"); order.verify(inventory).release("sku", 2);`.
- Captor: `ArgumentCaptor<String> msg = ArgumentCaptor.forClass(String.class); verify(mailer).send(eq("c1"), msg.capture()); assertThat(msg.getValue()).contains("confirmed");`
- Matchers: all-or-nothing: `verify(m).f(eq("a"), anyInt())` - never `f("a", anyInt())`.
- Prefer **fakes** (in-memory repo) for rich collaborators and **mocks** for outgoing commands (send mail, publish event).
- Inject time: `Clock.fixed(Instant.parse("2026-03-01T00:00:00Z"), ZoneOffset.UTC)`.

#### Examples

**Example 2.1 — Tiny — stub and verify**

```java
PaymentGateway gateway = mock(PaymentGateway.class);
when(gateway.charge("c1", 500L)).thenReturn(new PaymentResult(true, "p-1"));

PaymentResult result = gateway.charge("c1", 500L);

assertTrue(result.success());
verify(gateway).charge("c1", 500L);      // exactly once
verifyNoMoreInteractions(gateway);
```

**Example 2.2 — Tiny — capture an argument and check call order**

```java
ArgumentCaptor<String> message = ArgumentCaptor.forClass(String.class);
service.cancel("c1", "p-1", "sku-9", 2);

InOrder order = inOrder(gateway, inventory);
order.verify(gateway).refund("p-1");               // refund first ...
order.verify(inventory).release("sku-9", 2);        // ... then give the stock back
verify(notifier).send(eq("c1"), message.capture());
assertThat(message.getValue()).contains("cancelled");
```

**Example 2.3 — Medium — failure injection with strict stubs**

```java
@ExtendWith(MockitoExtension.class)
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
}
```

#### Quick checks

1. Mock vs stub vs spy vs fake?
2. Why must matchers be used for all arguments of a call or none?
3. When should you NOT mock a type?
4. How do you make code that reads the current time testable?

### TDD, the test pyramid, and JaCoCo coverage

#### What it is

**Test-Driven Development** is the micro-cycle **Red -> Green -> Refactor**: write the smallest failing test (red), write the simplest code that passes it (green, even if ugly), then clean up the design with the safety net of passing tests (refactor). Repeat in steps of minutes. Variants: *classicist/Detroit* (real collaborators, state assertions) vs *mockist/London* (mocks, interaction assertions, outside-in). The **test pyramid** (Mike Cohn) recommends a wide base of **unit tests** (milliseconds, one class, no I/O), a middle layer of **integration tests** (real database via Testcontainers, HTTP slice, Spring context - seconds), and a small top of **end-to-end/UI tests** (minutes, brittle, expensive). Anti-pattern: the **ice-cream cone** (mostly manual/E2E, few unit tests). **JaCoCo** (Java Code Coverage) instruments bytecode through a Java agent: `prepare-agent` attaches it to the `test` phase, `report` writes `target/site/jacoco/index.html` (and `jacoco.xml`/`.csv`). It reports **instruction, line, branch, method, class, and cyclomatic complexity** coverage. **Branch coverage** (each `if`/`switch` outcome taken) is more telling than line coverage. `jacoco:check` can fail the build below a threshold (e.g. `BRANCH COVEREDRATIO >= 0.80`).

#### Why it exists / why it matters

TDD gives you executable specifications, small steps, and designs that are easy to test (small, decoupled units). The pyramid gives you a *budget*: cheap tests catch most bugs quickly; expensive tests confirm wiring. Coverage tools answer *what code never ran under test* - a fast way to find forgotten error paths and dead code.

#### Pros and cons

**Pros**

- TDD: immediate feedback, regression net, smaller and more cohesive units, API designed from the caller's view
- Pyramid: fast CI, cheap failures, precise diagnosis
- JaCoCo: objective view of untested branches; integrates with Maven, Gradle, and CI dashboards
- Coverage gates prevent silent erosion of test discipline

**Cons / tradeoffs**

- TDD requires discipline and clear requirements; awkward for exploratory spikes and UI layout
- Heavily mocked pyramids miss wiring bugs; heavy E2E suites are slow and flaky
- **Coverage measures execution, not verification**: a test with no assertions still gives 100% coverage
- Chasing 100% leads to trivial tests (getters) and gaming; thresholds should be per-package and focus on branches

#### What happens without it / when misused

Skipping the *red* step means you never saw the test fail, so you do not know it can fail (a test that cannot fail is worthless). Skipping *refactor* leaves the first thing that passed. A team with only E2E tests waits an hour for CI and cannot tell which of 200 failures matters. A team that mandates 90% line coverage gets tests like `assertNotNull(new Foo())`. Without coverage at all, an entire `catch` block or an `else if` branch can ship that no test ever executed. Excluding generated code and simple DTOs from coverage (via plugin `<excludes>`) keeps the metric meaningful.

#### Syntax and rules

- TDD loop: write a failing test -> run (red, verify the failure message is the one you expect) -> minimal implementation -> run (green) -> refactor -> run again. Commit on green.
- The three laws (Uncle Bob): no production code without a failing test; no more of a test than is sufficient to fail; no more production code than is sufficient to pass.
- Naming: `methodUnderTest_condition_expectedResult` or sentence-style names (`rejectsEmptyExpression`).
- Pyramid targets (rule of thumb): ~70% unit, ~20% integration, ~10% E2E; unit test < 100 ms each.
- JaCoCo Maven wiring: `org.jacoco:jacoco-maven-plugin:0.8.12` with goals `prepare-agent` (before tests) and `report` (bound to `test` or `verify`); open `target/site/jacoco/index.html`.
- Reading the report: green = covered, yellow = partially covered branch (diamond), red = not executed; drill from package to class to source.
- Gate example: `<rule><element>BUNDLE</element><limits><limit><counter>BRANCH</counter><value>COVEREDRATIO</value><minimum>0.80</minimum></limit></limits></rule>` with the `check` goal.
- Exclusions: `<excludes><exclude>**/generated/**</exclude></excludes>`.

#### Examples

**Example 3.1 — Tiny — red, green, refactor on one function**

```java
// RED: written first, fails with "cannot find symbol" then with a wrong result
@Test
void addsTwoNumbersInRpn() {
    assertEquals(5, new RpnCalculator(8).evaluate("2 3 +"));
}
// GREEN: simplest thing that passes
//   long evaluate(String s) { return 5; }        <- yes, really, then a second test forces generality
// REFACTOR: introduce a stack, token loop, operator switch - tests stay green
```

**Example 3.2 — Tiny — what coverage does and does not tell you**

```java
static int sign(int x) {
    if (x > 0) return 1;      // branch 1
    if (x < 0) return -1;     // branch 2
    return 0;                 // fall-through
}

@Test
void covers100PercentOfLinesButNothingIsChecked() {
    sign(5); sign(-5); sign(0);         // every line and branch executed, no assertion!
}
```

**Example 3.3 — Medium — pom.xml fragment for JaCoCo with a branch-coverage gate**

```java
<plugin>
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
</plugin>
```

#### Quick checks

1. What is the purpose of seeing the test fail first (red)?
2. Why is branch coverage more informative than line coverage?
3. What does the test pyramid recommend?
4. Can a suite with 100% coverage still miss bugs?

## Interview angles

**Q: Unit vs integration vs end-to-end tests?**

Unit tests exercise one class in isolation (fast, no I/O); integration tests exercise real collaborators like a database or HTTP layer; end-to-end tests drive the whole deployed system. Prefer many unit tests, fewer integration, very few E2E.

**Q: Mock vs stub vs spy vs fake?**

Stub: canned answers. Mock: stub plus interaction verification. Spy: real object with partial stubbing/recording. Fake: simplified working implementation such as an in-memory repository.

**Q: How do you test code that depends on time or randomness?**

Inject the dependency (`Clock`, `Random`/`Supplier`) and use a fixed clock or seeded/fake source in tests; never `Thread.sleep` to wait for time to pass.

**Q: How do you test private methods?**

You don't - test them through the public behaviour that uses them; if a private method is complex enough to need its own tests, extract it into its own class.

**Q: What is TDD and what are its benefits and costs?**

Red-green-refactor: write a failing test, make it pass simply, then refactor. Benefits: design feedback, regression safety, focus. Costs: initial speed, discipline, and tests that need maintenance.

**Q: Is 100% code coverage a good goal?**

No. It is a useful diagnostic for finding untested code, but it measures execution not correctness; aim for meaningful branch coverage on business logic and review gaps instead of chasing a number.

**Q: What are flaky tests and how do you fix them?**

Tests that sometimes pass and sometimes fail without code changes: caused by shared state, ordering, time, concurrency, or external services. Fix by isolating state, injecting clocks, using synchronization primitives instead of sleeps, and faking external systems.

## Common mistakes & debugging

- Asserting nothing (coverage without verification) or only `assertNotNull`.
- Sharing mutable static state between tests; relying on test execution order.
- Using `Thread.sleep` or the real clock in unit tests.
- Mocking everything, including value objects; verifying every call so refactoring breaks tests.
- Mixing raw values and matchers in one Mockito call.
- Committing tests that were never red (they may test nothing).
- Treating a coverage percentage as the goal; testing getters to raise the number.
- Letting the pyramid invert: slow E2E suites replacing fast unit tests.

## Further reading

- JUnit 5 User Guide (junit.org/junit5/docs/current/user-guide/) - writing tests, parameterized tests, nested tests, extensions
- Mockito documentation and Javadoc (javadoc.io/doc/org.mockito/mockito-core) - especially `Mockito` class docs and `MockitoExtension`
- AssertJ core documentation (assertj.github.io/doc/)
- Kent Beck, *Test-Driven Development: By Example*
- Martin Fowler, *The Practical Test Pyramid* (martinfowler.com/articles/practical-test-pyramid.html) and *Mocks Aren't Stubs*
- JaCoCo documentation: Maven plugin goals, counters, and report interpretation (jacoco.org/jacoco/trunk/doc/)

## Glossary

| Term | Meaning |
|------|---------|
| SUT | System under test: the class or unit being verified |
| Test double | Any stand-in for a real collaborator (dummy, stub, mock, spy, fake) |
| Stub | Double that returns canned answers |
| Mock | Double that records interactions so they can be verified |
| Spy | Wrapper around a real object that records calls |
| Fake | Simplified but working implementation (in-memory database) |
| Red-Green-Refactor | The TDD cycle: failing test, passing code, cleanup |
| Test pyramid | Model: many unit tests, fewer integration, fewest E2E |
| Line coverage | Share of executable lines run by tests |
| Branch coverage | Share of decision outcomes (true/false) exercised |
| Flaky test | Test with nondeterministic pass/fail |
| Strict stubs | Mockito mode that fails tests with unused stubbings |

## Answers

Answers to every **Quick check** above (numbered `section.question`).

- **1.1** — Why does JUnit 5 create a new test-class instance for every test method?  
  To isolate tests: instance fields set by one test cannot leak into another (the default `Lifecycle.PER_METHOD`).

- **1.2** — What does `assertAll` give you over several plain assertions?  
  It runs every assertion and reports all failures together instead of stopping at the first one.

- **1.3** — Name three argument sources for `@ParameterizedTest`.  
  `@ValueSource`, `@CsvSource`, `@MethodSource` (also `@EnumSource`, `@NullSource`, `@EmptySource`).

- **1.4** — How do you test that a method throws and inspect the exception?  
  `assertThrows(Type.class, executable)` returns the exception; or AssertJ `assertThatThrownBy(...)`.

- **2.1** — Mock vs stub vs spy vs fake?  
  A stub returns canned data, a mock additionally verifies interactions, a spy wraps a real object, a fake is a simple working implementation (e.g. in-memory repository).

- **2.2** — Why must matchers be used for all arguments of a call or none?  
  Mockito records matchers separately from raw values; mixing them makes argument positions ambiguous, so it throws `InvalidUseOfMatchersException`.

- **2.3** — When should you NOT mock a type?  
  Value objects, records, strings and collections, and types you do not own - use real instances or a fake (and an integration test).

- **2.4** — How do you make code that reads the current time testable?  
  Inject a `java.time.Clock` and use `Clock.fixed(...)` in tests.

- **3.1** — What is the purpose of seeing the test fail first (red)?  
  It proves the test can fail and that it is testing the behaviour you think; a test that never failed may be vacuous.

- **3.2** — Why is branch coverage more informative than line coverage?  
  A single line like `a ? b : c` or a compound `if` can be executed while one outcome is never taken; branch coverage tracks each outcome.

- **3.3** — What does the test pyramid recommend?  
  Many fast unit tests at the base, fewer integration tests, and very few slow end-to-end tests at the top.

- **3.4** — Can a suite with 100% coverage still miss bugs?  
  Yes - coverage shows code was executed, not that results were asserted; missing requirements and wrong assertions are invisible to it.
