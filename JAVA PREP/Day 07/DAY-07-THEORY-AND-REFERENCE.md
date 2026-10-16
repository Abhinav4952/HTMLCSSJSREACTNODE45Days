# Day 07 — Methods, Access Modifiers, Static Members, Pass-by-Value, Overloading

**Phase:** Core Java  
**Day:** 07  
**Verify tasks with:** `mvn test`

## Overview

This day focuses on **Methods, Access Modifiers, Static Members, Pass-by-Value, Overloading**. Read each section, try the self-test questions, then complete the practical tasks in order.

## Day roadmap

1. Method anatomy
2. Access modifiers
3. Static members
4. Pass-by-value
5. Overloading

## Method anatomy

Modifiers, return type, name, parameters, throws clause, body. Varargs last.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Method anatomy**?
2. What bug appears if you misuse this concept?

## Access modifiers

`private`, package-private (default), `protected`, `public` — know who can call what across packages.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Access modifiers**?
2. What bug appears if you misuse this concept?

## Static members

Belong to the class. No `this`. Static init blocks run once. Static imports for constants cautiously.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Static members**?
2. What bug appears if you misuse this concept?

## Pass-by-value

Reassigning a parameter does not affect the caller; mutating a referenced object does.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Pass-by-value**?
2. What bug appears if you misuse this concept?

## Overloading

Same name, different parameter lists. Return type alone is not enough. Watch autoboxing ambiguities.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Overloading**?
2. What bug appears if you misuse this concept?

## Common mistakes & debugging

- Reading theory without running `mvn test` on the warm-up task first.
- Mixing up compile-time types with runtime behavior.
- Ignoring exception messages from failing tests.

## Interview angles

- Explain the key idea behind Methods, Access Modifiers, Static Members, Pass-by-Value, Overloading.
- What production bug have you seen (or can imagine) related to today's topic?

## Further reading

- Oracle Java Tutorials (matching topic)
- Java Language Specification sections referenced in interviews
- OCA Java SE 8 Programmer I Study Guide — overlapping chapters (update mentally to Java 21 where APIs differ)

## Glossary

| Term | Meaning |
|------|---------|
| Day 07 focus | Methods, Access Modifiers, Static Members, Pass-by-Value, Overloading |
| `mvn test` | Compile + run JUnit 5 tests |

## Answers (self-test)

Compare your answers against the theory sections above. Re-read any section you could not explain out loud in 60 seconds.
