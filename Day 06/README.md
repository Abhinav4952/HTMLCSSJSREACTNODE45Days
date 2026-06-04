# Day 06 — Shadows & CSS Units

## Learning objectives

- Compose **layered `box-shadow`** values for elevation, inset panels, and focus rings without relying on heavy image assets.
- Use **`text-shadow`** for legibility effects (soft glow, “letterpress” depth) while avoiding unreadable blur stacks.
- Choose among **`px`**, **`rem`**, **`em`**, **`vw`**, and **`vh`** deliberately: know what each anchors to, when compounding happens, and when viewport units create accessibility hazards.
- Combine **fluid typography** (`clamp()`, `vw`) with sensible min/max bounds and user font-size preferences (`rem` roots).
- Complete one **JavaScript** lab with **Vitest** that encodes numeric rules for converting CSS lengths at the **authoring** level (not full CSS parser scope).

## Prerequisites

- Days **01–05** (document structure, typography basics, selectors, decoration).

## How to use this folder

1. Read `DAY-06-THEORY-AND-REFERENCE.md` end-to-end once, then revisit sections while doing tasks.
2. Work tasks **in order** unless your instructor permits otherwise—difficulty ramps, and Task 04 depends on mental models from Tasks 01–03.
3. For Task 04: run `npm install` then `npm test` from that task folder; tests should fail until your `TODO`s are implemented.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-shadow-studio-cards` | HTML/CSS | Browser + rubric |
| 2 | `task-02-fluid-type-clamp-and-viewport` | HTML/CSS | Browser + rubric |
| 3 | `task-03-em-rem-compounding-trap` | HTML/CSS (challenge) | Browser + rubric |
| 4 | `task-04-css-length-math-lab` | JavaScript | `npm install` → `npm test` |
