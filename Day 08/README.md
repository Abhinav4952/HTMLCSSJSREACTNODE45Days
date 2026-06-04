# Day 08 — Positioning & Stacking Context (Intro)

## Learning objectives

- Use `position: static | relative | absolute | fixed | sticky` with accurate mental models of **offset properties** (`top/right/bottom/left`).
- Identify the **containing block** for absolutely positioned elements (not always the parent you visually expect).
- Explain **stacking contexts** at a high honest level: what creates them, why `z-index` “doesn’t work” sometimes, and how `isolation` can help.
- Combine `position: sticky` with overflow constraints without surprise clipping (preview of common footgun).

## Prerequisites

- Day **07** (box model + margins) — positioning interacts directly with containing blocks and overflow.

## How to use this folder

1. Read `DAY-08-THEORY-AND-REFERENCE.md` with DevTools open; many claims are easiest to *see* in the inspector.
2. Tasks 02 and 04 are intentionally “mystery” layouts—measure before changing.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
| 1 | `task-01-static-relative-playground` | HTML/CSS | Browser + rubric |
| 2 | `task-02-absolute-containing-block-challenge` | HTML/CSS (challenge) | Browser + rubric |
| 3 | `task-03-fixed-header-sticky-sidebar` | HTML/CSS | Browser + rubric |
| 4 | `task-04-stacking-context-z-index-mystery` | HTML/CSS (challenge) | Browser + rubric |
