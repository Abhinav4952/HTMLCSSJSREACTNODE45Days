# Day 13 — Generics: Classes, Methods, Bounds, and Wildcards (PECS)

**Phase:** Core Java  
**Primary theme:** Write type-safe reusable code with generic classes/methods, bounded type parameters, and wildcards.  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-box-generic`, `task-02-bounded-max`, `task-03-pecs-copy`, `task-04-generic-stack`  
**Instruction alignment:** Maps to the Day 13 entry of the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21 (no Spring today)

## Overview

Generics let one class or method work for many types while the **compiler** proves that you never put a `String` where an `Integer` belongs. Before Java 5 every collection held `Object`, so you cast on the way out and discovered mistakes as `ClassCastException` in production. Generics move that failure to compile time.

In backend work you meet generics everywhere: `List<Order>`, `Map<String, Customer>`, `Optional<T>`, `Comparator<T>`, Spring's `ResponseEntity<T>`, repositories like `JpaRepository<Order, Long>`, and your own utility methods (`<T> T firstOrThrow(List<T>)`). Interviewers love three questions: *what is type erasure*, *why can't I do `List<Object> x = new ArrayList<String>()`*, and *explain PECS*. Today you answer all three in code.

## Day roadmap

1. Generic classes, generic methods, and type erasure
2. Bounded type parameters and intersection bounds
3. Wildcards and the PECS rule
4. Interview angles
5. Common mistakes & debugging
6. Further reading, glossary, answers

### Generic classes, generic methods, and type erasure

#### What it is

A **generic class** declares one or more *type parameters* in angle brackets (`class Box<T>`). Callers supply *type arguments* (`Box<String>`). A **generic method** declares its own parameters before the return type (`static <T> T first(List<T> xs)`) and the compiler usually *infers* them from the arguments. Mental model: a generic type is a **template the compiler stamps checks from**; at runtime only one `Box.class` exists because of **type erasure** — the compiler removes type arguments, inserts casts where needed, and generates bridge methods.

#### Why it exists / why it matters

Without generics, reusable containers store `Object`, forcing casts and risking `ClassCastException`. Generics give compile-time safety, remove casts, and make APIs self-documenting (`Map<UserId, List<Order>>` tells a reader everything). Erasure exists for **backward compatibility**: pre-Java-5 bytecode and libraries keep working unchanged. Real problems solved: type-safe DAOs, result wrappers, caches, event buses.

#### Pros and cons

**Pros**

- Compile-time type safety eliminates a whole class of `ClassCastException` bugs
- No casts at call sites; code reads cleaner
- One implementation serves many types (less duplication)
- Self-documenting APIs and better IDE completion

**Cons / tradeoffs**

- Erasure removes type info at runtime: no `new T()`, no `T[] a = new T[n]`, no `instanceof List<String>`
- Primitives cannot be type arguments (`List<int>` is illegal) so boxing cost and null-unboxing risk appear
- Generic compiler errors can be cryptic until you learn to read capture types

#### What happens without it / when misused

**Raw types** (`List list = new ArrayList();`) turn the checks off: `list.add(42)` into a `List<String>` compiles with an *unchecked* warning and explodes later as `ClassCastException` at a distant line (**heap pollution**). Treating `List<Dog>` as a `List<Animal>` is rejected by the compiler for good reason: otherwise `animals.add(new Cat())` would corrupt the dog list. Overloads that differ only in type arguments (`void f(List<String>)` / `void f(List<Integer>)`) clash after erasure (*name clash: same erasure*).

#### Syntax and rules

- Type-parameter naming convention: `T` (type), `E` (element), `K`/`V` (key/value), `R` (result), `N` (number).
- Diamond: `Box<String> b = new Box<>("x");` lets the compiler infer the right-hand type arguments.
- Generic method call with explicit witness (rare): `Util.<String>empty()`.
- **Invariance:** `List<Dog>` is **not** a subtype of `List<Animal>` even though `Dog extends Animal`. Arrays *are* covariant (`Dog[]` is an `Animal[]`) and that is a known design wart (`ArrayStoreException`).
- Static members cannot use the class's type parameter; static generic methods declare their own `<T>`.
- Reifiable types (`String`, `List<?>`, raw `List`, primitives) are fully available at runtime; `List<String>` is not.

#### Examples

**Example 1.1 — Tiny — generic class**

```java
class Box<T> {
    private final T value;
    Box(T value) { this.value = value; }
    T get() { return value; }
}
Box<String> b = new Box<>("hi");
String s = b.get();          // no cast needed
// Box<String> bad = new Box<>(42);   // compile error
```

**Example 1.2 — Tiny — generic method with inference**

```java
static <T> T firstOrDefault(java.util.List<T> xs, T def) {
    return xs.isEmpty() ? def : xs.get(0);
}
String s = firstOrDefault(java.util.List.of("a", "b"), "z");  // T = String
Integer n = firstOrDefault(java.util.List.of(), 7);            // T = Integer
System.out.println(s + n); // a7
```

**Example 1.3 — Medium — erasure observed at runtime**

```java
import java.util.*;

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
// CCE at read time, not at add time
```

#### Quick checks

1. Why does `List<Object> xs = new ArrayList<String>();` not compile?
2. What does `new ArrayList<String>().getClass() == new ArrayList<Integer>().getClass()` print and why?
3. Why can't you write `new T()` or `new T[10]` inside a generic class?
4. Give two reasons `List<int>` is illegal.

### Bounded type parameters and intersection bounds

#### What it is

A **bounded type parameter** restricts what callers may supply: `<T extends Comparable<T>>` means *T must be comparable with itself*. `extends` is used for classes and interfaces alike. Multiple bounds form an **intersection**: `<T extends Number & Comparable<T>>` (class bound first, then interfaces). Inside the method you may call any method of the bounds on a `T`. The recursive bound `<T extends Comparable<T>>` is the standard way to say *this type has a natural order*.

#### Why it exists / why it matters

Without a bound `T` is just `Object`, so you cannot compare, add, or call domain methods. Bounds express **capabilities** and keep the method body free of casts and `instanceof`. `Collections.max(Collection<? extends T>)` has the bound `<T extends Object & Comparable<? super T>>`, which is the same idea in its most flexible form.

#### Pros and cons

**Pros**

- Lets generic code call bound methods (`compareTo`, `doubleValue`) safely
- Errors move to compile time: passing a non-comparable type is rejected
- Documents intent in the signature
- `Comparable<? super T>` makes subclasses of a comparable parent work

**Cons / tradeoffs**

- Signatures get long and harder to read
- Recursive bounds are conceptually tricky
- A bound cannot be a type *variable* with a lower bound (`<T super X>` does not exist)

#### What happens without it / when misused

Using `<T extends Comparable>` (raw bound) compiles with warnings and loses safety. Using `<T extends Comparable<T>>` instead of `Comparable<? super T>` rejects `Dog extends Animal implements Comparable<Animal>` - a legitimate type - producing the confusing error *inferred type does not conform to upper-bound*. Forgetting that the **class** bound must come first in an intersection gives a compile error.

#### Syntax and rules

- `<T extends Number>`: T is `Number` or a subtype (`Integer`, `Double`).
- `<T extends Number & Comparable<T>>`: at most one class, first; any number of interfaces after `&`.
- Prefer `<T extends Comparable<? super T>>` for max/min/sort helpers.
- Bounds also apply to class declarations: `class Stats<N extends Number> { ... }`.
- A bounded `T` is erased to its **leftmost bound** (so the example above erases to `Number`).

#### Examples

**Example 2.1 — Tiny — upper bound**

```java
static <N extends Number> double sum(java.util.List<N> xs) {
    double total = 0;
    for (N n : xs) total += n.doubleValue();   // allowed: N is a Number
    return total;
}
System.out.println(sum(java.util.List.of(1, 2, 3)));      // 6.0
System.out.println(sum(java.util.List.of(1.5, 2.5)));     // 4.0
```

**Example 2.2 — Tiny — max with the flexible Comparable bound**

```java
static <T extends Comparable<? super T>> T max(java.util.List<? extends T> xs) {
    T best = xs.get(0);
    for (T x : xs) if (x.compareTo(best) > 0) best = x;
    return best;
}
// max(List.of("pear", "apple", "zoo")) -> "zoo"
```

**Example 2.3 — Medium — why `? super T` matters in the bound**

```java
class Animal implements Comparable<Animal> {
    final int weight;
    Animal(int w) { weight = w; }
    public int compareTo(Animal o) { return Integer.compare(weight, o.weight); }
}
class Dog extends Animal { Dog(int w) { super(w); } }

