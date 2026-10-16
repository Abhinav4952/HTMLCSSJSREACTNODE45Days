# Day 11 — Exceptions: Checked vs Unchecked, try-with-resources, Custom Exceptions

**Phase:** Core Java  
**Day:** 11  
**Verify tasks with:** `mvn test`

## Overview

This day focuses on **Exceptions: Checked vs Unchecked, try-with-resources, Custom Exceptions**. Read each section, try the self-test questions, then complete the practical tasks in order.

## Day roadmap

1. Exception hierarchy
2. try / catch / finally / multi-catch
3. try-with-resources
4. Custom exceptions

## Exception hierarchy

Throwable → Error / Exception. RuntimeException unchecked. Checked must declare or handle.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Exception hierarchy**?
2. What bug appears if you misuse this concept?

## try / catch / finally / multi-catch

Finally always runs (except JVM kill). Multi-catch with `|`. Prefer precise catches.

### Quick checks (self-test)

1. In your own words, what is the main idea of **try / catch / finally / multi-catch**?
2. What bug appears if you misuse this concept?

## try-with-resources

AutoCloseable resources closed automatically. Suppressed exceptions attached to primary.

### Quick checks (self-test)

1. In your own words, what is the main idea of **try-with-resources**?
2. What bug appears if you misuse this concept?

## Custom exceptions

Extend Exception or RuntimeException. Include message and cause. Domain exceptions improve APIs.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Custom exceptions**?
2. What bug appears if you misuse this concept?

## Common mistakes & debugging

- Reading theory without running `mvn test` on the warm-up task first.
- Mixing up compile-time types with runtime behavior.
- Ignoring exception messages from failing tests.

## Interview angles

- Explain the key idea behind Exceptions: Checked vs Unchecked, try-with-resources, Custom Exceptions.
- What production bug have you seen (or can imagine) related to today's topic?

## Further reading

- Oracle Java Tutorials (matching topic)
- Java Language Specification sections referenced in interviews
- OCA Java SE 8 Programmer I Study Guide — overlapping chapters (update mentally to Java 21 where APIs differ)

## Glossary

| Term | Meaning |
|------|---------|
| Day 11 focus | Exceptions: Checked vs Unchecked, try-with-resources, Custom Exceptions |
| `mvn test` | Compile + run JUnit 5 tests |

## Answers (self-test)

Compare your answers against the theory sections above. Re-read any section you could not explain out loud in 60 seconds.
