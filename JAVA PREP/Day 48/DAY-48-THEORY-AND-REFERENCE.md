# Day 48 — Capstone API Slice II: Ownership, Pagination, Errors, and Tests

**Phase:** Capstone  
**Primary theme:** Object-level authorization, safe list endpoints, a consistent error contract, and hardening against bad input  
**Estimated study time:** 2-3 h theory + 5-7 h tasks  
**Related tasks:** `task-01-ownership-guard`, `task-02-paged-note-search`, `task-03-error-contract`, `task-04-note-service-ownership-challenge`  
**Instruction alignment:** Maps to Day 48 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Object-level authorization, safe list endpoints, a consistent error contract, and hardening against bad input. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. Object-level authorization and the ownership model
2. Pagination, sorting, and filtering
3. Consistent error contract and the test pyramid
4. Interview corner, common mistakes, glossary

## Subtopics

### Object-level authorization and the ownership model

#### What it is

Authentication and role checks are not enough: a logged-in USER must only touch **their own** records (OWASP API1: Broken Object Level Authorization). Every query/command that loads a resource by id must verify ownership (or admin) in the service layer.

#### Why it exists / why it matters

The most common API breach is changing an id in the URL and reading someone else's data. Role rules (`hasRole`) cannot express 'this note belongs to caller'.

#### Pros and cons

**Pros**

- Closes IDOR/BOLA vulnerabilities
- Policy is explicit and testable
- Centralizable in one guard/service helper

**Cons / trade-offs**

- Must be applied on every access path (including bulk and search)
- Tempting to forget in new endpoints

#### What happens without it / when misused

Without ownership checks, `GET /notes/123` returns any user's note; scoping only list endpoints but not detail endpoints is a classic gap.

#### Syntax and rules

Pattern: `repo.findById(id).filter(n -> admin || n.ownerId == caller).orElseThrow(NotFound)`. Or scope queries: `findByIdAndOwnerId`.
**403 vs 404 policy:** 404 hides that the resource exists (preferred for private data); 403 is more honest and easier to debug. Pick one policy per API and document it.

#### Examples

**Example 1 — Scoped query**

```java
Optional<Note> n = repo.findByIdAndOwnerId(id, callerId);
```

**Example 2 — Guard**

```java
if (!admin && note.getOwnerId() != caller) throw new NotFoundException("note not found");
```

#### Quick checks

1. What is BOLA/IDOR?
2. Why can 403 leak information?

### Pagination, sorting, and filtering

#### What it is

List endpoints must never return unbounded data. Spring Data's `Pageable`/`Page<T>` provide page index, size, sort and totals. Expose a stable envelope (`content`, `page`, `size`, `totalElements`, `totalPages`) rather than the raw `Page` type.

#### Why it exists / why it matters

Unbounded lists exhaust memory and DB; arbitrary sort fields leak or break queries.

#### Pros and cons

**Pros**

- Predictable memory/latency
- Standard client contract
- Sort/filter in the database

**Cons / trade-offs**

- Offset pagination gets slow on deep pages (use keyset for huge data)
- Counting total rows costs a query

#### What happens without it / when misused

Accepting `size=1000000` or `sort=passwordHash` from the client is a DoS and a data-exposure bug.

#### Syntax and rules

```java
Pageable p = PageRequest.of(page, Math.min(size, 50), Sort.by(Sort.Direction.DESC, "createdAt"));
Page<Note> result = repo.findByOwnerIdAndTitleContainingIgnoreCase(ownerId, q, p);
```
Whitelist sortable fields; clamp size; escape LIKE wildcards if you build patterns yourself.

#### Examples

**Example 1 — Envelope**

```json
{"content":[...],"page":0,"size":20,"totalElements":57,"totalPages":3}
```

#### Quick checks

1. Why whitelist sort fields?
2. Offset vs keyset pagination?

### Consistent error contract and the test pyramid

#### What it is

Clients need one predictable error shape. Spring 6 supports RFC 9457 `ProblemDetail` (`type`, `title`, `status`, `detail`, `instance` + extensions like `errors`). A `@RestControllerAdvice` maps domain exceptions to statuses and never leaks internals. Tests follow the **pyramid**: many fast unit tests, fewer slice tests (`@WebMvcTest`, `@DataJpaTest`), few full `@SpringBootTest` integration tests.

#### Why it exists / why it matters

A uniform contract simplifies clients; layered tests give fast feedback and precise failures.

#### Pros and cons

**Pros**

- Predictable client handling
- Security: no stack traces/SQL in responses
- Fast test suite

**Cons / trade-offs**

- Central handler must be kept in sync with new exceptions
- Slice tests need careful scoping (imports, mocks)

#### What happens without it / when misused

Default Boot error JSON differs per exception; leaking `exception.getMessage()` for unexpected errors reveals secrets and structure.

#### Syntax and rules

```java
@ExceptionHandler(NotFoundException.class)
ProblemDetail notFound(NotFoundException e) {
  ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
  pd.setTitle("Not Found");
  return pd;
}
```

#### Examples

**Example 1 — Validation errors**

```json
{"status":400,"title":"Bad Request","detail":"Validation failed","errors":{"name":"must not be blank"}}
```

#### Quick checks

1. What belongs in a 500 response?
2. Which test type verifies JSON error shapes?

## Interview corner

**Q1. What is BOLA?**

Broken object-level authorization: missing ownership checks on id-based access.

**Q2. 403 or 404 for someone else's resource?**

404 to hide existence (common for private data), 403 when existence is public; be consistent.

**Q3. How do you prevent huge responses?**

Mandatory pagination with a max size.

**Q4. What is ProblemDetail?**

Standard (RFC 9457) JSON error format supported by Spring 6.

**Q5. What goes in the test pyramid base?**

Fast unit tests of services/guards.

## Common mistakes & debugging

- Scoping list endpoints but not detail endpoints.
- Returning raw exception messages.
- Allowing arbitrary sort fields.
- Validating after the database lookup.
- Using `@SpringBootTest` for everything.

## Further reading

- OWASP API Security Top 10 (API1 BOLA)
- Spring Framework Reference: Error Responses
- Spring Data JPA Reference: Paging and Sorting

## Glossary

| Term | Meaning |
|------|---------|
| BOLA/IDOR | Accessing others' objects via ids |
| ProblemDetail | RFC 9457 error format |
| Keyset pagination | Paging by last-seen key |
| Slice test | Test loading only part of the context |
| Whitelist | Explicit list of allowed values |

## Answers

### Object-level authorization and the ownership model

1. Accessing objects of other users by guessing/changing identifiers.
2. It confirms that the id exists.

### Pagination, sorting, and filtering

1. Sorting by arbitrary properties can expose or break internals.
2. Offset is simple but slow deep in the table; keyset uses the last seen key and scales.

### Consistent error contract and the test pyramid

1. A generic message and a correlation id; details go to logs.
2. `@WebMvcTest` with MockMvc.
