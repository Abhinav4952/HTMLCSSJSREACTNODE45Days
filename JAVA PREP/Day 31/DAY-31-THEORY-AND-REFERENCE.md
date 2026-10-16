# Day 31 — REST II: DTOs, Bean Validation, Error Handling and Layered Design

**Phase:** Spring Boot  
**Primary theme:** Production-shaped REST APIs: validated DTOs, uniform error responses and a layered codebase  
**Estimated study time:** 2–3 h theory + 3–5 h tasks  
**Related tasks:** `task-01-create-user-validation`, `task-02-problem-detail-advice`, `task-03-layered-todo-service`, `task-04-custom-constraints`  
**Instruction alignment:** Maps to Day 31 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Production-shaped REST APIs: validated DTOs, uniform error responses and a layered codebase. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. DTOs, Bean Validation and @Valid
2. @RestControllerAdvice, ProblemDetail and error handling
3. Layered architecture: controller, service, repository, mapper
4. Interview corner, common mistakes, glossary

## Subtopics

### DTOs, Bean Validation and @Valid

#### What it is

A **DTO** (data transfer object) is a class/record that defines exactly what crosses the API boundary. **Bean Validation** (Jakarta Validation, implemented by Hibernate Validator) declares rules with annotations (`@NotBlank`, `@Email`, `@Min`, `@Size`, `@Pattern`, `@Positive`...). `@Valid` on a `@RequestBody` argument makes Spring validate it and raise `MethodArgumentNotValidException` (400) on violations; `@Validated` enables validation of `@RequestParam`/`@PathVariable` (yielding `HandlerMethodValidationException` in Spring 6.1+).

#### Why it exists / why it matters

Never trust client input. Declarative rules keep validation next to the data, are reusable and produce uniform errors. Separate DTOs prevent mass-assignment (a client setting `role=ADMIN`) and keep the API stable while entities evolve.

#### Pros and cons

**Pros**

- Rules are visible and declarative
- Same constraints reusable in persistence and UI
- Standard error flow
- DTOs hide internal fields and shape responses

**Cons / trade-offs**

- Mapping boilerplate between DTOs and entities
- Cross-field rules need custom constraints
- Annotation messages need i18n for production

#### What happens without it / when misused

Without validation, nulls and malformed data propagate into services and databases (NPEs, constraint violations at commit). Binding requests straight to entities lets clients overwrite fields such as `id`, `role`, `createdAt`.

#### Syntax and rules

```java
public record CreateUserRequest(@NotBlank String name, @Email String email, @Min(18) int age) {}
@PostMapping ResponseEntity<UserResponse> create(@Valid @RequestBody CreateUserRequest r)
```
Requires `spring-boot-starter-validation`. Groups (`@Validated(OnCreate.class)`) select rule sets. `@NotNull` vs `@NotBlank` vs `@NotEmpty`: null / not blank text / not empty collection or string.

#### Examples

**Example 1 — Constraint set**

```java
record SignUp(@NotBlank @Size(max = 50) String name,
               @NotBlank @Email String email,
               @Pattern(regexp = "^[A-Z]{2}\\d{4}$") String code) {}
```

**Example 2 — Validating a path variable**

```java
@Validated @RestController class C {
  @GetMapping("/{id}") Item get(@PathVariable @Positive long id) {...}
}
```

**Example 3 — Nested validation**

```java
record Order(@NotEmpty List<@Valid Line> lines) {}
record Line(@NotBlank String sku, @Positive int qty) {}
```

#### Quick checks

1. @NotNull vs @NotBlank?
2. What does @Valid trigger?
3. Why use separate request/response DTOs?

### @RestControllerAdvice, ProblemDetail and error handling

#### What it is

`@RestControllerAdvice` is a global `@ControllerAdvice` + `@ResponseBody`: its `@ExceptionHandler` methods translate exceptions from any controller into responses. **ProblemDetail** is Spring 6's model for RFC 9457 (`application/problem+json`) with `type`, `title`, `status`, `detail`, `instance` and custom properties. Enable it for built-in MVC exceptions with `spring.mvc.problemdetails.enabled=true` or by extending `ResponseEntityExceptionHandler`.

#### Why it exists / why it matters

Consistent, machine-readable errors let clients react (show field errors, retry, report) without parsing ad-hoc JSON. Central handling removes try/catch noise from controllers.

#### Pros and cons

**Pros**

- One place for error policy
- Standard format understood by tooling
- Controllers stay focused on the happy path
- Easy to add correlation ids and error codes

**Cons / trade-offs**

- Global handlers can mask exceptions if too broad (`Exception.class`)
- Handler order/specificity matters
- Must avoid leaking stack traces or internals

#### What happens without it / when misused

Without central handling, unhandled exceptions become 500 with Boot's default error JSON (possibly with message/trace depending on config). Each controller reinvents try/catch and formats differ.

