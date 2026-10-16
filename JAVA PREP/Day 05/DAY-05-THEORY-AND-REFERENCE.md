# Day 05 — Strings, String Pool, StringBuilder, Equality, and Text Blocks

**Phase:** Core Java  
**Day:** 05  
**Verify tasks with:** `mvn test`

## Overview

This day focuses on **Strings, String Pool, StringBuilder, Equality, and Text Blocks**. Read each section, try the self-test questions, then complete the practical tasks in order.

## Day roadmap

1. Immutability and the pool
2. Important String methods
3. StringBuilder
4. Text blocks

## Immutability and the pool

String objects are immutable. Literals may be interned in the pool. `new String("x")` is a different object. `==` is identity; `equals` is content.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Immutability and the pool**?
2. What bug appears if you misuse this concept?

## Important String methods

`length`, `charAt`, `substring`, `indexOf`, `contains`, `startsWith`, `strip`, `isBlank`, `split`, `formatted` / `String.format`.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Important String methods**?
2. What bug appears if you misuse this concept?

## StringBuilder

Mutable buffer for loops of concatenation. Prefer over `+=` in hot loops. Not thread-safe (use StringBuffer rarely).

### Quick checks (self-test)

1. In your own words, what is the main idea of **StringBuilder**?
2. What bug appears if you misuse this concept?

## Text blocks

`"""..."""` for multi-line literals; useful for SQL/JSON samples in tests and docs.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Text blocks**?
2. What bug appears if you misuse this concept?

## Common mistakes & debugging

- Reading theory without running `mvn test` on the warm-up task first.
- Mixing up compile-time types with runtime behavior.
- Ignoring exception messages from failing tests.

## Interview angles

- Explain the key idea behind Strings, String Pool, StringBuilder, Equality, and Text Blocks.
- What production bug have you seen (or can imagine) related to today's topic?

## Further reading

- Oracle Java Tutorials (matching topic)
- Java Language Specification sections referenced in interviews
- OCA Java SE 8 Programmer I Study Guide — overlapping chapters (update mentally to Java 21 where APIs differ)

## Glossary

| Term | Meaning |
|------|---------|
| Day 05 focus | Strings, String Pool, StringBuilder, Equality, and Text Blocks |
| `mvn test` | Compile + run JUnit 5 tests |

## Answers (self-test)

Compare your answers against the theory sections above. Re-read any section you could not explain out loud in 60 seconds.
