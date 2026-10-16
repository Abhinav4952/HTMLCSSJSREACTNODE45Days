# Day 04 — Control Flow: if, switch, Switch Expressions, Loops, and Labels

**Phase:** Core Java  
**Day:** 04  
**Verify tasks with:** `mvn test`

## Overview

This day focuses on **Control Flow: if, switch, Switch Expressions, Loops, and Labels**. Read each section, try the self-test questions, then complete the practical tasks in order.

## Day roadmap

1. if / else
2. Classic switch and switch expressions
3. Loops
4. Labels, break, continue

## if / else

Conditions must be boolean. Prefer early returns over deep nesting.

### Quick checks (self-test)

1. In your own words, what is the main idea of **if / else**?
2. What bug appears if you misuse this concept?

## Classic switch and switch expressions

Classic switch falls through unless `break`. Switch expressions (Java 14+) are exhaustive for enums and use `->` or `yield`. Prefer expressions for mapping values.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Classic switch and switch expressions**?
2. What bug appears if you misuse this concept?

## Loops

`while`, `do-while`, `for`, enhanced-for. Know when enhanced-for cannot modify the underlying structure safely with iterators.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Loops**?
2. What bug appears if you misuse this concept?

## Labels, break, continue

Labels qualify which loop to break/continue. Overuse harms readability — use for nested-loop escapes.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Labels, break, continue**?
2. What bug appears if you misuse this concept?

## Common mistakes & debugging

- Reading theory without running `mvn test` on the warm-up task first.
- Mixing up compile-time types with runtime behavior.
- Ignoring exception messages from failing tests.

## Interview angles

- Explain the key idea behind Control Flow: if, switch, Switch Expressions, Loops, and Labels.
- What production bug have you seen (or can imagine) related to today's topic?

## Further reading

- Oracle Java Tutorials (matching topic)
- Java Language Specification sections referenced in interviews
- OCA Java SE 8 Programmer I Study Guide — overlapping chapters (update mentally to Java 21 where APIs differ)

## Glossary

| Term | Meaning |
|------|---------|
| Day 04 focus | Control Flow: if, switch, Switch Expressions, Loops, and Labels |
| `mvn test` | Compile + run JUnit 5 tests |

## Answers (self-test)

Compare your answers against the theory sections above. Re-read any section you could not explain out loud in 60 seconds.
