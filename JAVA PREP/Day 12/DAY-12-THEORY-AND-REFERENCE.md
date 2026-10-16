# Day 12 — Wrappers, Autoboxing, Enums, and Nested Classes

**Phase:** Core Java  
**Day:** 12  
**Verify tasks with:** `mvn test`

## Overview

This day focuses on **Wrappers, Autoboxing, Enums, and Nested Classes**. Read each section, try the self-test questions, then complete the practical tasks in order.

## Day roadmap

1. Wrappers and autoboxing
2. Integer cache
3. Enums
4. Nested classes

## Wrappers and autoboxing

`Integer`, `Boolean`, etc. Autobox/unbox. Unboxing null → NPE. Prefer primitives in hot paths.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Wrappers and autoboxing**?
2. What bug appears if you misuse this concept?

## Integer cache

`Integer.valueOf` caches -128..127 by default — `==` may accidentally work; still use `equals`.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Integer cache**?
2. What bug appears if you misuse this concept?

## Enums

Type-safe constants. Can have fields, methods, abstract methods per constant.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Enums**?
2. What bug appears if you misuse this concept?

## Nested classes

Static nested, inner (has outer this), local, anonymous. Prefer static nested when no outer instance needed.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Nested classes**?
2. What bug appears if you misuse this concept?

## Common mistakes & debugging

- Reading theory without running `mvn test` on the warm-up task first.
- Mixing up compile-time types with runtime behavior.
- Ignoring exception messages from failing tests.

## Interview angles

- Explain the key idea behind Wrappers, Autoboxing, Enums, and Nested Classes.
- What production bug have you seen (or can imagine) related to today's topic?

## Further reading

- Oracle Java Tutorials (matching topic)
- Java Language Specification sections referenced in interviews
- OCA Java SE 8 Programmer I Study Guide — overlapping chapters (update mentally to Java 21 where APIs differ)

## Glossary

| Term | Meaning |
|------|---------|
| Day 12 focus | Wrappers, Autoboxing, Enums, and Nested Classes |
| `mvn test` | Compile + run JUnit 5 tests |

## Answers (self-test)

Compare your answers against the theory sections above. Re-read any section you could not explain out loud in 60 seconds.
