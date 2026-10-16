# Day 40 — Spring AOP: Aspects, Pointcuts and Advice

**Phase:** Spring Boot  
**Primary theme:** Cross-cutting concerns with proxies: advice types, pointcut expressions, around advice and aspect ordering  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-advice-types-order-service`, `task-02-around-timing-and-args`, `task-03-pointcut-expressions-lab`, `task-04-aspect-ordering-challenge`  
**Instruction alignment:** Maps to Day 40 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Cross-cutting concerns with proxies: advice types, pointcut expressions, around advice and aspect ordering. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. AOP concepts: aspects, join points, pointcuts and advice
2. Pointcut expressions
3. Around advice, ordering and common pitfalls
4. Interview corner, common mistakes, glossary

## Subtopics

### AOP concepts: aspects, join points, pointcuts and advice

#### What it is

**Aspect-oriented programming** modularizes cross-cutting concerns (logging, security checks, transactions, metrics). Vocabulary: **aspect** (the module), **join point** (a point in execution - in Spring AOP always a method execution on a Spring bean), **pointcut** (predicate selecting join points), **advice** (code run at them: `@Before`, `@After`, `@AfterReturning`, `@AfterThrowing`, `@Around`), **weaving** (applying aspects). Spring AOP weaves at runtime by creating **proxies** (JDK dynamic proxies for interfaces, CGLIB subclasses otherwise).

#### Why it exists / why it matters

Without AOP, concerns like transactions or auditing are copy-pasted into every service method, obscuring business logic. `@Transactional`, `@Cacheable`, `@Async` and Spring Security method security are all implemented as AOP advice.

#### Pros and cons

**Pros**

- Removes duplication of cross-cutting code
- Business classes stay focused
- Declarative and centrally changeable
- Foundation of many Spring features

**Cons / trade-offs**

- Proxy-based: self-invocation bypasses advice
- Only public method calls on Spring beans are advised (by default)
- Debugging through proxies is harder
- Hidden behavior can surprise readers

#### What happens without it / when misused

Hand-written try/finally timing code in 50 methods drifts and gets forgotten. Conversely, putting business rules in aspects hides logic where nobody looks. Calling `this.method()` inside a bean skips the proxy, so advice silently does not run.

#### Syntax and rules

```java
@Aspect @Component
class AuditAspect {
  @Pointcut("execution(* com.acme.OrderService.*(..))") void orderOps() {}
  @Before("orderOps()")        void before(JoinPoint jp) {...}
  @AfterReturning(pointcut = "orderOps()", returning = "r") void ok(Object r) {...}
  @AfterThrowing(pointcut = "orderOps()", throwing = "ex")  void failed(Throwable ex) {...}
  @After("orderOps()")         void always() {...}
}
```
Enable with `spring-boot-starter-aop` (auto-configured) or `@EnableAspectJAutoProxy`.

#### Examples

**Example 1 — Proxy check**

```java
AopUtils.isAopProxy(bean); AopUtils.isCglibProxy(bean);
```

**Example 2 — Self-invocation pitfall**

```java
public void a() { this.b(); }   // b()'s advice does NOT run
@Transactional public void b() {...}
```

**Example 3 — Dependency**

```xml
<dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-aop</artifactId></dependency>
```

#### Quick checks

1. What is a join point in Spring AOP?
2. Which advice always runs?
3. Why does self-invocation skip advice?

### Pointcut expressions

#### What it is

AspectJ pointcut designators select join points: `execution(modifiers? ret declaring.name(params) throws?)` (the workhorse), `within(type pattern)`, `this`/`target`, `args`, `@annotation(...)`, `@within(...)`, `bean(name)`. Wildcards: `*` one segment/any single element, `..` any number of packages or parameters. Combine with `&&`, `||`, `!`. Name reusable ones with `@Pointcut`.

#### Why it exists / why it matters

A precise pointcut decides what gets advised: too broad slows the app and surprises; too narrow misses calls.

#### Pros and cons

**Pros**

- Declarative selection by structure or annotation
- Composable and reusable
- Annotation-based pointcuts decouple from package layout

**Cons / trade-offs**

- Strings are not compile-checked (typos match nothing silently)
- Package refactors break `execution` patterns
- Complex expressions are hard to read

#### What happens without it / when misused

A typo in a package name results in an aspect that never fires - and no error. Overly broad `execution(* *(..))` advises framework beans and can break startup.

#### Syntax and rules

```text
execution(* com.acme.service.*.*(..))       all methods of classes directly in service
execution(* com.acme..*Service.*(..))        any *Service in com.acme and sub-packages
execution(* *..*.save(String))               any save(String)
within(com.acme.web..*)                      all types in web package tree
@annotation(com.acme.Audited)                methods annotated with @Audited
execution(* com.acme..*(..)) && !within(com.acme.web..*)
```
Prefer annotation-driven pointcuts for opt-in behavior (`@Timed`).

#### Examples

**Example 1 — Named pointcut**

```java
@Pointcut("within(@org.springframework.stereotype.Service *)")
void services() {}
```

**Example 2 — Binding arguments**

```java
@Before("execution(* *(..)) && args(id,..)")
void log(long id) {...}
```

**Example 3 — Test a pointcut**

```java
AspectJExpressionPointcut pc = new AspectJExpressionPointcut(); pc.setExpression(expr);
boolean m = pc.matches(method, targetClass);
```

#### Quick checks

1. `..` in a package pattern means?
2. execution vs within?
3. How can you unit-test a pointcut?

### Around advice, ordering and common pitfalls

#### What it is

`@Around` wraps the call: you receive a `ProceedingJoinPoint`, decide whether/when to call `proceed()` (optionally with replaced arguments), may transform the result or exception, and can short-circuit (e.g. cache hit). Multiple aspects form an onion; `@Order(n)` (or `Ordered`) sets precedence - the lowest value is the outermost. Within one aspect the order is Around, Before, After, AfterReturning/AfterThrowing on the way in.

#### Why it exists / why it matters

Timing, caching, retry, transaction and security checks need control over the call itself. Ordering decides correctness: authentication must run before the transaction opens, retries outside of transactions.

#### Pros and cons

**Pros**

- Full control over invocation
- Composable via ordering
- Single place for retry/metrics/cache logic

**Cons / trade-offs**

- Forgetting `proceed()` silently skips the target
- Swallowing exceptions hides failures
- Ordering bugs are subtle
- Performance overhead when pointcuts are broad

#### What happens without it / when misused

An around advice that catches `Exception` and returns null converts failures into silent nulls. Two aspects without `@Order` run in unspecified order, so a test passes locally and fails in CI. Private methods, final classes/methods (CGLIB) and `this.` calls are not advised.

#### Syntax and rules

```java
@Around("@annotation(com.acme.Timed)")
Object time(ProceedingJoinPoint pjp) throws Throwable {
  long t0 = System.nanoTime();
  try { return pjp.proceed(); }
  finally { metrics.record(pjp.getSignature().getName(), System.nanoTime() - t0); }
}
@Aspect @Order(1) class SecurityAspect {...}   // outermost
@Aspect @Order(2) class TxAspect {...}
```

#### Examples

**Example 1 — Rewrite arguments**

```java
Object[] args = pjp.getArgs().clone(); args[0] = ((String) args[0]).trim(); return pjp.proceed(args);
```

**Example 2 — Short-circuit (cache)**

```java
Object hit = cache.get(key); if (hit != null) return hit; return cache.put(key, pjp.proceed());
```

**Example 3 — Retry**

```java
for (int i = 0; ; i++) { try { return pjp.proceed(); } catch (TransientException e) { if (i == 2) throw e; } }
```

#### Quick checks

1. What is the outermost aspect with @Order(1) and @Order(2)?
2. Must an around advice call proceed()?
3. Why might advice not run on a bean method?

## Interview corner

**Q1. How does Spring AOP work?**

Runtime proxies (JDK or CGLIB) intercept method calls and run advice.

**Q2. JDK proxy vs CGLIB?**

JDK proxies implement interfaces; CGLIB subclasses the class (Boot defaults to CGLIB).

**Q3. Name AOP-based Spring features.**

@Transactional, @Cacheable, @Async, @PreAuthorize.

**Q4. Spring AOP vs AspectJ?**

Spring AOP is proxy-based and method-only; AspectJ weaves bytecode and supports more join points.

**Q5. How do you order aspects?**

@Order or implementing Ordered; lowest value is outermost.

## Common mistakes & debugging

- Self-invocation.
- Missing `proceed()`.
- Swallowing exceptions.
- Overly broad pointcuts.
- Final classes/methods with CGLIB.

## Further reading

- Spring Framework Reference: Aspect Oriented Programming with Spring
- AspectJ pointcut language cheat sheet

## Glossary

| Term | Meaning |
|------|---------|
| Aspect | Module encapsulating a cross-cutting concern |
| Join point | Point in execution (method call) |
| Pointcut | Selector for join points |
| Advice | Code run at a join point |
| Proxy | Wrapper object that applies advice |

## Answers

### AOP concepts: aspects, join points, pointcuts and advice

1. A method execution on a Spring-managed bean.
2. `@After` (like finally).
3. The call does not go through the proxy.

### Pointcut expressions

1. Any number of sub-packages.
2. execution matches method signatures; within matches the declaring type location.
3. With `AspectJExpressionPointcut#matches`.

### Around advice, ordering and common pitfalls

1. @Order(1).
2. Not always (short-circuit), but normally exactly once.
3. Self-invocation, private/final methods, or the object is not a Spring bean.