// With <T extends Comparable<T>> this call FAILS: Dog is Comparable<Animal>, not Comparable<Dog>.
// With <T extends Comparable<? super T>> it compiles:
Dog heaviest = max(java.util.List.of(new Dog(10), new Dog(30)));  // uses Animal.compareTo
```

#### Quick checks

1. Why must the class bound come first in `<T extends Number & Comparable<T>>`?
2. What is the erasure of `<T extends Comparable<T>> T max(T a, T b)`?
3. When do you prefer `Comparable<? super T>` over `Comparable<T>`?

### Wildcards and the PECS rule

#### What it is

A **wildcard** `?` stands for an *unknown* type. `List<? extends Number>` is a list of *some* subtype of Number (a **producer**: you can read `Number`s out). `List<? super Integer>` is a list of *some* supertype of Integer (a **consumer**: you can write `Integer`s in). `List<?>` means *anything*, read-only as `Object`. **PECS = Producer `extends`, Consumer `super`** (Joshua Bloch, *Effective Java* item 31).

#### Why it exists / why it matters

Invariance (`List<Dog>` is not a `List<Animal>`) makes APIs too rigid. Wildcards restore flexibility **without** losing safety: a method that only *reads* numbers should accept `List<Integer>` and `List<Double>`; a method that only *adds* integers should accept `List<Number>` and `List<Object>`. This is how `Collections.copy(List<? super T> dest, List<? extends T> src)` is declared.

#### Pros and cons

**Pros**

- Maximizes API reusability while staying type-safe
- Communicates direction of data flow (in vs out) to callers
- Required to use the full power of the JDK collection utilities
- Wildcard capture lets one helper work on any `List<?>`

**Cons / tradeoffs**

- You cannot add to `List<? extends T>` (except `null`) - surprising at first
- Return types should **not** be wildcards; they push complexity onto callers
- Readability: nested wildcards (`Map<? extends K, ? extends List<? extends V>>`) are hard to parse

#### What happens without it / when misused

Writing `void addAll(List<Number> src, List<Number> dst)` forces callers to build a `List<Number>` and rejects `List<Integer>` - the API is invariant for no reason. Declaring `void print(List<? extends Number> xs)` and then calling `xs.add(1)` is a compile error (the compiler cannot prove the unknown subtype accepts Integer). Using raw `List` to dodge the problem re-opens the heap-pollution hole.

#### Syntax and rules

- **Get-Put principle:** read only -> `? extends`; write only -> `? super`; both -> no wildcard (use `T` exactly).
- `List<?>`: you may call `size()`, `get(i)` (as `Object`), `clear()`, but cannot add anything but `null`.
- **Wildcard capture:** a private generic helper can name the unknown type:
  `static void swap(List<?> l, int i, int j) { swapHelper(l, i, j); }` and `private static <E> void swapHelper(List<E> l, int i, int j) {...}`.
- Wildcards are for **parameters**; do not use them in return types or on class declarations.
- Subtyping: `List<Integer>` <: `List<? extends Number>` <: `List<?>`; `List<Number>` <: `List<? super Integer>`.

#### Examples

**Example 3.1 — Tiny — producer extends**

```java
static double total(java.util.Collection<? extends Number> xs) {
    double t = 0;
    for (Number n : xs) t += n.doubleValue();
    return t;
}
// total(List.of(1, 2, 3)) == 6.0 ; total(List.of(1.5)) == 1.5
```

**Example 3.2 — Tiny — consumer super**

```java
static void fillWithInts(java.util.List<? super Integer> sink, int n) {
    for (int i = 0; i < n; i++) sink.add(i);   // OK: sink accepts Integer
}
java.util.List<Number> nums = new java.util.ArrayList<>();
java.util.List<Object> objs = new java.util.ArrayList<>();
fillWithInts(nums, 2);
fillWithInts(objs, 3);
System.out.println(nums + " " + objs);   // [0, 1] [0, 1, 2]
```

**Example 3.3 — Medium — PECS copy + wildcard capture**

```java
import java.util.*;

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
}
```

#### Quick checks

1. State PECS and give the JDK method that uses it.
2. Why does `List<? extends Number> xs; xs.add(1);` fail?
3. Which parameter type accepts `List<Integer>`, `List<Number>` and `List<Object>`?
4. Why is `List<?>` not the same as `List<Object>`?

## Interview angles

**Q: What is type erasure and what limitations does it cause?**

The compiler checks type arguments, then removes them, inserting casts and bridge methods. Consequences: no `new T()`, no generic arrays, no `instanceof List<String>`, overloads that differ only by type arguments clash, and runtime reflection sees raw types (except for generic *signatures* stored in class metadata).

**Q: Explain PECS with an example.**

If a parameter produces values you read, declare `? extends T`; if it consumes values you write, declare `? super T`. `Collections.copy(dest, src)` reads from `src` (`extends`) and writes into `dest` (`super`).

**Q: Why are arrays covariant but generics invariant?**

Arrays were designed before generics and check stores at runtime (`ArrayStoreException`). Generics are erased so runtime checks are impossible; invariance is the only way to keep compile-time safety.

**Q: `List<Object>` vs `List<?>` vs raw `List`?**

`List<Object>`: list of objects, invariant. `List<?>`: list of unknown type, read-only-ish and safe. Raw: unchecked legacy, disables checks.

**Q: What is a recursive bound and why use `Comparable<? super T>`?**

`T extends Comparable<T>` says T compares to itself; `? super T` also allows types that inherit comparability from a supertype.

**Q: What is heap pollution?**

A variable of a parameterized type refers to an object that is not of that type, usually via raw types or unchecked casts; it surfaces later as `ClassCastException`.

## Common mistakes & debugging

- Using raw types to "make the error go away" - you get `ClassCastException` later instead of a compile error now.
- Declaring `T extends Comparable<T>` and then being unable to call with a subclass whose parent defines `compareTo` (`inferred type does not conform to upper-bound`). Use `Comparable<? super T>`.
- Trying to `add` to a `List<? extends X>` parameter (`incompatible types: capture#1 of ? extends X`). You wanted `? super X` or an exact `T`.
- Returning wildcard types such as `List<? extends Number>` from a public API - callers cannot do much with it.
- Creating `new T[n]` (`generic array creation`); use `(T[]) new Object[n]` privately with a comment, or a `List<T>`.
- Confusing `static <T> void f(T x)` (generic method) with a class-level `T` - static members cannot see the class type parameter.

