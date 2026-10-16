# Day 02 — Primitives, References, Variables, Scope, var, and GC Basics

**Phase:** Core Java  
**Day:** 02  
**Verify tasks with:** `mvn test`

## Overview

This day focuses on **Primitives, References, Variables, Scope, var, and GC Basics**. Read each section, try the self-test questions, then complete the practical tasks in order.

## Day roadmap

1. Primitive types
2. References vs primitives
3. Declaration, initialization, and scope
4. `var` local-variable type inference
5. Garbage collection basics

## Primitive types

`byte`, `short`, `int`, `long`, `float`, `double`, `char`, `boolean`. Integer literals default to `int`; use `L` for long. Floating defaults to `double`; use `f` for float. `char` is UTF-16 code unit. Prefer `int`/`long`/`double`/`boolean` in application code.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Primitive types**?
2. What bug appears if you misuse this concept?

## References vs primitives

Primitives store values; references store addresses (or null). Assigning a reference copies the pointer, not the object. Two references can point to the same object — mutations are visible through both.

### Quick checks (self-test)

1. In your own words, what is the main idea of **References vs primitives**?
2. What bug appears if you misuse this concept?

## Declaration, initialization, and scope

Local variables must be definitely assigned before use. Instance/static fields get defaults (0, false, null). Scope is block-based. Shadowing is allowed but confusing — avoid in course code.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Declaration, initialization, and scope**?
2. What bug appears if you misuse this concept?

## `var` local-variable type inference

`var` requires an initializer and cannot be used for fields or method parameters. The inferred type is fixed at compile time — not dynamic typing.

### Quick checks (self-test)

1. In your own words, what is the main idea of **`var` local-variable type inference**?
2. What bug appears if you misuse this concept?

## Garbage collection basics

Objects become eligible when unreachable. You cannot force collection. `finalize` is deprecated/removed for practical use — never rely on it.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Garbage collection basics**?
2. What bug appears if you misuse this concept?

## Common mistakes & debugging

- Reading theory without running `mvn test` on the warm-up task first.
- Mixing up compile-time types with runtime behavior.
- Ignoring exception messages from failing tests.

## Interview angles

- Explain the key idea behind Primitives, References, Variables, Scope, var, and GC Basics.
- What production bug have you seen (or can imagine) related to today's topic?

## Further reading

- Oracle Java Tutorials (matching topic)
- Java Language Specification sections referenced in interviews
- OCA Java SE 8 Programmer I Study Guide — overlapping chapters (update mentally to Java 21 where APIs differ)

## Glossary

| Term | Meaning |
|------|---------|
| Day 02 focus | Primitives, References, Variables, Scope, var, and GC Basics |
| `mvn test` | Compile + run JUnit 5 tests |

## Answers (self-test)

Compare your answers against the theory sections above. Re-read any section you could not explain out loud in 60 seconds.
