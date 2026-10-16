from gen_helpers import sec, task

DAY = dict(
    num=13,
    title="Generics: Classes, Methods, Bounds, and Wildcards (PECS)",
    theme="Write type-safe reusable code with generic classes/methods, bounded type parameters, and wildcards.",
    objectives=[
        "Declare and use generic classes and generic methods with correct type-parameter naming",
        "Explain type erasure and what it forbids (`new T()`, `instanceof List<String>`, generic arrays)",
        "Apply bounded type parameters (`extends`, intersection bounds) to express capabilities",
        "Choose between `? extends`, `? super`, and unbounded `?` using the PECS rule",
        "Implement a small generic data structure (stack) that is safe for callers and iterable",
        "Read generic compiler errors and fix them without raw types or blind casts",
    ],
    prereqs=["Day 06–10 — classes, interfaces, inheritance, and polymorphism", "Day 12 — wrappers/autoboxing (generics work only with reference types)"],
    overview="""Generics let one class or method work for many types while the **compiler** proves that you never put a `String` where an `Integer` belongs. Before Java 5 every collection held `Object`, so you cast on the way out and discovered mistakes as `ClassCastException` in production. Generics move that failure to compile time.

In backend work you meet generics everywhere: `List<Order>`, `Map<String, Customer>`, `Optional<T>`, `Comparator<T>`, Spring's `ResponseEntity<T>`, repositories like `JpaRepository<Order, Long>`, and your own utility methods (`<T> T firstOrThrow(List<T>)`). Interviewers love three questions: *what is type erasure*, *why can't I do `List<Object> x = new ArrayList<String>()`*, and *explain PECS*. Today you answer all three in code.""",
    sections=[
        sec(
            "Generic classes, generic methods, and type erasure",
            "A **generic class** declares one or more *type parameters* in angle brackets (`class Box<T>`). Callers supply *type arguments* (`Box<String>`). A **generic method** declares its own parameters before the return type (`static <T> T first(List<T> xs)`) and the compiler usually *infers* them from the arguments. Mental model: a generic type is a **template the compiler stamps checks from**; at runtime only one `Box.class` exists because of **type erasure** — the compiler removes type arguments, inserts casts where needed, and generates bridge methods.",
            "Without generics, reusable containers store `Object`, forcing casts and risking `ClassCastException`. Generics give compile-time safety, remove casts, and make APIs self-documenting (`Map<UserId, List<Order>>` tells a reader everything). Erasure exists for **backward compatibility**: pre-Java-5 bytecode and libraries keep working unchanged. Real problems solved: type-safe DAOs, result wrappers, caches, event buses.",
            ["Compile-time type safety eliminates a whole class of `ClassCastException` bugs", "No casts at call sites; code reads cleaner", "One implementation serves many types (less duplication)", "Self-documenting APIs and better IDE completion"],
            ["Erasure removes type info at runtime: no `new T()`, no `T[] a = new T[n]`, no `instanceof List<String>`", "Primitives cannot be type arguments (`List<int>` is illegal) so boxing cost and null-unboxing risk appear", "Generic compiler errors can be cryptic until you learn to read capture types"],
            "**Raw types** (`List list = new ArrayList();`) turn the checks off: `list.add(42)` into a `List<String>` compiles with an *unchecked* warning and explodes later as `ClassCastException` at a distant line (**heap pollution**). Treating `List<Dog>` as a `List<Animal>` is rejected by the compiler for good reason: otherwise `animals.add(new Cat())` would corrupt the dog list. Overloads that differ only in type arguments (`void f(List<String>)` / `void f(List<Integer>)`) clash after erasure (*name clash: same erasure*).",
            """- Type-parameter naming convention: `T` (type), `E` (element), `K`/`V` (key/value), `R` (result), `N` (number).
- Diamond: `Box<String> b = new Box<>(\"x\");` lets the compiler infer the right-hand type arguments.
- Generic method call with explicit witness (rare): `Util.<String>empty()`.
- **Invariance:** `List<Dog>` is **not** a subtype of `List<Animal>` even though `Dog extends Animal`. Arrays *are* covariant (`Dog[]` is an `Animal[]`) and that is a known design wart (`ArrayStoreException`).
- Static members cannot use the class's type parameter; static generic methods declare their own `<T>`.
- Reifiable types (`String`, `List<?>`, raw `List`, primitives) are fully available at runtime; `List<String>` is not.""",
            [
                ("Tiny — generic class", """class Box<T> {
    private final T value;
    Box(T value) { this.value = value; }
    T get() { return value; }
}
Box<String> b = new Box<>("hi");
String s = b.get();          // no cast needed
// Box<String> bad = new Box<>(42);   // compile error"""),
                ("Tiny — generic method with inference", """static <T> T firstOrDefault(java.util.List<T> xs, T def) {
    return xs.isEmpty() ? def : xs.get(0);
}
String s = firstOrDefault(java.util.List.of("a", "b"), "z");  // T = String
Integer n = firstOrDefault(java.util.List.of(), 7);            // T = Integer
System.out.println(s + n); // a7"""),
                ("Medium — erasure observed at runtime", """import java.util.*;

public class ErasureDemo {
    public static void main(String[] args) {
        List<String> strings = new ArrayList<>();
        List<Integer> ints = new ArrayList<>();
        System.out.println(strings.getClass() == ints.getClass()); // true  (one ArrayList.class)

        @SuppressWarnings({"rawtypes", "unchecked"})
        List raw = strings;                 // allowed, unchecked
        raw.add(42);                        // heap pollution!
        try {
            String s = strings.get(0);      // compiler-inserted cast to String
        } catch (ClassCastException e) {
            System.out.println("CCE at read time, not at add time");
        }
    }
}
// Output:
// true
// CCE at read time, not at add time"""),
            ],
            [
                ("Why does `List<Object> xs = new ArrayList<String>();` not compile?", "Generics are invariant. If it compiled you could `xs.add(42)` and put an Integer into what is really an `ArrayList<String>`."),
                ("What does `new ArrayList<String>().getClass() == new ArrayList<Integer>().getClass()` print and why?", "`true`; type arguments are erased, only one `ArrayList` class exists at runtime."),
                ("Why can't you write `new T()` or `new T[10]` inside a generic class?", "`T` is erased to its bound (usually `Object`), so the JVM does not know which class to instantiate; pass a `Supplier<T>`/`Class<T>` or use `(T[]) new Object[n]` carefully."),
                ("Give two reasons `List<int>` is illegal.", "Type arguments must be reference types because erasure replaces `T` with `Object`/bound, which a primitive is not; use `List<Integer>` (autoboxing)."),
            ],
        ),
        sec(
            "Bounded type parameters and intersection bounds",
            "A **bounded type parameter** restricts what callers may supply: `<T extends Comparable<T>>` means *T must be comparable with itself*. `extends` is used for classes and interfaces alike. Multiple bounds form an **intersection**: `<T extends Number & Comparable<T>>` (class bound first, then interfaces). Inside the method you may call any method of the bounds on a `T`. The recursive bound `<T extends Comparable<T>>` is the standard way to say *this type has a natural order*.",
            "Without a bound `T` is just `Object`, so you cannot compare, add, or call domain methods. Bounds express **capabilities** and keep the method body free of casts and `instanceof`. `Collections.max(Collection<? extends T>)` has the bound `<T extends Object & Comparable<? super T>>`, which is the same idea in its most flexible form.",
            ["Lets generic code call bound methods (`compareTo`, `doubleValue`) safely", "Errors move to compile time: passing a non-comparable type is rejected", "Documents intent in the signature", "`Comparable<? super T>` makes subclasses of a comparable parent work"],
            ["Signatures get long and harder to read", "Recursive bounds are conceptually tricky", "A bound cannot be a type *variable* with a lower bound (`<T super X>` does not exist)"],
            "Using `<T extends Comparable>` (raw bound) compiles with warnings and loses safety. Using `<T extends Comparable<T>>` instead of `Comparable<? super T>` rejects `Dog extends Animal implements Comparable<Animal>` - a legitimate type - producing the confusing error *inferred type does not conform to upper-bound*. Forgetting that the **class** bound must come first in an intersection gives a compile error.",
            """- `<T extends Number>`: T is `Number` or a subtype (`Integer`, `Double`).
- `<T extends Number & Comparable<T>>`: at most one class, first; any number of interfaces after `&`.
- Prefer `<T extends Comparable<? super T>>` for max/min/sort helpers.
- Bounds also apply to class declarations: `class Stats<N extends Number> { ... }`.
- A bounded `T` is erased to its **leftmost bound** (so the example above erases to `Number`).""",
            [
                ("Tiny — upper bound", """static <N extends Number> double sum(java.util.List<N> xs) {
    double total = 0;
    for (N n : xs) total += n.doubleValue();   // allowed: N is a Number
    return total;
}
System.out.println(sum(java.util.List.of(1, 2, 3)));      // 6.0
System.out.println(sum(java.util.List.of(1.5, 2.5)));     // 4.0"""),
                ("Tiny — max with the flexible Comparable bound", """static <T extends Comparable<? super T>> T max(java.util.List<? extends T> xs) {
    T best = xs.get(0);
    for (T x : xs) if (x.compareTo(best) > 0) best = x;
    return best;
}
// max(List.of("pear", "apple", "zoo")) -> "zoo\""""),
                ("Medium — why `? super T` matters in the bound", """class Animal implements Comparable<Animal> {
    final int weight;
    Animal(int w) { weight = w; }
    public int compareTo(Animal o) { return Integer.compare(weight, o.weight); }
}
class Dog extends Animal { Dog(int w) { super(w); } }

// With <T extends Comparable<T>> this call FAILS: Dog is Comparable<Animal>, not Comparable<Dog>.
// With <T extends Comparable<? super T>> it compiles:
Dog heaviest = max(java.util.List.of(new Dog(10), new Dog(30)));  // uses Animal.compareTo"""),
            ],
            [
                ("Why must the class bound come first in `<T extends Number & Comparable<T>>`?", "The language allows at most one class bound and it must be listed first; the rest must be interfaces."),
                ("What is the erasure of `<T extends Comparable<T>> T max(T a, T b)`?", "`Comparable max(Comparable a, Comparable b)` - the leftmost bound replaces `T`."),
                ("When do you prefer `Comparable<? super T>` over `Comparable<T>`?", "When subclasses inherit `compareTo` from a parent that is comparable to the parent type (e.g. `Dog` using `Animal.compareTo`)."),
            ],
        ),
        sec(
            "Wildcards and the PECS rule",
            "A **wildcard** `?` stands for an *unknown* type. `List<? extends Number>` is a list of *some* subtype of Number (a **producer**: you can read `Number`s out). `List<? super Integer>` is a list of *some* supertype of Integer (a **consumer**: you can write `Integer`s in). `List<?>` means *anything*, read-only as `Object`. **PECS = Producer `extends`, Consumer `super`** (Joshua Bloch, *Effective Java* item 31).",
            "Invariance (`List<Dog>` is not a `List<Animal>`) makes APIs too rigid. Wildcards restore flexibility **without** losing safety: a method that only *reads* numbers should accept `List<Integer>` and `List<Double>`; a method that only *adds* integers should accept `List<Number>` and `List<Object>`. This is how `Collections.copy(List<? super T> dest, List<? extends T> src)` is declared.",
            ["Maximizes API reusability while staying type-safe", "Communicates direction of data flow (in vs out) to callers", "Required to use the full power of the JDK collection utilities", "Wildcard capture lets one helper work on any `List<?>`"],
            ["You cannot add to `List<? extends T>` (except `null`) - surprising at first", "Return types should **not** be wildcards; they push complexity onto callers", "Readability: nested wildcards (`Map<? extends K, ? extends List<? extends V>>`) are hard to parse"],
            "Writing `void addAll(List<Number> src, List<Number> dst)` forces callers to build a `List<Number>` and rejects `List<Integer>` - the API is invariant for no reason. Declaring `void print(List<? extends Number> xs)` and then calling `xs.add(1)` is a compile error (the compiler cannot prove the unknown subtype accepts Integer). Using raw `List` to dodge the problem re-opens the heap-pollution hole.",
            """- **Get-Put principle:** read only -> `? extends`; write only -> `? super`; both -> no wildcard (use `T` exactly).
- `List<?>`: you may call `size()`, `get(i)` (as `Object`), `clear()`, but cannot add anything but `null`.
- **Wildcard capture:** a private generic helper can name the unknown type:
  `static void swap(List<?> l, int i, int j) { swapHelper(l, i, j); }` and `private static <E> void swapHelper(List<E> l, int i, int j) {...}`.
- Wildcards are for **parameters**; do not use them in return types or on class declarations.
- Subtyping: `List<Integer>` <: `List<? extends Number>` <: `List<?>`; `List<Number>` <: `List<? super Integer>`.""",
            [
                ("Tiny — producer extends", """static double total(java.util.Collection<? extends Number> xs) {
    double t = 0;
    for (Number n : xs) t += n.doubleValue();
    return t;
}
// total(List.of(1, 2, 3)) == 6.0 ; total(List.of(1.5)) == 1.5"""),
                ("Tiny — consumer super", """static void fillWithInts(java.util.List<? super Integer> sink, int n) {
    for (int i = 0; i < n; i++) sink.add(i);   // OK: sink accepts Integer
}
java.util.List<Number> nums = new java.util.ArrayList<>();
java.util.List<Object> objs = new java.util.ArrayList<>();
fillWithInts(nums, 2);
fillWithInts(objs, 3);
System.out.println(nums + " " + objs);   // [0, 1] [0, 1, 2]"""),
                ("Medium — PECS copy + wildcard capture", """import java.util.*;

public final class Pecs {
    public static <T> void copy(List<? super T> dst, List<? extends T> src) {
        for (T t : src) dst.add(t);          // src produces, dst consumes
    }
    public static void swap(List<?> list, int i, int j) { swapHelper(list, i, j); }
    private static <E> void swapHelper(List<E> list, int i, int j) {
        E tmp = list.get(i);
        list.set(i, list.get(j));
        list.set(j, tmp);
    }
    public static void main(String[] a) {
        List<Number> dst = new ArrayList<>();
        copy(dst, List.of(1, 2));            // T inferred as Integer
        copy(dst, List.of(3.5));             // T inferred as Double (or Number)
        swap(dst, 0, 2);
        System.out.println(dst);             // [3.5, 2, 1]
    }
}"""),
            ],
            [
                ("State PECS and give the JDK method that uses it.", "Producer `extends`, Consumer `super`; `Collections.copy(List<? super T> dest, List<? extends T> src)`."),
                ("Why does `List<? extends Number> xs; xs.add(1);` fail?", "`xs` could really be a `List<Double>`; the compiler cannot guarantee an `Integer` fits, so only `null` may be added."),
                ("Which parameter type accepts `List<Integer>`, `List<Number>` and `List<Object>`?", "`List<? super Integer>` (consumer of Integers)."),
                ("Why is `List<?>` not the same as `List<Object>`?", "`List<Object>` accepts any object but only `List<Object>` arguments; `List<?>` accepts a list of any type but allows no additions."),
            ],
        ),
    ],
    interview=[
        ("What is type erasure and what limitations does it cause?", "The compiler checks type arguments, then removes them, inserting casts and bridge methods. Consequences: no `new T()`, no generic arrays, no `instanceof List<String>`, overloads that differ only by type arguments clash, and runtime reflection sees raw types (except for generic *signatures* stored in class metadata)."),
        ("Explain PECS with an example.", "If a parameter produces values you read, declare `? extends T`; if it consumes values you write, declare `? super T`. `Collections.copy(dest, src)` reads from `src` (`extends`) and writes into `dest` (`super`)."),
        ("Why are arrays covariant but generics invariant?", "Arrays were designed before generics and check stores at runtime (`ArrayStoreException`). Generics are erased so runtime checks are impossible; invariance is the only way to keep compile-time safety."),
        ("`List<Object>` vs `List<?>` vs raw `List`?", "`List<Object>`: list of objects, invariant. `List<?>`: list of unknown type, read-only-ish and safe. Raw: unchecked legacy, disables checks."),
        ("What is a recursive bound and why use `Comparable<? super T>`?", "`T extends Comparable<T>` says T compares to itself; `? super T` also allows types that inherit comparability from a supertype."),
        ("What is heap pollution?", "A variable of a parameterized type refers to an object that is not of that type, usually via raw types or unchecked casts; it surfaces later as `ClassCastException`."),
    ],
    mistakes=[
        "Using raw types to \"make the error go away\" - you get `ClassCastException` later instead of a compile error now.",
        "Declaring `T extends Comparable<T>` and then being unable to call with a subclass whose parent defines `compareTo` (`inferred type does not conform to upper-bound`). Use `Comparable<? super T>`.",
        "Trying to `add` to a `List<? extends X>` parameter (`incompatible types: capture#1 of ? extends X`). You wanted `? super X` or an exact `T`.",
        "Returning wildcard types such as `List<? extends Number>` from a public API - callers cannot do much with it.",
        "Creating `new T[n]` (`generic array creation`); use `(T[]) new Object[n]` privately with a comment, or a `List<T>`.",
        "Confusing `static <T> void f(T x)` (generic method) with a class-level `T` - static members cannot see the class type parameter.",
    ],
    reading=[
        "Java Language Specification, ch. 4.5 (Parameterized Types), 4.6 (Type Erasure), 4.10 (Subtyping)",
        "Oracle Java Tutorials - *Generics* trail (bounded types, wildcards, erasure, restrictions)",
        "*Effective Java* (Bloch), items 26-33 (raw types, wildcards, generic methods, heterogeneous containers)",
        "Javadoc: `java.util.Collections#copy`, `#max`, `java.util.function.Function`",
    ],
    glossary=[
        ("Type parameter", "A placeholder such as `T` declared by a generic class or method"),
        ("Type argument", "The concrete type supplied by the caller (`String` in `Box<String>`)"),
        ("Invariance", "`G<A>` is not a subtype of `G<B>` even if `A <: B`"),
        ("Type erasure", "Compiler removal of type arguments, leaving casts and bridge methods"),
        ("Reifiable type", "A type whose full information exists at runtime (e.g. `String`, `List<?>`)"),
        ("PECS", "Producer `extends`, Consumer `super`"),
        ("Wildcard capture", "Compiler inference that gives a name to an unknown `?` so a helper can use it"),
        ("Heap pollution", "A parameterized variable pointing to an object of the wrong parameterization"),
    ],
    tasks=[
        task(
            "box-generic", "Generic Box with map/orElse", "Warm-up", "Box",
            "Implement an immutable generic container `Box<T>` that either holds a non-null value or is empty, with `map`, `orElse`, and value-based equality. A test also proves that `Box<String>` and `Box<Integer>` share one runtime class (erasure).",
            [
                "`Box.of(value)` returns a box holding the value and throws `NullPointerException` for `null`",
                "`Box.empty()` returns an empty box; `isEmpty()` reports the state; `get()` on an empty box throws `NoSuchElementException`",
                "`orElse(fallback)` returns the value or the fallback",
                "`map(fn)` returns a `Box<R>`; an empty box stays empty and a function returning `null` yields an empty box; the signature must be `Function<? super T, ? extends R>`",
                "`equals`/`hashCode` are value-based and `toString` is `Box[value]` or `Box.empty`",
                "`Box<String>` and `Box<Integer>` have the same runtime class (observable erasure)",
            ],
            ["`of(null)` -> `NullPointerException`", "mapping an empty box never calls the function", "function returning null -> empty box", "`equals` between empty boxes is true; between empty and non-empty is false"],
            {"Box.java": r'''package @PKG@;

import java.util.NoSuchElementException;
import java.util.Objects;
import java.util.function.Function;

/** Immutable container holding zero or one non-null value. */
public final class Box<T> {

    private final T value;

    private Box(T value) {
        this.value = value;
    }

    public static <T> Box<T> of(T value) {
        //@TODO of | return a box holding value; throw NullPointerException when value is null
        Objects.requireNonNull(value, "value");
        return new Box<>(value);
        //@END
    }

    public static <T> Box<T> empty() {
        //@TODO empty | return an empty box (a box that holds no value)
        return new Box<>(null);
        //@END
    }

    public boolean isEmpty() {
        //@TODO isEmpty | return true when the box holds no value
        return value == null;
        //@END
    }

    public T get() {
        //@TODO get | return the value; throw NoSuchElementException when the box is empty
        if (value == null) {
            throw new NoSuchElementException("empty box");
        }
        return value;
        //@END
    }

    public T orElse(T fallback) {
        //@TODO orElse | return the value, or fallback when the box is empty
        return value != null ? value : fallback;
        //@END
    }

    public <R> Box<R> map(Function<? super T, ? extends R> fn) {
        //@TODO map | apply fn to the value and wrap the result; empty stays empty; a null result gives an empty box; never call fn on an empty box
        if (value == null) {
            return empty();
        }
        R result = fn.apply(value);
        return result == null ? empty() : new Box<>(result);
        //@END
    }

    @Override
    public boolean equals(Object o) {
        //@TODO equals | two boxes are equal when both are empty or hold equal values; use pattern matching or getClass
        if (this == o) {
            return true;
        }
        return o instanceof Box<?> other && Objects.equals(value, other.value);
        //@END
    }

    @Override
    public int hashCode() {
        //@TODO hashCode | consistent with equals (Objects.hashCode(value))
        return Objects.hashCode(value);
        //@END
    }

    @Override
    public String toString() {
        //@TODO toString | return "Box[value]" for a full box and "Box.empty" for an empty one
        return value == null ? "Box.empty" : "Box[" + value + "]";
        //@END
    }
}
'''},
            {"BoxTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.NoSuchElementException;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Function;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class BoxTest {

    @Test
    @DisplayName("of() wraps a value and rejects null")
    void r1_of() {
        Box<String> box = Box.of("hi");
        assertThat(box.get()).isEqualTo("hi");
        assertThatThrownBy(() -> Box.of(null)).isInstanceOf(NullPointerException.class);
    }

    @Test
    void r2_emptyBoxBehavior() {
        Box<String> empty = Box.empty();
        assertThat(empty.isEmpty()).isTrue();
        assertThat(Box.of(1).isEmpty()).isFalse();
        assertThatThrownBy(empty::get).isInstanceOf(NoSuchElementException.class);
    }

    @Test
    void r3_orElse() {
        assertThat(Box.of("a").orElse("z")).isEqualTo("a");
        assertThat(Box.<String>empty().orElse("z")).isEqualTo("z");
    }

    @Test
    void r4_mapTransformsValue() {
        Box<Integer> length = Box.of("hello").map(String::length);
        assertThat(length.get()).isEqualTo(5);
    }

    @Test
    void r4_mapAcceptsWiderFunction() {
        Function<Object, CharSequence> describe = o -> "<" + o + ">";
        Box<CharSequence> result = Box.of(42).map(describe);
        assertThat(result.get().toString()).isEqualTo("<42>");
    }

    @Test
    void r4_mapOnEmptyNeverCallsFunction() {
        AtomicInteger calls = new AtomicInteger();
        Box<Integer> result = Box.<String>empty().map(s -> {
            calls.incrementAndGet();
            return s.length();
        });
        assertThat(result.isEmpty()).isTrue();
        assertThat(calls).hasValue(0);
    }

    @Test
    void r4_mapReturningNullGivesEmpty() {
        Box<String> result = Box.of("x").map(s -> (String) null);
        assertThat(result.isEmpty()).isTrue();
    }

    @Test
    void r5_equalsHashCodeToString() {
        assertThat(Box.of("a")).isEqualTo(Box.of("a")).hasSameHashCodeAs(Box.of("a"));
        assertThat(Box.of("a")).isNotEqualTo(Box.of("b"));
        assertThat(Box.empty()).isEqualTo(Box.empty()).isNotEqualTo(Box.of(1));
        assertThat(Box.of(7).toString()).isEqualTo("Box[7]");
        assertThat(Box.empty().toString()).isEqualTo("Box.empty");
    }

    @Test
    @DisplayName("Erasure: Box<String> and Box<Integer> are the same runtime class")
    void r6_erasure() {
        Box<String> s = Box.of("a");
        Box<Integer> i = Box.of(1);
        assertThat(s.getClass()).isSameAs(i.getClass()).isSameAs(Box.class);
    }
}
'''},
            ["Make the constructor private and keep `value` final; use `null` internally to mean empty.", "`map` can reuse `empty()`; for `equals` compare `Objects.equals(value, other.value)`."],
            ["`map` uses `Function<? super T, ? extends R>` (PECS)", "No raw types or unchecked warnings", "Immutability preserved (no setters)"],
        ),
        task(
            "bounded-max", "Bounded Max/Min/Clamp", "Core", "BoundedMath",
            "Write generic numeric and ordering helpers using bounded type parameters: `max`, `min` over lists of comparables (including subclasses of a comparable parent), `clamp` for number-and-comparable types, and a `sum` over any `Collection<? extends Number>`.",
            [
                "`max(List)` returns the greatest element by natural order; empty or null list throws `IllegalArgumentException`",
                "`min(List)` returns the smallest element; same validation",
                "`max`/`min` signatures use `T extends Comparable<? super T>` so `List<Dog>` works when `Dog extends Animal implements Comparable<Animal>`",
                "`clamp(value, lo, hi)` constrains a value into `[lo, hi]` for `T extends Number & Comparable<T>`; `lo > hi` throws `IllegalArgumentException`",
                "`sum(Collection<? extends Number>)` adds `doubleValue()`s and treats an empty collection as `0.0`",
            ],
            ["empty list, null list", "single-element list", "lo == hi in clamp", "a `List<Integer>` and a `List<Double>` both accepted by `sum`"],
            {"BoundedMath.java": r'''package @PKG@;

import java.util.Collection;
import java.util.List;

/** Generic helpers that rely on bounded type parameters. */
public final class BoundedMath {

    private BoundedMath() {
    }

    public static <T extends Comparable<? super T>> T max(List<? extends T> items) {
        //@TODO max | return the greatest element (compareTo); IllegalArgumentException when items is null or empty
        if (items == null || items.isEmpty()) {
            throw new IllegalArgumentException("items must not be null or empty");
        }
        T best = items.get(0);
        for (T item : items) {
            if (item.compareTo(best) > 0) {
                best = item;
            }
        }
        return best;
        //@END
    }

    public static <T extends Comparable<? super T>> T min(List<? extends T> items) {
        //@TODO min | return the smallest element (compareTo); IllegalArgumentException when items is null or empty
        if (items == null || items.isEmpty()) {
            throw new IllegalArgumentException("items must not be null or empty");
        }
        T best = items.get(0);
        for (T item : items) {
            if (item.compareTo(best) < 0) {
                best = item;
            }
        }
        return best;
        //@END
    }

    public static <T extends Number & Comparable<T>> T clamp(T value, T lo, T hi) {
        //@TODO clamp | return lo if value < lo, hi if value > hi, else value; IllegalArgumentException when lo > hi
        if (lo.compareTo(hi) > 0) {
            throw new IllegalArgumentException("lo must be <= hi");
        }
        if (value.compareTo(lo) < 0) {
            return lo;
        }
        if (value.compareTo(hi) > 0) {
            return hi;
        }
        return value;
        //@END
    }

    public static double sum(Collection<? extends Number> numbers) {
        //@TODO sum | add doubleValue() of every element; empty collection gives 0.0
        double total = 0;
        for (Number n : numbers) {
            total += n.doubleValue();
        }
        return total;
        //@END
    }
}
'''},
            {"BoundedMathTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

class BoundedMathTest {

    static class Animal implements Comparable<Animal> {
        final int weight;

        Animal(int weight) {
            this.weight = weight;
        }

        @Override
        public int compareTo(Animal o) {
            return Integer.compare(weight, o.weight);
        }
    }

    static class Dog extends Animal {
        Dog(int weight) {
            super(weight);
        }
    }

    @Test
    void r1_maxOfStringsAndIntegers() {
        assertThat(BoundedMath.max(List.of("pear", "apple", "zoo", "kiwi"))).isEqualTo("zoo");
        assertThat(BoundedMath.max(List.of(3, 9, -2))).isEqualTo(9);
        assertThat(BoundedMath.max(List.of(5))).isEqualTo(5);
    }

    @Test
    void r1_maxRejectsNullAndEmpty() {
        assertThatThrownBy(() -> BoundedMath.max(List.<Integer>of())).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> BoundedMath.max((List<Integer>) null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r2_minOfStringsAndDoubles() {
        assertThat(BoundedMath.min(List.of("pear", "apple", "zoo"))).isEqualTo("apple");
        assertThat(BoundedMath.min(List.of(2.5, -1.0, 7.0))).isEqualTo(-1.0);
        assertThatThrownBy(() -> BoundedMath.min(new ArrayList<Integer>())).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r3_worksForSubclassOfComparableParent() {
        Dog light = new Dog(10);
        Dog heavy = new Dog(30);
        Dog result = BoundedMath.max(List.of(light, heavy));
        assertThat(result).isSameAs(heavy);
        assertThat(BoundedMath.min(List.of(light, heavy))).isSameAs(light);
    }

    @Test
    void r4_clamp() {
        assertThat(BoundedMath.clamp(5, 1, 10)).isEqualTo(5);
        assertThat(BoundedMath.clamp(-4, 0, 10)).isEqualTo(0);
        assertThat(BoundedMath.clamp(99, 0, 10)).isEqualTo(10);
        assertThat(BoundedMath.clamp(2.5, 2.5, 2.5)).isEqualTo(2.5);
    }

    @Test
    void r4_clampRejectsInvertedRange() {
        assertThatThrownBy(() -> BoundedMath.clamp(5, 10, 1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r5_sumAcceptsAnyNumberCollection() {
        assertThat(BoundedMath.sum(List.of(1, 2, 3))).isEqualTo(6.0);
        assertThat(BoundedMath.sum(List.of(1.5, 2.5))).isEqualTo(4.0);
        assertThat(BoundedMath.sum(Set.of(10L))).isEqualTo(10.0);
        assertThat(BoundedMath.sum(List.<Number>of())).isEqualTo(0.0);
    }
}
'''},
            ["Seed `best` with the first element, then scan with `compareTo`.", "For `clamp`, validate the range first so `lo > hi` fails even when `value` is in range."],
            ["Signatures use `Comparable<? super T>` and `List<? extends T>` exactly as described", "No casts to `Comparable` or `Object`"],
        ),
        task(
            "pecs-copy", "PECS Copy Utilities", "Core", "Pecs",
            "Implement collection utilities whose signatures apply PECS correctly, so they accept subtype sources and supertype destinations. Includes a wildcard-capture helper.",
            [
                "`copy(dst, src)` appends every element of `src` (`List<? extends T>`) to `dst` (`List<? super T>`)",
                "`moveAll(src, dst)` moves all elements from `Collection<? extends T>` into `Collection<? super T>` and leaves `src` empty",
                "`fill(dst, value, n)` adds `n` copies of `value` to a `List<? super T>`; negative `n` throws `IllegalArgumentException`",
                "`firstOrDefault(src, def)` returns the first element of a `List<? extends T>` or `def` when empty",
                "`swap(List<?> list, int i, int j)` swaps two elements using a private capture helper",
            ],
            ["empty source", "negative count in fill", "swap with equal indexes is a no-op", "out-of-range swap index raises `IndexOutOfBoundsException` (from the list)"],
            {"Pecs.java": r'''package @PKG@;

import java.util.Collection;
import java.util.List;

/** Utilities demonstrating Producer-Extends / Consumer-Super. */
public final class Pecs {

    private Pecs() {
    }

    public static <T> void copy(List<? super T> dst, List<? extends T> src) {
        //@TODO copy | append every element of src to dst; src is a producer (extends), dst a consumer (super)
        for (T item : src) {
            dst.add(item);
        }
        //@END
    }

    public static <T> void moveAll(Collection<? extends T> src, Collection<? super T> dst) {
        //@TODO moveAll | add every element of src to dst, then clear src
        dst.addAll(src);
        src.clear();
        //@END
    }

    public static <T> void fill(List<? super T> dst, T value, int n) {
        //@TODO fill | add n copies of value to dst; IllegalArgumentException when n is negative
        if (n < 0) {
            throw new IllegalArgumentException("n must be >= 0");
        }
        for (int i = 0; i < n; i++) {
            dst.add(value);
        }
        //@END
    }

    public static <T> T firstOrDefault(List<? extends T> src, T def) {
        //@TODO firstOrDefault | return src.get(0), or def when src is empty
        return src.isEmpty() ? def : src.get(0);
        //@END
    }

    public static void swap(List<?> list, int i, int j) {
        //@TODO swap | delegate to the private generic helper swapHelper(list, i, j) (wildcard capture)
        swapHelper(list, i, j);
        //@END
    }

    private static <E> void swapHelper(List<E> list, int i, int j) {
        E tmp = list.get(i);
        list.set(i, list.get(j));
        list.set(j, tmp);
    }
}
'''},
            {"PecsTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

class PecsTest {

    @Test
    void r1_copyIntegersIntoNumberList() {
        List<Number> dst = new ArrayList<>(List.of(0.5));
        List<Integer> src = List.of(1, 2, 3);
        Pecs.copy(dst, src);
        assertThat(dst).containsExactly(0.5, 1, 2, 3);
    }

    @Test
    void r1_copyIntoObjectListAndEmptySource() {
        List<Object> dst = new ArrayList<>(List.of("x"));
        Pecs.copy(dst, List.of("a", "b"));
        Pecs.copy(dst, List.<Integer>of());
        assertThat(dst).containsExactly("x", "a", "b");
    }

    @Test
    void r2_moveAllEmptiesSource() {
        List<Integer> src = new ArrayList<>(List.of(4, 5));
        Collection<Number> dst = new ArrayList<>(List.of(1.5));
        Pecs.moveAll(src, dst);
        assertThat(src).isEmpty();
        assertThat(dst).containsExactly(1.5, 4, 5);
    }

    @Test
    void r2_moveAllIntoSet() {
        Set<String> src = new HashSet<>(Set.of("a", "b"));
        Set<Object> dst = new HashSet<>();
        Pecs.moveAll(src, dst);
        assertThat(src).isEmpty();
        assertThat(dst).containsExactlyInAnyOrder("a", "b");
    }

    @Test
    void r3_fill() {
        List<Number> dst = new ArrayList<>();
        Pecs.fill(dst, 7, 3);
        assertThat(dst).containsExactly(7, 7, 7);
        List<Object> objs = new ArrayList<>();
        Pecs.fill(objs, "z", 0);
        assertThat(objs).isEmpty();
    }

    @Test
    void r3_fillRejectsNegative() {
        List<Object> dst = new ArrayList<>();
        assertThatThrownBy(() -> Pecs.fill(dst, "x", -1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r4_firstOrDefault() {
        Number n = Pecs.firstOrDefault(List.of(10, 20), 0.5);
        assertThat(n).isEqualTo(10);
        Number fallback = Pecs.firstOrDefault(List.<Integer>of(), 0.5);
        assertThat(fallback).isEqualTo(0.5);
    }

    @Test
    void r5_swapWorksOnAnyListType() {
        List<String> strings = new ArrayList<>(List.of("a", "b", "c"));
        Pecs.swap(strings, 0, 2);
        assertThat(strings).containsExactly("c", "b", "a");

        List<Integer> ints = new ArrayList<>(List.of(1, 2));
        Pecs.swap(ints, 1, 1);
        assertThat(ints).containsExactly(1, 2);
    }

    @Test
    void r5_swapOutOfRange() {
        List<String> strings = new ArrayList<>(List.of("a"));
        assertThatThrownBy(() -> Pecs.swap(strings, 0, 3)).isInstanceOf(IndexOutOfBoundsException.class);
    }
}
'''},
            ["`swap(List<?>, ...)` itself cannot call `list.set(i, list.get(j))` - delegate to a generic helper so the compiler can name the captured type.", "`moveAll`'s `src.clear()` is legal even though `src` is `? extends T` because `clear` does not take a `T`."],
            ["Producers use `? extends`, consumers `? super` - no unnecessary invariant parameters", "Wildcard capture helper used instead of raw types/casts"],
        ),
        task(
            "generic-stack", "Generic Array-Backed Stack", "Challenge", "ArrayStack",
            "Build `ArrayStack<E>`, a growable LIFO stack on an internal `Object[]`. It must be safe for callers (generics, PECS bulk operations), iterable top-to-bottom, and it contains the one legitimate unchecked cast in the course (reading from `Object[]`). **Challenge:** explain in a comment why the cast is safe.",
            [
                "Constructor `ArrayStack(int initialCapacity)` rejects capacity <= 0 with `IllegalArgumentException`; `ArrayStack()` uses 4",
                "`push`, `pop`, `peek`, `size`, `isEmpty` follow LIFO semantics; `pop`/`peek` on an empty stack throw `NoSuchElementException`",
                "The backing array grows (doubling) when full, and popped slots are nulled to avoid memory leaks",
                "`pushAll(Iterable<? extends E>)` pushes in iteration order",
                "`popAll(Collection<? super E>)` pops everything into the sink in pop order and returns the count",
                "`iterator()` walks from top to bottom without modifying the stack; calling `next()` past the end throws `NoSuchElementException`",
            ],
            ["capacity 0 or negative", "growth well beyond initial capacity", "pop on empty", "iterating an empty stack", "pushAll of a `List<Integer>` into `ArrayStack<Number>`"],
            {"ArrayStack.java": r'''package @PKG@;

import java.util.Collection;
import java.util.Iterator;
import java.util.NoSuchElementException;

/** Growable LIFO stack backed by an Object[]. */
public class ArrayStack<E> implements Iterable<E> {

    private Object[] elements;
    private int size;

    public ArrayStack() {
        this(4);
    }

    public ArrayStack(int initialCapacity) {
        //@TODO constructor | reject initialCapacity <= 0 with IllegalArgumentException, else allocate the backing array
        if (initialCapacity <= 0) {
            throw new IllegalArgumentException("initialCapacity must be > 0");
        }
        this.elements = new Object[initialCapacity];
        //@END
    }

    public void push(E item) {
        //@TODO push | grow the array (double) when full, then store item on top
        if (size == elements.length) {
            elements = java.util.Arrays.copyOf(elements, elements.length * 2);
        }
        elements[size++] = item;
        //@END
    }

    @SuppressWarnings("unchecked")
    public E pop() {
        //@TODO pop | remove and return the top element, null out the slot; NoSuchElementException when empty
        if (size == 0) {
            throw new NoSuchElementException("stack is empty");
        }
        // Safe: only push(E) ever stores into elements, so every non-null slot holds an E.
        E top = (E) elements[--size];
        elements[size] = null;
        return top;
        //@END
    }

    @SuppressWarnings("unchecked")
    public E peek() {
        //@TODO peek | return the top element without removing it; NoSuchElementException when empty
        if (size == 0) {
            throw new NoSuchElementException("stack is empty");
        }
        return (E) elements[size - 1];
        //@END
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public void pushAll(Iterable<? extends E> source) {
        //@TODO pushAll | push every element of source in iteration order (source is a producer)
        for (E e : source) {
            push(e);
        }
        //@END
    }

    public int popAll(Collection<? super E> sink) {
        //@TODO popAll | pop every element into sink (consumer) in pop order and return how many were moved
        int moved = 0;
        while (!isEmpty()) {
            sink.add(pop());
            moved++;
        }
        return moved;
        //@END
    }

    @Override
    public Iterator<E> iterator() {
        //@TODO iterator | return an Iterator that walks top to bottom; next() past the end throws NoSuchElementException; remove() is unsupported
        return new Iterator<>() {
            private int index = size - 1;

            @Override
            public boolean hasNext() {
                return index >= 0;
            }

            @Override
            @SuppressWarnings("unchecked")
            public E next() {
                if (index < 0) {
                    throw new NoSuchElementException();
                }
                return (E) elements[index--];
            }
        };
        //@END
    }
}
'''},
            {"ArrayStackTest.java": r'''package @PKG@;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import org.junit.jupiter.api.Test;

class ArrayStackTest {

    @Test
    void r1_constructorValidation() {
        assertThatThrownBy(() -> new ArrayStack<String>(0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new ArrayStack<String>(-3)).isInstanceOf(IllegalArgumentException.class);
        assertThat(new ArrayStack<String>().isEmpty()).isTrue();
    }

    @Test
    void r2_lifoOrder() {
        ArrayStack<String> stack = new ArrayStack<>();
        stack.push("a");
        stack.push("b");
        assertThat(stack.size()).isEqualTo(2);
        assertThat(stack.peek()).isEqualTo("b");
        assertThat(stack.pop()).isEqualTo("b");
        assertThat(stack.pop()).isEqualTo("a");
        assertThat(stack.isEmpty()).isTrue();
    }

    @Test
    void r2_emptyStackThrows() {
        ArrayStack<Integer> stack = new ArrayStack<>();
        assertThatThrownBy(stack::pop).isInstanceOf(java.util.NoSuchElementException.class);
        assertThatThrownBy(stack::peek).isInstanceOf(java.util.NoSuchElementException.class);
    }

    @Test
    void r3_growsBeyondInitialCapacity() {
        ArrayStack<Integer> stack = new ArrayStack<>(1);
        for (int i = 0; i < 1_000; i++) {
            stack.push(i);
        }
        assertThat(stack.size()).isEqualTo(1_000);
        for (int i = 999; i >= 0; i--) {
            assertThat(stack.pop()).isEqualTo(i);
        }
    }

    @Test
    void r4_pushAllAcceptsSubtypeSource() {
        ArrayStack<Number> stack = new ArrayStack<>();
        List<Integer> source = List.of(1, 2, 3);
        stack.pushAll(source);
        assertThat(stack.pop()).isEqualTo(3);
        assertThat(stack.size()).isEqualTo(2);
    }

    @Test
    void r5_popAllIntoSupertypeSink() {
        ArrayStack<Integer> stack = new ArrayStack<>();
        stack.pushAll(List.of(1, 2, 3));
        List<Object> sink = new ArrayList<>();
        int moved = stack.popAll(sink);
        assertThat(moved).isEqualTo(3);
        assertThat(sink).containsExactly(3, 2, 1);
        assertThat(stack.isEmpty()).isTrue();
        assertThat(stack.popAll(sink)).isZero();
    }

    @Test
    void r6_iteratorWalksTopToBottomWithoutMutating() {
        ArrayStack<String> stack = new ArrayStack<>();
        stack.push("x");
        stack.push("y");
        stack.push("z");
        List<String> seen = new ArrayList<>();
        for (String s : stack) {
            seen.add(s);
        }
        assertThat(seen).containsExactly("z", "y", "x");
        assertThat(stack.size()).isEqualTo(3);
    }

    @Test
    void r6_iteratorEdgeCases() {
        ArrayStack<String> stack = new ArrayStack<>();
        Iterator<String> empty = stack.iterator();
        assertThat(empty.hasNext()).isFalse();
        assertThatThrownBy(empty::next).isInstanceOf(java.util.NoSuchElementException.class);
        stack.push("only");
        Iterator<String> it = stack.iterator();
        assertThat(it.next()).isEqualTo("only");
        assertThatThrownBy(it::next).isInstanceOf(java.util.NoSuchElementException.class);
    }
}
'''},
            ["Nulling `elements[size]` after `pop` prevents *loitering* references (a memory leak).", "In the iterator, capture `size` at creation or read it live - either passes the tests; explain your choice in a comment."],
            ["Exactly one justified unchecked cast pattern, annotated and commented", "Bulk operations use PECS signatures", "Popped slots are cleared"],
            constraints=["Do not use `java.util.ArrayList`, `Stack`, `Deque` or any collection as the backing store - use `Object[]`", "Do not edit the tests"],
        ),
    ],
)