## Further reading

- Java Language Specification, ch. 4.5 (Parameterized Types), 4.6 (Type Erasure), 4.10 (Subtyping)
- Oracle Java Tutorials - *Generics* trail (bounded types, wildcards, erasure, restrictions)
- *Effective Java* (Bloch), items 26-33 (raw types, wildcards, generic methods, heterogeneous containers)
- Javadoc: `java.util.Collections#copy`, `#max`, `java.util.function.Function`

## Glossary

| Term | Meaning |
|------|---------|
| Type parameter | A placeholder such as `T` declared by a generic class or method |
| Type argument | The concrete type supplied by the caller (`String` in `Box<String>`) |
| Invariance | `G<A>` is not a subtype of `G<B>` even if `A <: B` |
| Type erasure | Compiler removal of type arguments, leaving casts and bridge methods |
| Reifiable type | A type whose full information exists at runtime (e.g. `String`, `List<?>`) |
| PECS | Producer `extends`, Consumer `super` |
| Wildcard capture | Compiler inference that gives a name to an unknown `?` so a helper can use it |
| Heap pollution | A parameterized variable pointing to an object of the wrong parameterization |

## Answers

Answers to every **Quick check** above (numbered `section.question`).

- **1.1** — Why does `List<Object> xs = new ArrayList<String>();` not compile?  
  Generics are invariant. If it compiled you could `xs.add(42)` and put an Integer into what is really an `ArrayList<String>`.

