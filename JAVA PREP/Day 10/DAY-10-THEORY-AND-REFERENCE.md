# Day 10 — Abstract Classes, Interfaces, Polymorphism, Sealed Types, SOLID (Light)

**Phase:** Core Java  
**Day:** 10  
**Verify tasks with:** `mvn test`

## Overview

This day focuses on **Abstract Classes, Interfaces, Polymorphism, Sealed Types, SOLID (Light)**. Read each section, try the self-test questions, then complete the practical tasks in order.

## Day roadmap

1. Abstract classes
2. Interfaces
3. Polymorphism and casting
4. Sealed classes and SOLID (light)

## Abstract classes

Cannot instantiate. May have state and constructors. Subclasses must implement abstract methods unless abstract.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Abstract classes**?
2. What bug appears if you misuse this concept?

## Interfaces

Contracts. Default methods enable evolution. Multiple interfaces OK. Conflict resolution rules.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Interfaces**?
2. What bug appears if you misuse this concept?

## Polymorphism and casting

Reference type vs runtime type. `instanceof` pattern matching (Java 16+). ClassCastException risk.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Polymorphism and casting**?
2. What bug appears if you misuse this concept?

## Sealed classes and SOLID (light)

`sealed`/`permits` for closed hierarchies. SOLID: SRP, OCP, LSP, ISP, DIP — map to DI in Spring later.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Sealed classes and SOLID (light)**?
2. What bug appears if you misuse this concept?

## Common mistakes & debugging

- Reading theory without running `mvn test` on the warm-up task first.
- Mixing up compile-time types with runtime behavior.
- Ignoring exception messages from failing tests.

## Interview angles

- Explain the key idea behind Abstract Classes, Interfaces, Polymorphism, Sealed Types, SOLID (Light).
- What production bug have you seen (or can imagine) related to today's topic?

## Further reading

- Oracle Java Tutorials (matching topic)
- Java Language Specification sections referenced in interviews
- OCA Java SE 8 Programmer I Study Guide — overlapping chapters (update mentally to Java 21 where APIs differ)

## Glossary

| Term | Meaning |
|------|---------|
| Day 10 focus | Abstract Classes, Interfaces, Polymorphism, Sealed Types, SOLID (Light) |
| `mvn test` | Compile + run JUnit 5 tests |

## Answers (self-test)

Compare your answers against the theory sections above. Re-read any section you could not explain out loud in 60 seconds.
