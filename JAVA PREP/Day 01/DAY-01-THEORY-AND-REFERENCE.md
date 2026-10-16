# Day 01 — JDK, JVM, Class Structure, Packages, and First Maven Project

**Phase:** Core Java  
**Day:** 01  
**Verify tasks with:** `mvn test`

## Overview

This day focuses on **JDK, JVM, Class Structure, Packages, and First Maven Project**. Read each section, try the self-test questions, then complete the practical tasks in order.

## Day roadmap

1. JDK, JRE, and JVM
2. Compiling and running (`javac` / `java`)
3. Class structure and `main`
4. Packages and imports
5. Maven project shape

## JDK, JRE, and JVM

The **JVM** executes bytecode. The **JRE** historically bundled the JVM plus libraries to *run* apps. The **JDK** adds compilers (`javac`), tools (`jar`, `jcmd`), and APIs to *build* apps. Modern Temurin distributions ship a full JDK; you develop with the JDK, and production images may slim to a runtime build via `jlink`. **Why it matters:** interviews ask this constantly; wrong answers signal you have never shipped Java. **Without the JDK** you cannot compile. **Without a matching major version** (21 vs 17) you get class-file version errors.

### Quick checks (self-test)

1. In your own words, what is the main idea of **JDK, JRE, and JVM**?
2. What bug appears if you misuse this concept?

## Compiling and running (`javac` / `java`)

Source `.java` → `javac` → `.class` bytecode → `java` launches the JVM and loads the main class. Package folders must match package names. Example: `com.javaprep.Hello` lives at `com/javaprep/Hello.java`. Classpath (`-cp`) lists jars and directories of classes. Maven hides this; you still must understand it.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Compiling and running (`javac` / `java`)**?
2. What bug appears if you misuse this concept?

## Class structure and `main`

A public top-level class name must match its file name. `public static void main(String[] args)` is the entry point. Fields hold state; methods hold behavior. Comments: `//`, `/* */`, and Javadoc `/** */`.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Class structure and `main`**?
2. What bug appears if you misuse this concept?

## Packages and imports

Packages organize namespaces and access control (package-private). `import` brings simple names into scope; `import static` imports static members. Avoid star-imports in course code except for tests if needed.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Packages and imports**?
2. What bug appears if you misuse this concept?

## Maven project shape

`pom.xml` defines coordinates (`groupId`, `artifactId`, `version`), dependencies, and the `maven-compiler-plugin` for Java 21. Standard layout: `src/main/java`, `src/test/java`, `src/main/resources`. `mvn test` compiles and runs JUnit.

### Quick checks (self-test)

1. In your own words, what is the main idea of **Maven project shape**?
2. What bug appears if you misuse this concept?

## Common mistakes & debugging

- Reading theory without running `mvn test` on the warm-up task first.
- Mixing up compile-time types with runtime behavior.
- Ignoring exception messages from failing tests.

## Interview angles

- What is the difference between JDK, JRE, and JVM?
- Why must a public class name match its file name?
- What does `mvn test` do in the Maven lifecycle?

## Further reading

- Oracle Java Tutorials (matching topic)
- Java Language Specification sections referenced in interviews
- OCA Java SE 8 Programmer I Study Guide — overlapping chapters (update mentally to Java 21 where APIs differ)

## Glossary

| Term | Meaning |
|------|---------|
| Day 01 focus | JDK, JVM, Class Structure, Packages, and First Maven Project |
| `mvn test` | Compile + run JUnit 5 tests |

## Answers (self-test)

Compare your answers against the theory sections above. Re-read any section you could not explain out loud in 60 seconds.
