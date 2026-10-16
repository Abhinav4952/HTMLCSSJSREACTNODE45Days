# Day 16 — Lambdas, Functional Interfaces, Method References, and Optional

**Phase:** Core Java  
**Primary theme:** Pass behavior as data: lambdas, `java.util.function`, method references, and `Optional` for absent values.  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-lambda-filter`, `task-02-predicate-compose`, `task-03-optional-chain`, `task-04-method-ref-map`  
**Instruction alignment:** Maps to the Day 16 entry of the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21 (no Spring today)

## Overview

Java 8 introduced lambdas so that *behavior* can be passed to methods as a value. That one idea underlies `list.sort(cmp)`, `removeIf`, `computeIfAbsent`, streams (Days 17-18), `CompletableFuture` (Day 21), and every Spring callback you will meet later. `Optional` complements it by turning "maybe absent" into an explicit type instead of a `null` that explodes later.

Interviews ask: *what is a functional interface*, *what does effectively final mean and why*, *method reference kinds*, *Optional.orElse vs orElseGet*, and *why not use Optional as a field or parameter*. Today you answer them by writing the code.

## Day roadmap

1. Lambdas and functional interfaces
2. Method references
3. Optional: modelling absence
4. Interview angles
5. Common mistakes & debugging
6. Further reading, glossary, answers

### Lambdas and functional interfaces

#### What it is

A **functional interface** has exactly one abstract method (a *SAM*); `default`, `static`, and `Object` methods do not count. A **lambda** `(params) -> body` is a concise implementation of that single method; the target type is inferred from context (`Comparator<String> c = (a, b) -> a.length() - b.length();`). The `java.util.function` package supplies the common shapes: `Predicate<T>` (T -> boolean), `Function<T,R>`, `UnaryOperator<T>`, `BinaryOperator<T>`, `Supplier<T>` (() -> T), `Consumer<T>` (T -> void), `BiFunction`, and primitive variants (`IntPredicate`, `ToIntFunction`, `IntUnaryOperator`) that avoid boxing. A lambda **captures** variables from the enclosing scope, but only if they are *effectively final* (never reassigned).

#### Why it exists / why it matters

Before lambdas, passing behavior required verbose anonymous classes. Lambdas make APIs like `removeIf`, `sort`, `forEach`, `computeIfAbsent`, and streams practical, enable **strategy/callback** patterns in one line, and enable lazy evaluation (`Supplier`). They compile via `invokedynamic`, so they are not anonymous inner classes at runtime (and do not create a new `this` scope: inside a lambda `this` is the enclosing instance).

#### Pros and cons

**Pros**

- Concise, readable callbacks and strategies
- Enable declarative styles (filter/map) and lazy defaults (`Supplier`)
- Composable (`andThen`, `and`, `negate`)
- Primitive specializations avoid boxing overhead

**Cons / tradeoffs**

- Stack traces and debugging of nested lambdas are harder to read
- Captured variables must be effectively final (workarounds like arrays/`AtomicInteger` can hide bugs)
- Checked exceptions cannot be thrown from the standard functional interfaces without wrapping

#### What happens without it / when misused

Capturing a loop variable that is reassigned (`for (int i...) tasks.add(() -> i)`) does not compile (*local variables referenced from a lambda expression must be final or effectively final*). Working around it with a mutable holder (`int[] c = {0}`) compiles but is not thread-safe. Putting side effects in a `Predicate` used by a parallel stream gives nondeterministic results. A lambda that throws a checked `IOException` inside `Function` does not compile; developers then swallow or wrap it badly. Using `Function<Integer,Integer>` in a hot loop allocates `Integer` objects; use `IntUnaryOperator`.

#### Syntax and rules

- Syntax: `x -> x * 2`, `(a, b) -> a + b`, `() -> 42`, `(String s) -> { return s.trim(); }`.
- Lambdas need a **target type**: `Object o = () -> 1;` does not compile.
- `@FunctionalInterface` is optional documentation; the compiler then verifies the single-abstract-method rule.
- Capture: locals and parameters must be effectively final; fields (instance/static) may be mutated.
- Composition: `f.andThen(g)` = g(f(x)); `f.compose(g)` = f(g(x)); `p.and(q)`, `p.or(q)`, `p.negate()`, `Predicate.not(p)`.
- Common signatures: `Comparator.comparing(Function)`, `list.removeIf(Predicate)`, `map.computeIfAbsent(k, Function)`, `Optional.orElseGet(Supplier)`.
- Own SAM: `@FunctionalInterface interface Validator<T> { boolean validate(T t); }`.

#### Examples

**Example 1.1 — Tiny — basic shapes**

```java
Predicate<String> notBlank = s -> !s.isBlank();
Function<String, Integer> len = String::length;
Supplier<List<String>> fresh = ArrayList::new;
Consumer<String> shout = s -> System.out.println(s.toUpperCase());
BinaryOperator<Integer> max = Math::max;
System.out.println(notBlank.test(" ") + " " + len.apply("abcd") + " " + max.apply(3, 9)); // false 4 9
shout.accept("hi");   // HI
```

**Example 1.2 — Tiny — the loop-variable capture pitfall and its fix**

```java
List<Supplier<Integer>> bad = new ArrayList<>();
// for (int i = 0; i < 3; i++) bad.add(() -> i);   // compile error: i is not effectively final