#### Syntax and rules

```java
@RestControllerAdvice
class ApiErrors {
  @ExceptionHandler(NotFound.class)
  ProblemDetail notFound(NotFound e) {
    ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
    pd.setTitle("Not Found");
    return pd;
  }
}
```
Most specific exception type wins. Use `@ResponseStatus` on an exception class for the simple cases.

#### Examples

**Example 1 — Custom property**

```java
pd.setProperty("errors", Map.of("email", "must be a well-formed email address"));
```

**Example 2 — Extend base handler**

```java
@RestControllerAdvice
class Handler extends ResponseEntityExceptionHandler {}
// + spring.mvc.problemdetails.enabled=true
```

**Example 3 — Exception with status**

```java
@ResponseStatus(HttpStatus.NOT_FOUND)
class NotFound extends RuntimeException {}
```

#### Quick checks

1. What media type does ProblemDetail use?
2. Which exception signals a failed @Valid body?
3. Why not catch `Exception` globally and return 500 details?

### Layered architecture: controller, service, repository, mapper

#### What it is

Typical Spring layering: **controller** (HTTP: binding, status codes), **service** (business rules and transactions), **repository** (persistence), plus **mappers** that convert between entities/domain objects and DTOs. Dependencies point inward: controller -> service -> repository; lower layers never depend on HTTP types.

#### Why it exists / why it matters

Separation lets you test rules without a web server, swap storage, and keep controllers thin. Transaction boundaries and security rules live naturally in the service layer.

#### Pros and cons

**Pros**

- Testability (unit test services with fakes)
- Clear ownership of responsibilities
- Reuse of services across controllers, jobs and messaging
- Easier refactoring

**Cons / trade-offs**

- More classes for small apps
- Pass-through services add noise
- Mappers need maintenance (or a library such as MapStruct)

#### What happens without it / when misused

Fat controllers mix parsing, rules and SQL, so logic cannot be reused or tested without HTTP. Letting controllers call repositories skips transactions and business checks.

#### Syntax and rules

```text
controller  -> service -> repository -> database
   |          |
  DTO       domain/entity
```
Constructor injection everywhere; one public method per use case; throw domain exceptions (`TodoNotFoundException`) and translate them in the advice.

#### Examples

**Example 1 — Thin controller**

```java
@PostMapping TodoDto create(@Valid @RequestBody CreateTodo r) { return service.create(r.title()); }
```

**Example 2 — Service rule**

```java
if (repo.existsByTitleIgnoreCase(title)) throw new DuplicateTodoException(title);
```

**Example 3 — Mapper**

```java
static TodoDto toDto(Todo t) { return new TodoDto(t.id(), t.title(), t.done() ? "DONE" : "OPEN"); }
```

#### Quick checks

1. Where do business rules belong?
2. Why should controllers not use repositories directly?
3. What does a mapper protect against?

## Interview corner

**Q1. Why DTOs instead of entities in the API?**

Stability, security (mass assignment) and avoiding lazy-loading/serialization problems.

**Q2. How does Spring turn validation errors into 400?**

Argument resolution raises MethodArgumentNotValidException which the default or custom handler maps to 400.

**Q3. What is ProblemDetail?**

Spring's RFC 9457 error representation.

**Q4. Controller vs service responsibility?**

Controller adapts HTTP; service owns rules and transactions.

**Q5. How do you validate a path variable?**

`@Validated` on the controller plus constraints on the parameter.

## Common mistakes & debugging

- Forgetting `spring-boot-starter-validation`.
- Putting `@Valid` on the wrong parameter or omitting it.
- Catching `Exception` in the advice.
- Returning entities from controllers.

## Further reading

- Spring Framework Reference: Error Responses
- Jakarta Bean Validation specification
- RFC 9457 Problem Details

## Glossary

| Term | Meaning |
|------|---------|
| DTO | Object defining an API payload |
| ProblemDetail | RFC 9457 error model |
| ConstraintValidator | Custom validation logic |
| Controller advice | Global exception/model handling |
| Mass assignment | Client setting fields it should not |

## Answers

### DTOs, Bean Validation and @Valid

1. `@NotNull` rejects only null; `@NotBlank` also rejects empty/whitespace strings.
2. Validation of the annotated argument; failures raise `MethodArgumentNotValidException`.
3. To control exposed fields, avoid mass assignment and decouple the API from the persistence model.

### @RestControllerAdvice, ProblemDetail and error handling

1. `application/problem+json`.
2. `MethodArgumentNotValidException`.
3. It hides root causes and may leak internals; handle known types and let the rest log and return a generic 500.

### Layered architecture: controller, service, repository, mapper

1. In the service layer.
2. It bypasses business rules/transactions and couples HTTP to persistence.
3. Leaking entity internals and mass assignment.
