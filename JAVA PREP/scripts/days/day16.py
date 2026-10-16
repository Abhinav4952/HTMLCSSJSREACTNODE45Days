from gen_helpers import sec, task

DAY = dict(
    num=16,
    title="Lambdas, Functional Interfaces, Method References, and Optional",
    theme="Pass behavior as data: lambdas, `java.util.function`, method references, and `Optional` for absent values.",
    objectives=[
        "Write lambda expressions and explain what a functional interface (SAM type) is",
        "Use the core `java.util.function` types: `Predicate`, `Function`, `Supplier`, `Consumer`, `UnaryOperator`, `BiFunction`, and primitive specializations",
        "Explain variable capture and the *effectively final* rule, including the loop-variable pitfall",
        "Choose among the four kinds of method references and rewrite lambdas as method references",
        "Compose behavior with `andThen`, `compose`, `and`, `or`, `negate`",
        "Use `Optional` correctly (`map`, `flatMap`, `orElseGet`, `orElseThrow`) and avoid its misuses",
    ],
    prereqs=["Day 13 — generics (`Function<? super T, ? extends R>`)", "Day 14–15 — collections and comparators", "Day 10 — interfaces and anonymous classes"],
    overview="""Java 8 introduced lambdas so that *behavior* can be passed to methods as a value. That one idea underlies `list.sort(cmp)`, `removeIf`, `computeIfAbsent`, streams (Days 17-18), `CompletableFuture` (Day 21), and every Spring callback you will meet later. `Optional` complements it by turning "maybe absent" into an explicit type instead of a `null` that explodes later.

Interviews ask: *what is a functional interface*, *what does effectively final mean and why*, *method reference kinds*, *Optional.orElse vs orElseGet*, and *why not use Optional as a field or parameter*. Today you answer them by writing the code.""",
    sections=[
        sec(
            "Lambdas and functional interfaces",
            "A **functional interface** has exactly one abstract method (a *SAM*); `default`, `static`, and `Object` methods do not count. A **lambda** `(params) -> body` is a concise implementation of that single method; the target type is inferred from context (`Comparator<String> c = (a, b) -> a.length() - b.length();`). The `java.util.function` package supplies the common shapes: `Predicate<T>` (T -> boolean), `Function<T,R>`, `UnaryOperator<T>`, `BinaryOperator<T>`, `Supplier<T>` (() -> T), `Consumer<T>` (T -> void), `BiFunction`, and primitive variants (`IntPredicate`, `ToIntFunction`, `IntUnaryOperator`) that avoid boxing. A lambda **captures** variables from the enclosing scope, but only if they are *effectively final* (never reassigned).",
            "Before lambdas, passing behavior required verbose anonymous classes. Lambdas make APIs like `removeIf`, `sort`, `forEach`, `computeIfAbsent`, and streams practical, enable **strategy/callback** patterns in one line, and enable lazy evaluation (`Supplier`). They compile via `invokedynamic`, so they are not anonymous inner classes at runtime (and do not create a new `this` scope: inside a lambda `this` is the enclosing instance).",
            ["Concise, readable callbacks and strategies", "Enable declarative styles (filter/map) and lazy defaults (`Supplier`)", "Composable (`andThen`, `and`, `negate`)", "Primitive specializations avoid boxing overhead"],
            ["Stack traces and debugging of nested lambdas are harder to read", "Captured variables must be effectively final (workarounds like arrays/`AtomicInteger` can hide bugs)", "Checked exceptions cannot be thrown from the standard functional interfaces without wrapping"],
            "Capturing a loop variable that is reassigned (`for (int i...) tasks.add(() -> i)`) does not compile (*local variables referenced from a lambda expression must be final or effectively final*). Working around it with a mutable holder (`int[] c = {0}`) compiles but is not thread-safe. Putting side effects in a `Predicate` used by a parallel stream gives nondeterministic results. A lambda that throws a checked `IOException` inside `Function` does not compile; developers then swallow or wrap it badly. Using `Function<Integer,Integer>` in a hot loop allocates `Integer` objects; use `IntUnaryOperator`.",
            """- Syntax: `x -> x * 2`, `(a, b) -> a + b`, `() -> 42`, `(String s) -> { return s.trim(); }`.
- Lambdas need a **target type**: `Object o = () -> 1;` does not compile.
- `@FunctionalInterface` is optional documentation; the compiler then verifies the single-abstract-method rule.
- Capture: locals and parameters must be effectively final; fields (instance/static) may be mutated.
- Composition: `f.andThen(g)` = g(f(x)); `f.compose(g)` = f(g(x)); `p.and(q)`, `p.or(q)`, `p.negate()`, `Predicate.not(p)`.
- Common signatures: `Comparator.comparing(Function)`, `list.removeIf(Predicate)`, `map.computeIfAbsent(k, Function)`, `Optional.orElseGet(Supplier)`.
- Own SAM: `@FunctionalInterface interface Validator<T> { boolean validate(T t); }`.""",
            [
                ("Tiny — basic shapes", """Predicate<String> notBlank = s -> !s.isBlank();
Function<String, Integer> len = String::length;
Supplier<List<String>> fresh = ArrayList::new;
Consumer<String> shout = s -> System.out.println(s.toUpperCase());
BinaryOperator<Integer> max = Math::max;
System.out.println(notBlank.test(" ") + " " + len.apply("abcd") + " " + max.apply(3, 9)); // false 4 9
shout.accept("hi");   // HI"""),
                ("Tiny — the loop-variable capture pitfall and its fix", """List<Supplier<Integer>> bad = new ArrayList<>();
// for (int i = 0; i < 3; i++) bad.add(() -> i);   // compile error: i is not effectively final

List<Supplier<Integer>> good = new ArrayList<>();
for (int i = 0; i < 3; i++) {
    final int copy = i;                 // new effectively-final variable per iteration
    good.add(() -> copy);
}
good.forEach(s -> System.out.print(s.get() + " "));   // 0 1 2"""),
                ("Medium — a custom functional interface, composition, and laziness", """import java.util.*;
import java.util.function.*;

public class Rules {
    @FunctionalInterface
    interface Rule<T> {
        boolean check(T t);
        default Rule<T> and(Rule<? super T> other) { return t -> check(t) && other.check(t); }
    }

    static <T> void validate(T value, Rule<? super T> rule, Supplier<String> message) {
        if (!rule.check(value)) throw new IllegalArgumentException(message.get());  // message built lazily
    }

    public static void main(String[] args) {
        Rule<String> nonEmpty = s -> !s.isEmpty();
        Rule<String> shortEnough = s -> s.length() <= 5;
        Rule<String> both = nonEmpty.and(shortEnough);

        validate("abc", both, () -> "should not be built");
        try {
            validate("abcdefgh", both, () -> "too long: abcdefgh");
        } catch (IllegalArgumentException e) {
            System.out.println(e.getMessage());   // too long: abcdefgh
        }

        Function<Integer, Integer> plus1 = x -> x + 1, times2 = x -> x * 2;
        System.out.println(plus1.andThen(times2).apply(5) + " " + plus1.compose(times2).apply(5)); // 12 11
    }
}"""),
            ],
            [
                ("What makes an interface functional, and does `Comparator` qualify even though it declares `equals`?", "Exactly one abstract method; `Comparator.equals(Object)` matches an `Object` method so it does not count."),
                ("Why can't a lambda modify a captured local variable?", "Captured locals are copied into the lambda; allowing mutation would imply shared mutable state across stack frames/threads. They must be effectively final."),
                ("What is the difference between `f.andThen(g)` and `f.compose(g)`?", "`andThen`: g(f(x)); `compose`: f(g(x))."),
                ("Which functional type would you use for a lazily computed default and why?", "`Supplier<T>`: the computation runs only if needed (e.g. `Optional.orElseGet`)."),
            ],
        ),
        sec(
            "Method references",
            "A **method reference** is a compact lambda that just calls an existing method. Four kinds: (1) **static**: `Integer::parseInt` = `s -> Integer.parseInt(s)`; (2) **bound instance** (receiver fixed now): `prefix::concat` = `s -> prefix.concat(s)`; (3) **unbound instance** (receiver is the first argument): `String::toUpperCase` = `s -> s.toUpperCase()`; (4) **constructor**: `ArrayList::new` = `() -> new ArrayList<>()`, `Person::new` = `n -> new Person(n)`, `int[]::new` = `n -> new int[n]`. The compiler matches the reference's parameters to the functional interface's.",
            "Method references remove noise and name the intent (`map(String::trim)` reads better than `map(s -> s.trim())`), encourage small named methods that are individually testable, and are the standard way to pass factories (`Supplier<List<T>>`) and key extractors (`Comparator.comparing(Person::name)`).",
            ["Shorter and more readable than equivalent lambdas", "Encourages reusable, testable methods", "Good for constructors and factories", "Often produces clearer stack traces than anonymous lambdas"],
            ["Overloaded methods can make a reference ambiguous (`ambiguous method reference`)", "Bound vs unbound distinction confuses beginners", "Over-use can hide logic; a short lambda is sometimes clearer"],
            "`Stream.of(\"1\",\"2\").map(Integer::toString)` is ambiguous (static `toString(int)` vs instance `toString()`) and does not compile. Using `this::method` captures `this` and can leak the object in long-lived callbacks. A bound reference evaluates its receiver **immediately**: `list::add` with a null `list` throws NPE at creation. Passing `Integer::parseInt` where `Function<String,Integer>` is expected works, but `Function<String,Long>` does not (no autoboxing of the result type conversion).",
            """- `ClassName::staticMethod` - arguments pass through unchanged.
- `instance::method` - bound; receiver evaluated at creation time.
- `ClassName::instanceMethod` - unbound; first argument becomes the receiver.
- `ClassName::new` - constructor; target type picks which constructor.
- Array constructor: `String[]::new` (used by `stream.toArray(String[]::new)`).
- Rewrite rule: if a lambda body is only a call that forwards all parameters in order, use a method reference.""",
            [
                ("Tiny — the four kinds side by side", """Function<String, Integer> a = Integer::parseInt;              // static
String prefix = "id-";
Function<String, String> b = prefix::concat;                 // bound instance
Function<String, String> c = String::toUpperCase;            // unbound instance
Supplier<List<String>> d = ArrayList::new;                   // constructor
System.out.println(a.apply("7") + " " + b.apply("9") + " " + c.apply("x")); // 7 id-9 X"""),
                ("Tiny — constructor reference to build objects", """record Person(String name) {}
Function<String, Person> make = Person::new;
List<Person> people = Stream.of("ann", "bob").map(make).toList();
System.out.println(people);           // [Person[name=ann], Person[name=bob]]
String[] arr = Stream.of("a", "b").toArray(String[]::new);"""),
                ("Medium — indexBy with a key-extractor reference", """import java.util.*;
import java.util.function.Function;

public class Index {
    static <K, V> Map<K, V> indexBy(List<V> values, Function<? super V, ? extends K> key) {
        Map<K, V> map = new LinkedHashMap<>();
        for (V v : values) {
            K k = key.apply(v);
            if (map.putIfAbsent(k, v) != null) throw new IllegalArgumentException("duplicate key " + k);
        }
        return map;
    }
    record Book(String isbn, String title) {}

    public static void main(String[] args) {
        List<Book> books = List.of(new Book("1", "Java"), new Book("2", "Go"));
        System.out.println(indexBy(books, Book::isbn).keySet());   // [1, 2]
    }
}"""),
            ],
            [
                ("Rewrite `s -> s.length()` and `(a, b) -> Integer.compare(a, b)` as method references.", "`String::length` (unbound instance) and `Integer::compare` (static)."),
                ("What is the difference between `prefix::concat` and `String::concat`?", "`prefix::concat` is bound: `s -> prefix.concat(s)` (one argument); `String::concat` is unbound: `(a, b) -> a.concat(b)` (two arguments)."),
                ("When is the receiver of a bound method reference evaluated?", "At the moment the reference is created, not each time it is invoked."),
                ("What does `String[]::new` do?", "It is an array constructor reference, `n -> new String[n]`, used by `toArray`."),
            ],
        ),
        sec(
            "Optional: modelling absence",
            "`Optional<T>` is an immutable container that holds either a non-null value or nothing. It is intended **only as a return type** to signal \"may be absent\". Key API: factories `of` (NPE on null), `ofNullable`, `empty`; transforms `map`, `flatMap`, `filter`; extraction `orElse(value)`, `orElseGet(supplier)`, `orElseThrow()` / `orElseThrow(supplier)`; actions `ifPresent`, `ifPresentOrElse`; `or(supplier)`, `stream()`. Primitive variants: `OptionalInt`, `OptionalLong`, `OptionalDouble`.",
            "`null` carries no information and fails far from its origin (`NullPointerException`). A method returning `Optional<User> findByEmail(...)` forces callers to decide what absence means, and chained `map`/`flatMap` replaces pyramids of null checks. It is the standard return type for repository lookups (Spring Data `findById`) and stream terminal operations (`findFirst`, `max`).",
            ["Makes absence explicit in the type system", "Fluent null-safe chains with `map`/`flatMap`/`filter`", "`orElseThrow` gives clean \"not found\" handling", "Streams return it, so you must know it"],
            ["Extra allocation; not `Serializable`; poor fit for fields, parameters, collections", "`get()` without a check reintroduces the failure (`NoSuchElementException`)", "Overuse makes code noisy; `Optional<Optional<T>>` or `Optional<List<T>>` is a smell"],
            "`opt.get()` on an empty Optional throws `NoSuchElementException` - as bad as an NPE. `orElse(expensiveCall())` **always** evaluates its argument, even when a value is present; use `orElseGet(() -> expensiveCall())`. `Optional.of(maybeNull)` throws NPE. Returning `null` from a method whose type is `Optional` defeats the whole purpose. Using `Optional` as a JPA entity field or method parameter is discouraged (extra allocation, awkward callers). `if (opt.isPresent()) { x = opt.get(); }` is just a verbose null check - prefer `map`/`orElse*`.",
            """- Create: `Optional.of(v)` (v non-null), `Optional.ofNullable(v)`, `Optional.empty()`.
- Transform: `opt.map(User::address)` (if mapper returns null -> empty), `opt.flatMap(User::addressOpt)` when the mapper itself returns `Optional`.
- Default: `orElse(const)`, `orElseGet(() -> compute())` for lazy, `orElseThrow(() -> new NotFound(id))`.
- Side effects: `ifPresent(x -> ...)`, `ifPresentOrElse(x -> ..., () -> ...)`.
- Do not: store in fields, accept as parameters, wrap collections (return an empty collection instead), compare with `==`.""",
            [
                ("Tiny — map / filter / orElse", """Optional<String> name = Optional.of("  Ada ");
String clean = name.map(String::trim).filter(s -> !s.isEmpty()).orElse("anonymous");
System.out.println(clean);                                     // Ada
System.out.println(Optional.<String>empty().map(String::trim).orElse("anonymous")); // anonymous"""),
                ("Tiny — orElse vs orElseGet", """static String expensive() { System.out.println("computing"); return "fallback"; }
Optional<String> present = Optional.of("value");
present.orElse(expensive());                 // prints "computing" even though not needed!
present.orElseGet(() -> expensive());        // prints nothing"""),
                ("Medium — null-safe chain with flatMap", """import java.util.*;

public class Chain {
    record Address(String city) {}
    record User(String name, Address address) {
        Optional<Address> addressOpt() { return Optional.ofNullable(address); }
    }

    static Optional<String> cityOf(User u) {
        return Optional.ofNullable(u)
                .flatMap(User::addressOpt)
                .map(Address::city)
                .filter(c -> !c.isBlank());
    }

    public static void main(String[] args) {
        System.out.println(cityOf(new User("a", new Address("Pune"))));  // Optional[Pune]
        System.out.println(cityOf(new User("b", null)));                 // Optional.empty
        System.out.println(cityOf(null));                                // Optional.empty
        System.out.println(cityOf(new User("c", new Address(" "))).orElse("unknown")); // unknown
    }
}"""),
            ],
            [
                ("Why is `opt.orElse(load())` sometimes a performance bug?", "`load()` is evaluated eagerly even when the Optional is present; use `orElseGet(this::load)`."),
                ("When do you use `flatMap` instead of `map`?", "When the mapping function itself returns an `Optional`; `map` would produce `Optional<Optional<T>>`."),
                ("Should an entity field be `Optional<String>`?", "No - Optional is for return values; fields and parameters should use plain types (nullable) or overloads."),
                ("What does `Optional.map(f)` return if `f` returns null?", "An empty Optional."),
            ],
        ),
    ],
    interview=[
        ("What is a functional interface? Name five built-ins.", "An interface with exactly one abstract method. `Predicate`, `Function`, `Supplier`, `Consumer`, `UnaryOperator`, `BinaryOperator`, `Runnable`, `Callable`, `Comparator`."),
        ("What does effectively final mean and why does it exist?", "A local that is never reassigned after initialization. Lambdas copy captured locals; allowing reassignment would create confusing or racy shared state."),
        ("Lambda vs anonymous class - how do they differ?", "`this` refers to the enclosing instance in a lambda but to the anonymous object in an anonymous class; lambdas compile to `invokedynamic`, are only for functional interfaces, and cannot have state/fields."),
        ("List the kinds of method references with an example of each.", "Static `Integer::parseInt`, bound `prefix::concat`, unbound `String::length`, constructor `ArrayList::new`."),
        ("Optional.orElse vs orElseGet vs orElseThrow?", "orElse eagerly takes a value, orElseGet lazily computes one, orElseThrow signals absence as an exception."),
        ("Why shouldn't you use Optional for fields or parameters?", "It adds allocation, is not serializable, makes call sites awkward, and was designed only as a return-type idiom."),
    ],
    mistakes=[
        "Trying to mutate a captured local from a lambda (`local variables referenced from a lambda expression must be final or effectively final`).",
        "Using `Optional.get()` without checking - prefer `orElseThrow` with a meaningful exception.",
        "`orElse(expensive())` instead of `orElseGet`.",
        "Ambiguous method references (`Integer::toString`) - use a lambda.",
        "Doing side effects in `map`/`filter` lambdas, then being surprised by laziness or parallelism.",
        "Returning `null` from a method that returns `Optional`, or wrapping collections in `Optional`.",
    ],
    reading=[
        "Javadoc: `java.util.function` package summary, `java.util.Optional`",
        "Java Language Specification 15.27 (Lambda Expressions) and 15.13 (Method References)",
        "Oracle Java Tutorials - *Lambda Expressions* and *Method References*",
        "Stuart Marks, \"Optional - The Mother of All Bikesheds\" (Devoxx), and the Javadoc API note on `Optional`",
    ],
    glossary=[
        ("SAM", "Single abstract method - the shape of a functional interface"),
        ("Effectively final", "A variable never reassigned after initialization; capturable by lambdas"),
        ("Closure", "A lambda together with the captured variables of its enclosing scope"),
        ("Target typing", "Inferring a lambda's type from the context where it appears"),
        ("Bound / unbound reference", "Method reference with a fixed receiver / with the receiver as first argument"),
        ("invokedynamic", "JVM instruction used to link lambdas lazily at runtime"),
        ("Monad-like", "Informal: a container with `map`/`flatMap` (Optional, Stream)"),
    ],
    tasks=[
        task(
            "lambda-filter", "Lambda Filter, Map, and Closures", "Warm-up", "LambdaFilter",
            "Implement generic higher-order helpers that accept lambdas, then three small closure exercises: applying a unary operator twice, creating independent counters, and generating adders without falling into the loop-variable capture trap.",
            [
                "`filter(list, predicate)` returns a new list of elements matching the predicate (accepts `Predicate<? super T>`)",
                "`mapAll(list, fn)` returns a new list of transformed elements (accepts `Function<? super T, ? extends R>`)",
                "`applyTwice(f, x)` applies an `IntUnaryOperator` two times",
                "`counter()` returns a `Supplier<Integer>`; each supplier yields 1, 2, 3, ... independently of other suppliers",
                "`adders(n)` returns `n` `IntUnaryOperator`s where the operator at index `i` adds `i` to its argument",
            ],
            ["empty list", "predicate matching nothing/everything", "`adders(0)` is empty; negative `n` throws `IllegalArgumentException`", "two counters do not share state"],
            {"LambdaFilter.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Function;
import java.util.function.IntUnaryOperator;
import java.util.function.Predicate;
import java.util.function.Supplier;

/** Higher-order functions and closures. */
public final class LambdaFilter {

    private LambdaFilter() {
    }

    public static <T> List<T> filter(List<T> items, Predicate<? super T> predicate) {
        //@TODO filter | return a new list containing only the elements for which predicate.test is true
        List<T> out = new ArrayList<>();
        for (T item : items) {
            if (predicate.test(item)) {
                out.add(item);
            }
        }
        return out;
        //@END
    }

    public static <T, R> List<R> mapAll(List<T> items, Function<? super T, ? extends R> fn) {
        //@TODO mapAll | return a new list with fn applied to every element, preserving order
        List<R> out = new ArrayList<>();
        for (T item : items) {
            out.add(fn.apply(item));
        }
        return out;
        //@END
    }

    public static int applyTwice(IntUnaryOperator f, int x) {
        //@TODO applyTwice | return f(f(x))
        return f.applyAsInt(f.applyAsInt(x));
        //@END
    }

    public static Supplier<Integer> counter() {
        //@TODO counter | return a Supplier whose successive calls return 1, 2, 3, ...; every counter() call gets its own state (captured AtomicInteger)
        AtomicInteger next = new AtomicInteger();
        return next::incrementAndGet;
        //@END
    }

    public static List<IntUnaryOperator> adders(int n) {
        //@TODO adders | return n operators; operator i adds i to its input; IllegalArgumentException when n is negative (watch effectively-final capture in the loop)
        if (n < 0) {
            throw new IllegalArgumentException("n must be >= 0");
        }
        List<IntUnaryOperator> ops = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            final int amount = i;
            ops.add(x -> x + amount);
        }
        return ops;
        //@END
    }
}
'''},
            {"LambdaFilterTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import java.util.function.IntUnaryOperator;
import java.util.function.Supplier;
import org.junit.jupiter.api.Test;

class LambdaFilterTest {

    @Test
    void r1_filter() {
        assertThat(LambdaFilter.filter(List.of(1, 2, 3, 4, 5, 6), n -> n % 2 == 0)).containsExactly(2, 4, 6);
        assertThat(LambdaFilter.filter(List.of("a", "bb", "ccc"), s -> s.length() > 5)).isEmpty();
        assertThat(LambdaFilter.filter(List.of("a", "b"), s -> true)).containsExactly("a", "b");
        assertThat(LambdaFilter.filter(List.<String>of(), s -> true)).isEmpty();
    }

    @Test
    void r1_filterAcceptsSupertypePredicate() {
        java.util.function.Predicate<Object> notNullObject = o -> o != null;
        assertThat(LambdaFilter.filter(List.of("x", "y"), notNullObject)).containsExactly("x", "y");
    }

    @Test
    void r2_mapAll() {
        assertThat(LambdaFilter.mapAll(List.of("a", "bb", "ccc"), String::length)).containsExactly(1, 2, 3);
        assertThat(LambdaFilter.mapAll(List.of(1, 2), n -> "#" + n)).containsExactly("#1", "#2");
        assertThat(LambdaFilter.mapAll(List.<Integer>of(), n -> n)).isEmpty();
    }

    @Test
    void r3_applyTwice() {
        assertThat(LambdaFilter.applyTwice(x -> x * 3, 2)).isEqualTo(18);
        assertThat(LambdaFilter.applyTwice(x -> x + 10, -5)).isEqualTo(15);
        assertThat(LambdaFilter.applyTwice(IntUnaryOperator.identity(), 7)).isEqualTo(7);
    }

    @Test
    void r4_countersAreIndependent() {
        Supplier<Integer> a = LambdaFilter.counter();
        Supplier<Integer> b = LambdaFilter.counter();
        assertThat(a.get()).isEqualTo(1);
        assertThat(a.get()).isEqualTo(2);
        assertThat(b.get()).isEqualTo(1);
        assertThat(a.get()).isEqualTo(3);
    }

    @Test
    void r5_addersCaptureTheRightValue() {
        List<IntUnaryOperator> ops = LambdaFilter.adders(4);
        assertThat(ops).hasSize(4);
        for (int i = 0; i < ops.size(); i++) {
            assertThat(ops.get(i).applyAsInt(100)).isEqualTo(100 + i);
        }
    }

    @Test
    void r5_addersEdgeCases() {
        assertThat(LambdaFilter.adders(0)).isEmpty();
        assertThatThrownBy(() -> LambdaFilter.adders(-1)).isInstanceOf(IllegalArgumentException.class);
    }
}
'''},
            ["`counter()` needs mutable state inside a lambda: capture an `AtomicInteger` (a reference that is itself effectively final).", "Create a fresh `final int` per loop iteration before capturing it."],
            ["No mutation of input lists", "Lambdas/method references used where natural", "Loop-variable capture handled with a per-iteration copy"],
            constraints=["Do not use streams (Day 17)", "Do not edit the tests"],
        ),
        task(
            "predicate-compose", "Composing Predicates and Functions", "Core", "PredicateCompose",
            "Combine small predicates into richer rules (`allOf`, `anyOf`, `noneOf`), make predicates null-safe, build a realistic username validator from composed predicates, and chain `UnaryOperator`s into a pipeline.",
            [
                "`allOf(predicates)` is true only if every predicate matches (empty list -> `true`)",
                "`anyOf(predicates)` is true if at least one matches (empty list -> `false`)",
                "`noneOf(predicates)` is true if no predicate matches (empty list -> `true`)",
                "`nullSafe(predicate)` returns `false` for `null` input instead of calling the delegate",
                "`validUsername()` accepts names that are 3-12 characters, start with a letter, and contain only letters, digits, or `_`; it returns `false` for `null`",
                "`pipeline(operators)` composes unary operators left-to-right; an empty list is the identity",
            ],
            ["empty predicate lists", "null input", "boundary lengths 2/3/12/13", "start with digit or underscore"],
            {"PredicateCompose.java": r'''package @PKG@;

import java.util.List;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.UnaryOperator;

/** Predicate and function composition. */
public final class PredicateCompose {

    private PredicateCompose() {
    }

    public static <T> Predicate<T> allOf(List<Predicate<T>> predicates) {
        //@TODO allOf | combine with Predicate.and; empty list yields a predicate that is always true
        Predicate<T> result = t -> true;
        for (Predicate<T> p : predicates) {
            result = result.and(p);
        }
        return result;
        //@END
    }

    public static <T> Predicate<T> anyOf(List<Predicate<T>> predicates) {
        //@TODO anyOf | combine with Predicate.or; empty list yields a predicate that is always false
        Predicate<T> result = t -> false;
        for (Predicate<T> p : predicates) {
            result = result.or(p);
        }
        return result;
        //@END
    }

    public static <T> Predicate<T> noneOf(List<Predicate<T>> predicates) {
        //@TODO noneOf | true when no predicate matches (negate anyOf); empty list is always true
        return anyOf(predicates).negate();
        //@END
    }

    public static <T> Predicate<T> nullSafe(Predicate<? super T> delegate) {
        //@TODO nullSafe | return a predicate that is false for null input and otherwise delegates
        return t -> t != null && delegate.test(t);
        //@END
    }

    public static Predicate<String> validUsername() {
        //@TODO validUsername | build from composed predicates: not null, length 3..12, first char is a letter, all chars letter/digit/underscore
        Predicate<String> length = s -> s.length() >= 3 && s.length() <= 12;
        Predicate<String> startsWithLetter = s -> Character.isLetter(s.charAt(0));
        Predicate<String> allowedChars = s -> s.chars().allMatch(c -> Character.isLetterOrDigit(c) || c == '_');
        return nullSafe(length.and(startsWithLetter).and(allowedChars));
        //@END
    }

    public static <T> Function<T, T> pipeline(List<UnaryOperator<T>> operators) {
        //@TODO pipeline | apply operators left to right using Function.andThen; empty list returns the identity function
        Function<T, T> result = Function.identity();
        for (UnaryOperator<T> op : operators) {
            result = result.andThen(op);
        }
        return result;
        //@END
    }
}
'''},
            {"PredicateComposeTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.UnaryOperator;
import org.junit.jupiter.api.Test;

class PredicateComposeTest {

    private final Predicate<Integer> positive = n -> n > 0;
    private final Predicate<Integer> even = n -> n % 2 == 0;

    @Test
    void r1_allOf() {
        Predicate<Integer> p = PredicateCompose.allOf(List.of(positive, even));
        assertThat(p.test(4)).isTrue();
        assertThat(p.test(3)).isFalse();
        assertThat(p.test(-2)).isFalse();
        assertThat(PredicateCompose.allOf(List.<Predicate<Integer>>of()).test(1)).isTrue();
    }

    @Test
    void r2_anyOf() {
        Predicate<Integer> p = PredicateCompose.anyOf(List.of(positive, even));
        assertThat(p.test(3)).isTrue();
        assertThat(p.test(-2)).isTrue();
        assertThat(p.test(-3)).isFalse();
        assertThat(PredicateCompose.anyOf(List.<Predicate<Integer>>of()).test(1)).isFalse();
    }

    @Test
    void r3_noneOf() {
        Predicate<Integer> p = PredicateCompose.noneOf(List.of(positive, even));
        assertThat(p.test(-3)).isTrue();
        assertThat(p.test(-2)).isFalse();
        assertThat(p.test(5)).isFalse();
        assertThat(PredicateCompose.noneOf(List.<Predicate<Integer>>of()).test(1)).isTrue();
    }

    @Test
    void r4_nullSafe() {
        Predicate<String> nonEmpty = s -> !s.isEmpty();
        Predicate<String> safe = PredicateCompose.nullSafe(nonEmpty);
        assertThat(safe.test(null)).isFalse();
        assertThat(safe.test("")).isFalse();
        assertThat(safe.test("x")).isTrue();
    }

    @Test
    void r5_validUsernameAccepts() {
        Predicate<String> v = PredicateCompose.validUsername();
        assertThat(v.test("abc")).isTrue();
        assertThat(v.test("Ada_99")).isTrue();
        assertThat(v.test("abcdefghijkl")).isTrue();
    }

    @Test
    void r5_validUsernameRejects() {
        Predicate<String> v = PredicateCompose.validUsername();
        assertThat(v.test(null)).isFalse();
        assertThat(v.test("ab")).isFalse();
        assertThat(v.test("abcdefghijklm")).isFalse();
        assertThat(v.test("9lives")).isFalse();
        assertThat(v.test("_hidden")).isFalse();
        assertThat(v.test("bad name")).isFalse();
        assertThat(v.test("bad-name")).isFalse();
        assertThat(v.test("")).isFalse();
    }

    @Test
    void r6_pipelineAppliesLeftToRight() {
        UnaryOperator<String> trim = String::trim;
        UnaryOperator<String> upper = String::toUpperCase;
        UnaryOperator<String> exclaim = s -> s + "!";
        Function<String, String> f = PredicateCompose.pipeline(List.of(trim, upper, exclaim));
        assertThat(f.apply("  hi ")).isEqualTo("HI!");
        UnaryOperator<Integer> plus1 = n -> n + 1;
        UnaryOperator<Integer> times2 = n -> n * 2;
        assertThat(PredicateCompose.pipeline(List.of(plus1, times2)).apply(5)).isEqualTo(12);
        assertThat(PredicateCompose.pipeline(List.of(times2, plus1)).apply(5)).isEqualTo(11);
    }

    @Test
    void r6_emptyPipelineIsIdentity() {
        assertThat(PredicateCompose.pipeline(List.<UnaryOperator<String>>of()).apply("same")).isEqualTo("same");
    }
}
'''},
            ["`Predicate.and/or/negate` already do the heavy lifting; start from a neutral element.", "`String.chars()` gives an `IntStream` - using it for `allMatch` is fine here (character check), or write a loop."],
            ["Neutral elements handled (empty lists)", "No duplicated null checks - compose with `nullSafe`", "Readable composition rather than one giant boolean expression"],
            constraints=["Do not use regular expressions in `validUsername` (compose predicates instead)", "Do not edit the tests"],
        ),
        task(
            "optional-chain", "Optional Chains Without Null Checks", "Stretch", "OptionalChain",
            "Model absent data with `Optional`: navigate a nullable `User -> Address -> city` chain, search a list, parse input safely, and convert absence into a meaningful exception - all without writing `if (x == null)` in the main logic path (null checks are allowed only at the API boundary through `Optional.ofNullable`).",
            [
                "`cityOf(user)` returns the trimmed city, or empty when the user, address, or city is null/blank",
                "`findByName(users, name)` finds the first user whose name equals `name` ignoring case; `null` name or no match -> empty",
                "`parsePositive(text)` returns the parsed positive integer, or empty for null, blank, non-numeric, zero, or negative input",
                "`zipOrDefault(user, defaultZip)` returns the zip code or the default (compute lazily using `orElseGet` where it makes sense)",
                "`requireCity(user)` returns the city or throws `IllegalStateException` whose message contains the user's name (or `unknown` when the user is null)",
            ],
            ["null user", "null address", "blank city", "whitespace around numbers (`\" 42 \"` parses)", "overflow like `99999999999` returns empty"],
            {"Address.java": r'''package @PKG@;

/** Provided: any component may be null. */
public record Address(String city, String zip) {
}
''',
             "User.java": r'''package @PKG@;

/** Provided: address may be null. */
public record User(String name, Address address) {
}
''',
             "OptionalChain.java": r'''package @PKG@;

import java.util.List;
import java.util.Optional;

/** Optional-based lookups. */
public final class OptionalChain {

    private OptionalChain() {
    }

    public static Optional<String> cityOf(User user) {
        //@TODO cityOf | Optional.ofNullable(user) -> map address -> map city -> map trim -> filter non-empty
        return Optional.ofNullable(user)
                .map(User::address)
                .map(Address::city)
                .map(String::trim)
                .filter(c -> !c.isEmpty());
        //@END
    }

    public static Optional<User> findByName(List<User> users, String name) {
        //@TODO findByName | first user whose name equalsIgnoreCase name; empty if name is null or none matches (loop or later-day streams are both fine)
        if (name == null) {
            return Optional.empty();
        }
        for (User u : users) {
            if (u != null && name.equalsIgnoreCase(u.name())) {
                return Optional.of(u);
            }
        }
        return Optional.empty();
        //@END
    }

    public static Optional<Integer> parsePositive(String text) {
        //@TODO parsePositive | parse a trimmed int; empty for null/blank/non-numeric/overflow/zero/negative (catch NumberFormatException)
        return Optional.ofNullable(text)
                .map(String::trim)
                .flatMap(t -> {
                    try {
                        return Optional.of(Integer.parseInt(t));
                    } catch (NumberFormatException e) {
                        return Optional.empty();
                    }
                })
                .filter(n -> n > 0);
        //@END
    }

    public static String zipOrDefault(User user, String defaultZip) {
        //@TODO zipOrDefault | return the address zip, or defaultZip when the user, address, or zip is missing
        return Optional.ofNullable(user)
                .map(User::address)
                .map(Address::zip)
                .orElse(defaultZip);
        //@END
    }

    public static String requireCity(User user) {
        //@TODO requireCity | return cityOf(user) or throw IllegalStateException with a message containing the user's name ("unknown" for a null user) via orElseThrow
        return cityOf(user).orElseThrow(() -> new IllegalStateException(
                "no city for " + Optional.ofNullable(user).map(User::name).orElse("unknown")));
        //@END
    }
}
'''},
            {"OptionalChainTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import org.junit.jupiter.api.Test;

class OptionalChainTest {

    private static final User ANN = new User("Ann", new Address(" Pune ", "411001"));
    private static final User BOB = new User("Bob", null);
    private static final User CAL = new User("Cal", new Address("   ", null));

    @Test
    void r1_cityOf() {
        assertThat(OptionalChain.cityOf(ANN)).contains("Pune");
        assertThat(OptionalChain.cityOf(BOB)).isEmpty();
        assertThat(OptionalChain.cityOf(CAL)).isEmpty();
        assertThat(OptionalChain.cityOf(null)).isEmpty();
        assertThat(OptionalChain.cityOf(new User("D", new Address(null, "1")))).isEmpty();
    }

    @Test
    void r2_findByName() {
        List<User> users = List.of(ANN, BOB, CAL);
        assertThat(OptionalChain.findByName(users, "bob")).contains(BOB);
        assertThat(OptionalChain.findByName(users, "ANN")).contains(ANN);
        assertThat(OptionalChain.findByName(users, "zed")).isEmpty();
        assertThat(OptionalChain.findByName(users, null)).isEmpty();
        assertThat(OptionalChain.findByName(List.of(), "ann")).isEmpty();
    }

    @Test
    void r3_parsePositive() {
        assertThat(OptionalChain.parsePositive("42")).contains(42);
        assertThat(OptionalChain.parsePositive("  7 ")).contains(7);
    }

    @Test
    void r3_parsePositiveRejects() {
        assertThat(OptionalChain.parsePositive(null)).isEmpty();
        assertThat(OptionalChain.parsePositive("")).isEmpty();
        assertThat(OptionalChain.parsePositive("   ")).isEmpty();
        assertThat(OptionalChain.parsePositive("abc")).isEmpty();
        assertThat(OptionalChain.parsePositive("0")).isEmpty();
        assertThat(OptionalChain.parsePositive("-5")).isEmpty();
        assertThat(OptionalChain.parsePositive("99999999999")).isEmpty();
        assertThat(OptionalChain.parsePositive("4.5")).isEmpty();
    }

    @Test
    void r4_zipOrDefault() {
        assertThat(OptionalChain.zipOrDefault(ANN, "000000")).isEqualTo("411001");
        assertThat(OptionalChain.zipOrDefault(BOB, "000000")).isEqualTo("000000");
        assertThat(OptionalChain.zipOrDefault(CAL, "000000")).isEqualTo("000000");
        assertThat(OptionalChain.zipOrDefault(null, "000000")).isEqualTo("000000");
    }

    @Test
    void r5_requireCity() {
        assertThat(OptionalChain.requireCity(ANN)).isEqualTo("Pune");
        assertThatThrownBy(() -> OptionalChain.requireCity(BOB))
                .isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("Bob");
        assertThatThrownBy(() -> OptionalChain.requireCity(null))
                .isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("unknown");
    }
}
'''},
            ["`flatMap` is the right tool when your lambda itself returns an `Optional` (e.g. a safe parse).", "A `try/catch` for `NumberFormatException` inside the `flatMap` lambda is a clean way to turn parsing failure into `Optional.empty()`."],
            ["No `Optional.get()` and no `isPresent()`/`get()` pairs", "`orElseThrow` supplies a meaningful exception", "No `Optional` fields or parameters"],
            constraints=["Do not call `Optional.get()` or `isPresent()`", "Do not edit the tests"],
        ),
        task(
            "method-ref-map", "Method References Zoo", "Challenge", "MethodRefMap",
            "Return functions implemented with each kind of method reference (static, bound, unbound, constructor) and build a map index from a key-extractor reference. **Challenge:** the implementation of each method must be a method reference (not a lambda), except where a lambda is unavoidable - justify those in a comment.",
            [
                "`parser()` returns a `Function<String,Integer>` using `Integer::parseInt` (static reference)",
                "`upper()` returns a `Function<String,String>` using `String::toUpperCase` (unbound instance reference)",
                "`prefixer(prefix)` returns a function that prepends `prefix`, using a bound reference (`prefix::concat`); `null` prefix throws `NullPointerException` immediately (when creating the reference)",
                "`listFactory()` returns a `Supplier<List<String>>` producing a **new** empty mutable list each call (`ArrayList::new`)",
                "`personFactory()` returns a `Function<String, Person>` using the `Person::new` constructor reference",
                "`indexBy(values, keyFn)` returns a `LinkedHashMap` of key -> value in input order and throws `IllegalArgumentException` on duplicate keys",
            ],
            ["null prefix", "each listFactory call yields a distinct list", "duplicate keys", "empty input"],
            {"Person.java": r'''package @PKG@;

/** Provided: constructor target for Person::new. */
public record Person(String name) {
}
''',
             "MethodRefMap.java": r'''package @PKG@;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.function.Supplier;

/** One method of each method-reference kind. */
public final class MethodRefMap {

    private MethodRefMap() {
    }

    public static Function<String, Integer> parser() {
        //@TODO parser | return Integer::parseInt (static method reference)
        return Integer::parseInt;
        //@END
    }

    public static Function<String, String> upper() {
        //@TODO upper | return String::toUpperCase (unbound instance method reference)
        return String::toUpperCase;
        //@END
    }

    public static Function<String, String> prefixer(String prefix) {
        //@TODO prefixer | return prefix::concat (bound reference); a null prefix must fail immediately with NullPointerException
        return prefix::concat;
        //@END
    }

    public static Supplier<List<String>> listFactory() {
        //@TODO listFactory | return ArrayList::new (constructor reference)
        return ArrayList::new;
        //@END
    }

    public static Function<String, Person> personFactory() {
        //@TODO personFactory | return Person::new (constructor reference)
        return Person::new;
        //@END
    }

    public static <K, V> Map<K, V> indexBy(List<V> values, Function<? super V, ? extends K> keyFn) {
        //@TODO indexBy | build a LinkedHashMap key -> value in input order; IllegalArgumentException on a duplicate key (use putIfAbsent)
        Map<K, V> index = new LinkedHashMap<>();
        for (V value : values) {
            K key = keyFn.apply(value);
            if (index.putIfAbsent(key, value) != null) {
                throw new IllegalArgumentException("duplicate key: " + key);
            }
        }
        return index;
        //@END
    }
}
'''},
            {"MethodRefMapTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import java.util.Map;
import java.util.function.Supplier;
import org.junit.jupiter.api.Test;

class MethodRefMapTest {

    @Test
    void r1_parser() {
        assertThat(MethodRefMap.parser().apply("42")).isEqualTo(42);
        assertThat(MethodRefMap.parser().apply("-7")).isEqualTo(-7);
        assertThatThrownBy(() -> MethodRefMap.parser().apply("x")).isInstanceOf(NumberFormatException.class);
    }

    @Test
    void r2_upper() {
        assertThat(MethodRefMap.upper().apply("abc")).isEqualTo("ABC");
        assertThat(MethodRefMap.upper().apply("")).isEmpty();
    }

    @Test
    void r3_prefixerIsBound() {
        assertThat(MethodRefMap.prefixer("id-").apply("9")).isEqualTo("id-9");
        assertThat(MethodRefMap.prefixer("").apply("z")).isEqualTo("z");
    }

    @Test
    void r3_nullPrefixFailsImmediately() {
        assertThatThrownBy(() -> MethodRefMap.prefixer(null)).isInstanceOf(NullPointerException.class);
    }

    @Test
    void r4_listFactoryReturnsFreshMutableLists() {
        Supplier<List<String>> factory = MethodRefMap.listFactory();
        List<String> first = factory.get();
        List<String> second = factory.get();
        first.add("x");
        assertThat(first).containsExactly("x");
        assertThat(second).isEmpty();
        assertThat(first).isNotSameAs(second);
    }

    @Test
    void r5_personFactory() {
        Person p = MethodRefMap.personFactory().apply("Ada");
        assertThat(p).isEqualTo(new Person("Ada"));
        assertThat(p.name()).isEqualTo("Ada");
    }

    @Test
    void r6_indexByKeepsOrder() {
        List<Person> people = List.of(new Person("ann"), new Person("bob"), new Person("cy"));
        Map<Integer, String> byLength = MethodRefMap.indexBy(List.of("a", "bb", "ccc"), String::length)
                .entrySet().stream().collect(java.util.stream.Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
        assertThat(byLength).containsEntry(2, "bb");
        Map<String, Person> byName = MethodRefMap.indexBy(people, Person::name);
        assertThat(byName.keySet()).containsExactly("ann", "bob", "cy");
        assertThat(byName.get("bob")).isEqualTo(new Person("bob"));
        assertThat(MethodRefMap.indexBy(List.<Person>of(), Person::name)).isEmpty();
    }

    @Test
    void r6_indexByRejectsDuplicates() {
        assertThatThrownBy(() -> MethodRefMap.indexBy(List.of("aa", "bb"), String::length))
                .isInstanceOf(IllegalArgumentException.class);
    }
}
'''},
            ["`prefix::concat` evaluates `prefix` immediately; a null receiver fails when the reference is created, which is exactly what the test expects.", "`map.putIfAbsent` returns the previous value (or null) - handy for duplicate detection."],
            ["Each of the four reference kinds is used where the task names it", "No lambda where a method reference works", "Fail-fast semantics of bound references understood and commented"],
            constraints=["Return method references (not lambdas) from `parser`, `upper`, `prefixer`, `listFactory`, `personFactory`", "Do not edit the tests"],
        ),
    ],
)
