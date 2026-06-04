# Day 07 — Box Model, `box-sizing`, and Margin Collapse

## Learning objectives

- Explain the CSS box model in terms of **content, padding, border, margin**, and how `outline`/`box-shadow` differ from border for layout size.
- Use **`box-sizing: border-box`** as a default mental model for component sizing, and know when `content-box` still appears (legacy widgets, some form controls).
- Predict **vertical margin collapsing** between siblings and between parent/child, and apply standard fixes (`padding` on parent, `border`, `display: flow-root`, `overflow` not `visible`, etc.).
- Debug “mystery gaps” using DevTools **Layout** overlays rather than guessing.

## Prerequisites

- Days **01–06** (especially units and shadows; margin collapse interacts with vertical rhythm).

## How to use this folder

1. Read `DAY-07-THEORY-AND-REFERENCE.md` slowly—margin collapse rewards careful reading.
2. Do tasks in order: Task 02 and Task 04 are intentionally “detective” puzzles.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-box-model-measurement-sheet` | HTML/CSS | Browser + DevTools + rubric |
| 2 | `task-02-margin-collapse-detective` | HTML/CSS (challenge) | Browser + rubric |
| 3 | `task-03-border-box-migration-playground` | HTML/CSS | Browser + rubric |
| 4 | `task-04-triple-collapse-clinic` | HTML/CSS (challenge) | Browser + rubric |