- **1.2** — What does `new ArrayList<String>().getClass() == new ArrayList<Integer>().getClass()` print and why?  
  `true`; type arguments are erased, only one `ArrayList` class exists at runtime.

- **1.3** — Why can't you write `new T()` or `new T[10]` inside a generic class?  
  `T` is erased to its bound (usually `Object`), so the JVM does not know which class to instantiate; pass a `Supplier<T>`/`Class<T>` or use `(T[]) new Object[n]` carefully.

- **1.4** — Give two reasons `List<int>` is illegal.  
  Type arguments must be reference types because erasure replaces `T` with `Object`/bound, which a primitive is not; use `List<Integer>` (autoboxing).

- **2.1** — Why must the class bound come first in `<T extends Number & Comparable<T>>`?  
  The language allows at most one class bound and it must be listed first; the rest must be interfaces.

- **2.2** — What is the erasure of `<T extends Comparable<T>> T max(T a, T b)`?  
  `Comparable max(Comparable a, Comparable b)` - the leftmost bound replaces `T`.

- **2.3** — When do you prefer `Comparable<? super T>` over `Comparable<T>`?  
  When subclasses inherit `compareTo` from a parent that is comparable to the parent type (e.g. `Dog` using `Animal.compareTo`).

- **3.1** — State PECS and give the JDK method that uses it.  
  Producer `extends`, Consumer `super`; `Collections.copy(List<? super T> dest, List<? extends T> src)`.

- **3.2** — Why does `List<? extends Number> xs; xs.add(1);` fail?  
  `xs` could really be a `List<Double>`; the compiler cannot guarantee an `Integer` fits, so only `null` may be added.

- **3.3** — Which parameter type accepts `List<Integer>`, `List<Number>` and `List<Object>`?  
  `List<? super Integer>` (consumer of Integers).

- **3.4** — Why is `List<?>` not the same as `List<Object>`?  
  `List<Object>` accepts any object but only `List<Object>` arguments; `List<?>` accepts a list of any type but allows no additions.