List<Supplier<Integer>> good = new ArrayList<>();
for (int i = 0; i < 3; i++) {
    final int copy = i;                 // new effectively-final variable per iteration
    good.add(() -> copy);
}
good.forEach(s -> System.out.print(s.get() + " "));   // 0 1 2
```

**Example 1.3 — Medium — a custom functional interface, composition, and laziness**

```java
import java.util.*;
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
}
```

#### Quick checks

1. What makes an interface functional, and does `Comparator` qualify even though it declares `equals`?
2. Why can't a lambda modify a captured local variable?
3. What is the difference between `f.andThen(g)` and `f.compose(g)`?
4. Which functional type would you use for a lazily computed default and why?

### Method references

#### What it is

A **method reference** is a compact lambda that just calls an existing method. Four kinds: (1) **static**: `Integer::parseInt` = `s -> Integer.parseInt(s)`; (2) **bound instance** (receiver fixed now): `prefix::concat` = `s -> prefix.concat(s)`; (3) **unbound instance** (receiver is the first argument): `String::toUpperCase` = `s -> s.toUpperCase()`; (4) **constructor**: `ArrayList::new` = `() -> new ArrayList<>()`, `Person::new` = `n -> new Person(n)`, `int[]::new` = `n -> new int[n]`. The compiler matches the reference's parameters to the functional interface's.

#### Why it exists / why it matters

Method references remove noise and name the intent (`map(String::trim)` reads better than `map(s -> s.trim())`), encourage small named methods that are individually testable, and are the standard way to pass factories (`Supplier<List<T>>`) and key extractors (`Comparator.comparing(Person::name)`).

#### Pros and cons

**Pros**

- Shorter and more readable than equivalent lambdas
- Encourages reusable, testable methods
- Good for constructors and factories
- Often produces clearer stack traces than anonymous lambdas

**Cons / tradeoffs**

- Overloaded methods can make a reference ambiguous (`ambiguous method reference`)
- Bound vs unbound distinction confuses beginners
- Over-use can hide logic; a short lambda is sometimes clearer

#### What happens without it / when misused

`Stream.of("1","2").map(Integer::toString)` is ambiguous (static `toString(int)` vs instance `toString()`) and does not compile. Using `this::method` captures `this` and can leak the object in long-lived callbacks. A bound reference evaluates its receiver **immediately**: `list::add` with a null `list` throws NPE at creation. Passing `Integer::parseInt` where `Function<String,Integer>` is expected works, but `Function<String,Long>` does not (no autoboxing of the result type conversion).

#### Syntax and rules

- `ClassName::staticMethod` - arguments pass through unchanged.
- `instance::method` - bound; receiver evaluated at creation time.
- `ClassName::instanceMethod` - unbound; first argument becomes the receiver.
- `ClassName::new` - constructor; target type picks which constructor.
- Array constructor: `String[]::new` (used by `stream.toArray(String[]::new)`).
- Rewrite rule: if a lambda body is only a call that forwards all parameters in order, use a method reference.

#### Examples

**Example 2.1 — Tiny — the four kinds side by side**

```java
Function<String, Integer> a = Integer::parseInt;              // static
String prefix = "id-";
Function<String, String> b = prefix::concat;                 // bound instance
Function<String, String> c = String::toUpperCase;            // unbound instance
Supplier<List<String>> d = ArrayList::new;                   // constructor
System.out.println(a.apply("7") + " " + b.apply("9") + " " + c.apply("x")); // 7 id-9 X
```

**Example 2.2 — Tiny — constructor reference to build objects**

```java
record Person(String name) {}
Function<String, Person> make = Person::new;
List<Person> people = Stream.of("ann", "bob").map(make).toList();
System.out.println(people);           // [Person[name=ann], Person[name=bob]]
String[] arr = Stream.of("a", "b").toArray(String[]::new);
```

**Example 2.3 — Medium — indexBy with a key-extractor reference**

```java
import java.util.*;
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
}
```

#### Quick checks

1. Rewrite `s -> s.length()` and `(a, b) -> Integer.compare(a, b)` as method references.
2. What is the difference between `prefix::concat` and `String::concat`?
3. When is the receiver of a bound method reference evaluated?
4. What does `String[]::new` do?

### Optional: modelling absence

#### What it is

`Optional<T>` is an immutable container that holds either a non-null value or nothing. It is intended **only as a return type** to signal "may be absent". Key API: factories `of` (NPE on null), `ofNullable`, `empty`; transforms `map`, `flatMap`, `filter`; extraction `orElse(value)`, `orElseGet(supplier)`, `orElseThrow()` / `orElseThrow(supplier)`; actions `ifPresent`, `ifPresentOrElse`; `or(supplier)`, `stream()`. Primitive variants: `OptionalInt`, `OptionalLong`, `OptionalDouble`.

#### Why it exists / why it matters

`null` carries no information and fails far from its origin (`NullPointerException`). A method returning `Optional<User> findByEmail(...)` forces callers to decide what absence means, and chained `map`/`flatMap` replaces pyramids of null checks. It is the standard return type for repository lookups (Spring Data `findById`) and stream terminal operations (`findFirst`, `max`).

#### Pros and cons

**Pros**

- Makes absence explicit in the type system
- Fluent null-safe chains with `map`/`flatMap`/`filter`
- `orElseThrow` gives clean "not found" handling
- Streams return it, so you must know it

**Cons / tradeoffs**

- Extra allocation; not `Serializable`; poor fit for fields, parameters, collections
- `get()` without a check reintroduces the failure (`NoSuchElementException`)
- Overuse makes code noisy; `Optional<Optional<T>>` or `Optional<List<T>>` is a smell

#### What happens without it / when misused

`opt.get()` on an empty Optional throws `NoSuchElementException` - as bad as an NPE. `orElse(expensiveCall())` **always** evaluates its argument, even when a value is present; use `orElseGet(() -> expensiveCall())`. `Optional.of(maybeNull)` throws NPE. Returning `null` from a method whose type is `Optional` defeats the whole purpose. Using `Optional` as a JPA entity field or method parameter is discouraged (extra allocation, awkward callers). `if (opt.isPresent()) { x = opt.get(); }` is just a verbose null check - prefer `map`/`orElse*`.

#### Syntax and rules

- Create: `Optional.of(v)` (v non-null), `Optional.ofNullable(v)`, `Optional.empty()`.
- Transform: `opt.map(User::address)` (if mapper returns null -> empty), `opt.flatMap(User::addressOpt)` when the mapper itself returns `Optional`.
- Default: `orElse(const)`, `orElseGet(() -> compute())` for lazy, `orElseThrow(() -> new NotFound(id))`.
- Side effects: `ifPresent(x -> ...)`, `ifPresentOrElse(x -> ..., () -> ...)`.
- Do not: store in fields, accept as parameters, wrap collections (return an empty collection instead), compare with `==`.

#### Examples

**Example 3.1 — Tiny — map / filter / orElse**

```java
Optional<String> name = Optional.of("  Ada ");
String clean = name.map(String::trim).filter(s -> !s.isEmpty()).orElse("anonymous");
System.out.println(clean);                                     // Ada
System.out.println(Optional.<String>empty().map(String::trim).orElse("anonymous")); // anonymous
```

**Example 3.2 — Tiny — orElse vs orElseGet**

```java
static String expensive() { System.out.println("computing"); return "fallback"; }
Optional<String> present = Optional.of("value");
present.orElse(expensive());                 // prints "computing" even though not needed!
present.orElseGet(() -> expensive());        // prints nothing
```

**Example 3.3 — Medium — null-safe chain with flatMap**

```java
import java.util.*;

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
}
```

#### Quick checks

1. Why is `opt.orElse(load())` sometimes a performance bug?
2. When do you use `flatMap` instead of `map`?
3. Should an entity field be `Optional<String>`?
4. What does `Optional.map(f)` return if `f` returns null?

## Interview angles

**Q: What is a functional interface? Name five built-ins.**

An interface with exactly one abstract method. `Predicate`, `Function`, `Supplier`, `Consumer`, `UnaryOperator`, `BinaryOperator`, `Runnable`, `Callable`, `Comparator`.

**Q: What does effectively final mean and why does it exist?**

A local that is never reassigned after initialization. Lambdas copy captured locals; allowing reassignment would create confusing or racy shared state.

**Q: Lambda vs anonymous class - how do they differ?**

`this` refers to the enclosing instance in a lambda but to the anonymous object in an anonymous class; lambdas compile to `invokedynamic`, are only for functional interfaces, and cannot have state/fields.

**Q: List the kinds of method references with an example of each.**

Static `Integer::parseInt`, bound `prefix::concat`, unbound `String::length`, constructor `ArrayList::new`.

**Q: Optional.orElse vs orElseGet vs orElseThrow?**

orElse eagerly takes a value, orElseGet lazily computes one, orElseThrow signals absence as an exception.

**Q: Why shouldn't you use Optional for fields or parameters?**

It adds allocation, is not serializable, makes call sites awkward, and was designed only as a return-type idiom.

## Common mistakes & debugging

- Trying to mutate a captured local from a lambda (`local variables referenced from a lambda expression must be final or effectively final`).
- Using `Optional.get()` without checking - prefer `orElseThrow` with a meaningful exception.
- `orElse(expensive())` instead of `orElseGet`.
- Ambiguous method references (`Integer::toString`) - use a lambda.
- Doing side effects in `map`/`filter` lambdas, then being surprised by laziness or parallelism.
- Returning `null` from a method that returns `Optional`, or wrapping collections in `Optional`.

## Further reading

- Javadoc: `java.util.function` package summary, `java.util.Optional`
- Java Language Specification 15.27 (Lambda Expressions) and 15.13 (Method References)
- Oracle Java Tutorials - *Lambda Expressions* and *Method References*
- Stuart Marks, "Optional - The Mother of All Bikesheds" (Devoxx), and the Javadoc API note on `Optional`

## Glossary

| Term | Meaning |
|------|---------|
| SAM | Single abstract method - the shape of a functional interface |
| Effectively final | A variable never reassigned after initialization; capturable by lambdas |
| Closure | A lambda together with the captured variables of its enclosing scope |
| Target typing | Inferring a lambda's type from the context where it appears |
| Bound / unbound reference | Method reference with a fixed receiver / with the receiver as first argument |
| invokedynamic | JVM instruction used to link lambdas lazily at runtime |
| Monad-like | Informal: a container with `map`/`flatMap` (Optional, Stream) |

## Answers

Answers to every **Quick check** above (numbered `section.question`).

- **1.1** — What makes an interface functional, and does `Comparator` qualify even though it declares `equals`?  
  Exactly one abstract method; `Comparator.equals(Object)` matches an `Object` method so it does not count.

- **1.2** — Why can't a lambda modify a captured local variable?  
  Captured locals are copied into the lambda; allowing mutation would imply shared mutable state across stack frames/threads. They must be effectively final.

- **1.3** — What is the difference between `f.andThen(g)` and `f.compose(g)`?  
  `andThen`: g(f(x)); `compose`: f(g(x)).

- **1.4** — Which functional type would you use for a lazily computed default and why?  
  `Supplier<T>`: the computation runs only if needed (e.g. `Optional.orElseGet`).

- **2.1** — Rewrite `s -> s.length()` and `(a, b) -> Integer.compare(a, b)` as method references.  
  `String::length` (unbound instance) and `Integer::compare` (static).

- **2.2** — What is the difference between `prefix::concat` and `String::concat`?  
  `prefix::concat` is bound: `s -> prefix.concat(s)` (one argument); `String::concat` is unbound: `(a, b) -> a.concat(b)` (two arguments).

- **2.3** — When is the receiver of a bound method reference evaluated?  
  At the moment the reference is created, not each time it is invoked.

- **2.4** — What does `String[]::new` do?  
  It is an array constructor reference, `n -> new String[n]`, used by `toArray`.

- **3.1** — Why is `opt.orElse(load())` sometimes a performance bug?  
  `load()` is evaluated eagerly even when the Optional is present; use `orElseGet(this::load)`.

- **3.2** — When do you use `flatMap` instead of `map`?  
  When the mapping function itself returns an `Optional`; `map` would produce `Optional<Optional<T>>`.

- **3.3** — Should an entity field be `Optional<String>`?  
  No - Optional is for return values; fields and parameters should use plain types (nullable) or overloads.

- **3.4** — What does `Optional.map(f)` return if `f` returns null?  
  An empty Optional.
