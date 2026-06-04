# Day 11 — Cascade, Inheritance, Specificity, and Opacity

## Learning objectives

- Explain the **CSS cascade** in terms of origin, importance, specificity, and source order—and predict which declaration wins for a given element.
- Distinguish **inherited** properties (e.g. `color`) from **non-inherited** defaults (e.g. `border`) and use **custom properties** as an inheritance-aware bridge.
- Compute and compare **specificity** for realistic compound selectors, and articulate why `!important` is a maintenance hazard.
- Choose between **`opacity`** and **`rgba()`/`hsla()`** alpha when stacking colors or building overlays, including child-element compositing effects.

## Prerequisites

- Days **05–10** (selectors, pseudo-classes/elements, box model context). Review **Day 05** selectors and **Day 10** pseudo selectors if specificity feels unfamiliar.

## How to use this folder

1. Read `DAY-11-THEORY-AND-REFERENCE.md` first—work the quick checks before peeking at answers.
2. Complete `practical-tasks/` in order unless your instructor assigns otherwise. Task 02 is a **specificity challenge**; Task 04 uses **Vitest** (`npm install` → `npm test`).

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-inheritance-and-custom-properties-playground` | HTML/CSS | Browser + rubric |
| 2 | `task-02-specificity-duel-scoreboard` | HTML/CSS (challenge) | Browser + rubric |
| 3 | `task-03-opacity-stacking-clinic` | HTML/CSS | Browser + rubric |
| 4 | `task-04-cascade-specificity-lab` | JavaScript (Vitest) | `npm install` → `npm test` |
