# Task 01 — Function Declarations vs Expressions

## Summary

Implement **`square`** as a **function declaration** and **`cube`** as a **`const`-bound function expression**, both with the same numeric validation rules.

## Learning goals

- Practice the two most common function “shapes” at module scope.
- Reinforce **finite number** validation before doing math.

## Provided files

- `package.json`, `.npmrc`
- `src/functionFormsLab.js` — your edits only
- `tests/functionFormsLab.test.js` — read-only

## Prerequisites

- Day 21 theory sections on declarations vs expressions.

## What you will implement

1. `square(n)` using a **top-level function declaration** named `square`.
2. `cube(n)` using **`export const cube = function (n) { ... }`** (a function expression, not an arrow).
3. For both: if `n` is not a number or is not finite, return `NaN`.

## Constraints

- Do not edit tests or the Markdown spec files.
- Keep `square` as a declaration (do not rewrite it as `const square = ...`).

## Step-by-step guidance

1. Read the JSDoc in `src/functionFormsLab.js`.
2. Implement `typeof n === "number" && Number.isFinite(n)` guards.
3. Run `npm test` until green.

## How to run and verify

### Install dependencies

```bash
cd "Day 21/practical-tasks/task-01-function-declarations-and-expressions"
npm install
```

### Run tests (JavaScript / Node logic tasks)

```bash
npm test
```

Expect **red** until both functions are implemented.

### Manual checks (all tasks)

- [ ] `square` remains a `function` declaration in source (human review).
- [ ] `cube` uses a non-arrow function expression assigned to `const`.

## `TODO` map

| Location | Done means |
|----------|------------|
| `// TODO(Day21-task01):` in `square` | Correct math + validation |
| `// TODO(Day21-task01):` in `cube` | Correct math + validation |

## Submission checklist (Git)

- [ ] Only intentional files changed
- [ ] `npm test` passes
- [ ] No secrets committed

## Hints (optional)

<details><summary>Spoiler: validation one-liner</summary>

```js
if (typeof n !== "number" || !Number.isFinite(n)) return Number.NaN;
```

</details>
