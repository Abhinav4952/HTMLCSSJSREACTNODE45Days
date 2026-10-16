# Day 03 — Operators, Numeric Promotion, Casting, and Overflow

**Phase:** Core Java  
**Day:** 03  
**Verify tasks with:** `mvn test`

## Overview

This day focuses on **Operators, Numeric Promotion, Casting, and Overflow**. Read each section, try the self-test questions, then complete the practical tasks in order.

## Day roadmap

1. Arithmetic and unary operators
2. Numeric promotion
3. Casting and overflow
4. Relational, logical, and compound assignment

## Arithmetic and unary operators

`+ - * / %`, unary `+ -`, `++ --` (pre/post). Integer division truncates toward zero. Division by zero throws `ArithmeticException` for ints; for doubles yields Infinity/NaN.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Arithmetic and unary operators**?
2. What bug appears if you misuse this concept?

## Numeric promotion

Binary numeric promotion lifts smaller types toward `int`/`long`/`float`/`double` per JLS rules. `byte + byte` promotes to `int`.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Numeric promotion**?
2. What bug appears if you misuse this concept?

## Casting and overflow

Narrowing casts truncate. Integer overflow wraps silently (two's complement). Use `Math.addExact` when overflow must be detected.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Casting and overflow**?
2. What bug appears if you misuse this concept?

## Relational, logical, and compound assignment

`==` on primitives compares values; on references compares identity. `&&`/`||` short-circuit; `&`/`|` on booleans do not. Compound `+=` includes a cast.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Relational, logical, and compound assignment**?
2. What bug appears if you misuse this concept?

## Common mistakes & debugging

- Reading theory without running `mvn test` on the warm-up task first.
- Mixing up compile-time types with runtime behavior.
- Ignoring exception messages from failing tests.

## Interview angles

- Explain the key idea behind Operators, Numeric Promotion, Casting, and Overflow.
- What production bug have you seen (or can imagine) related to today's topic?

## Further reading

- Oracle Java Tutorials (matching topic)
- Java Language Specification sections referenced in interviews
- OCA Java SE 8 Programmer I Study Guide — overlapping chapters (update mentally to Java 21 where APIs differ)

## Glossary

| Term | Meaning |
|------|---------|
| Day 03 focus | Operators, Numeric Promotion, Casting, and Overflow |
| `mvn test` | Compile + run JUnit 5 tests |

## Answers (self-test)

Compare your answers against the theory sections above. Re-read any section you could not explain out loud in 60 seconds.
