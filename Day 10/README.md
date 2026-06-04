# Day 10 — Pseudo-classes & Pseudo-elements

## Learning objectives

- Use **structural pseudo-classes** like `:first-child`, `:last-child`, `:nth-child()`, `:nth-of-type()`, and `:focus-visible` with predictable outcomes.
- Apply `::before` and `::after` for decoration and lightweight UI affordances while respecting **accessibility** (decorations must not replace essential content).
- Implement a small **CSS counters** outline for numbered headings or nav items (lightweight, no JS).

## Prerequisites

- Days **05–09** (selectors, layout, positioning).

## How to use this folder

1. Read `DAY-10-THEORY-AND-REFERENCE.md` carefully—pseudo selectors are “brittle” when DOM structure changes.
2. Treat Task 01 as a **trap training** exercise: `:nth-child` vs `:nth-of-type` is a classic interview failure mode.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-nth-child-vs-nth-of-type-trap` | HTML/CSS (challenge) | Browser + rubric |
| 2 | `task-02-pseudo-element-icons-and-a11y` | HTML/CSS | Browser + rubric |
| 3 | `task-03-focus-visible-ring-customization` | HTML/CSS (challenge) | Browser + rubric |
| 4 | `task-04-css-counters-outline-nav` | HTML/CSS (challenge) | Browser + rubric |
