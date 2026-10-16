# Day 09 — Inheritance, Overriding, super, and Object Methods

**Phase:** Core Java  
**Day:** 09  
**Verify tasks with:** `mvn test`

## Overview

This day focuses on **Inheritance, Overriding, super, and Object Methods**. Read each section, try the self-test questions, then complete the practical tasks in order.

## Day roadmap

1. Inheritance basics
2. Overriding
3. Object methods

## Inheritance basics

`extends` one class. Constructors chain to `super(...)`. Protected members visible to subclasses.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Inheritance basics**?
2. What bug appears if you misuse this concept?

## Overriding

Same signature, compatible return, non-weaker access. `@Override` catches typos. `final` methods cannot be overridden.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Overriding**?
2. What bug appears if you misuse this concept?

## Object methods

`equals`/`hashCode` contract. Prefer Objects.equals/hash. `toString` for debugging.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Object methods**?
2. What bug appears if you misuse this concept?

## Common mistakes & debugging

- Reading theory without running `mvn test` on the warm-up task first.
- Mixing up compile-time types with runtime behavior.
- Ignoring exception messages from failing tests.

## Interview angles

- Explain the key idea behind Inheritance, Overriding, super, and Object Methods.
- What production bug have you seen (or can imagine) related to today's topic?

## Further reading

- Oracle Java Tutorials (matching topic)
- Java Language Specification sections referenced in interviews
- OCA Java SE 8 Programmer I Study Guide — overlapping chapters (update mentally to Java 21 where APIs differ)

## Glossary

| Term | Meaning |
|------|---------|
| Day 09 focus | Inheritance, Overriding, super, and Object Methods |
| `mvn test` | Compile + run JUnit 5 tests |

## Answers (self-test)

Compare your answers against the theory sections above. Re-read any section you could not explain out loud in 60 seconds.
