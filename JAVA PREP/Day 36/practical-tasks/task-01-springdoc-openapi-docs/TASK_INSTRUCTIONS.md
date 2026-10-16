# Task 1 — OpenAPI Documentation with springdoc

**Day:** 36 · **Task ID:** Day36-task01 · **Type:** Spring Boot · **Difficulty:** Warm-up

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Generate and enrich an OpenAPI 3 document: Info bean, @Tag, @Operation, @ApiResponse and @Schema.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day36/task01/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day36/task01/Item.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day36/task01/ItemController.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day36/task01/OpenApiConfig.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day36/task01/OpenApiDocsTest.java` | Provided helper or test (do not edit) |

## Prerequisites

- Day 36 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Build the `OpenAPI` bean with title, version and description.
2. Add `@Tag`, `@Operation` and `@ApiResponse` annotations to the controller.
3. Document the `Item` record fields with `@Schema`.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day36-task01)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day36-task01)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 36: complete task-01-springdoc-openapi-docs`.

## How to run and verify

```bash
java -version   # 21.x
mvn -v          # 3.9+
mvn test        # expected RED at the start
mvn -Dtest=<TestClass> test
```

## TODO map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `Item.java` | `Day36-task01` | document this field: @Schema(description = "Display name", example = "Laptop |
| `Item.java` | `Day36-task01` | document this field: @Schema(description = "Price in euro", example = "999.00 |
| `ItemController.java` | `Day36-task01` | group the endpoints: @Tag(name = "Items", description = "Item catalogue |
| `ItemController.java` | `Day36-task01` | @Operation(summary = "List all items |
| `ItemController.java` | `Day36-task01` | @Operation(summary = "Find an item by id") and @ApiResponse(responseCode = "200", description = "Item found") and @ApiResponse(responseCode = "404", description = "Item not found |
| `OpenApiConfig.java` | `Day36-task01` | build an OpenAPI with an Info(title, version, description |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `docsAreServed` |
| 2 | `infoBlock` |
| 3 | `controllerIsGroupedUnderTag` |
| 4 | `operationsHaveSummaries` |
| 5 | `notFoundResponseIsDocumented` |
| 6 | `schemaFieldsAreDocumented` |

## Edge cases to handle

- The 404 response must appear even though the method returns `ResponseEntity<Item>`.
- Docs are generated at runtime from the running mappings.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 36: OpenAPI Documentation with springdoc`

## Hints (optional)

<details><summary>Hint 1</summary>
`@ApiResponse` is repeatable on a method.
</details>

<details><summary>Hint 2</summary>
`OpenAPI` and `Info` live in `io.swagger.v3.oas.models`.
</details>
