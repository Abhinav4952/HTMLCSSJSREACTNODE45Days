# Day 26 — Closures: Lexical Scope, Loops, and the Module Pattern

## Learning objectives

- Explain **lexical scoping**: inner functions “see” outer variables by source structure, not call stack.
- Predict and fix the **loop + `var` closure** pitfall using `let` or IIFE binding.
- Use **closures** to hide mutable state while exposing a small public API (module pattern intro).
- Recognize when closures **retain references** (memory / stale state tradeoffs).

## Prerequisites

- **Days 21–25** (functions, `this`, functional patterns).

## How to use this folder

1. Read `DAY-26-THEORY-AND-REFERENCE.md`.
2. Each task is **JavaScript + Vitest**: from the task folder run `npm install` then `npm test`.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-counter-factory` | JavaScript | `npm install` → `npm test` |
| 2 | `task-02-lexical-multiplier` | JavaScript | `npm install` → `npm test` |
| 3 | `task-03-loop-closure-handlers` | JavaScript | `npm install` → `npm test` |
| 4 | `task-04-module-pattern-budget-challenge` | JavaScript | `npm install` → `npm test` |
