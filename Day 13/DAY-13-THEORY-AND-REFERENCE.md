# Day 13 — Responsive Design (First Pass)

**Primary theme:** Fluid typography/layout, min/max constraints, and media queries without losing the box model mental model  
**Estimated study time:** 2–3 hours theory + 4–7 hours tasks  
**Related tasks:** `task-01-fluid-max-width-reading-column`, `task-02-breakpoint-padding-footgun-clinic`, `task-03-responsive-image-card-grid`, `task-04-mobile-first-two-column-split`  
**Instruction alignment:** Maps to *Responsive design (first pass)*, *Media queries*, and reinforces *CSS units* (Day 06) + *box model* (Day 07).

---

## Overview

Responsive design is not “write three totally different websites.” It is **one system** that stretches and reflows as the viewport changes. The first-pass toolkit is small but powerful:

- constrain readable measure with **`max-width` + `ch`/`rem`**
- allow flexible widths with **`min()` / `max()` / `clamp()`** (light preview; deeper typography on Day 16)
- choose breakpoints based on **content tearing**, not device brands
- use **`max-width: 100%`** on images inside fluid containers

This day intentionally introduces **footguns**: padding that appears only at large breakpoints can change the effective content width and make “pixel perfect” breakpoints lie. You will learn to sanity-check in DevTools rather than trusting magic numbers.

---

## Day roadmap

1. [Fluid widths vs fixed widths](#fluid-widths-vs-fixed-widths)
2. [`min-width`, `max-width`, and readable line length](#min-width-max-width-and-readable-line-length)
3. [Media queries: mobile-first vs desktop-first](#media-queries-mobile-first-vs-desktop-first)
4. [Breakpoint footguns (padding, nested wrappers, scrollbar width)](#breakpoint-footguns-padding-nested-wrappers-scrollbar-width)
5. [Responsive images and intrinsic sizing](#responsive-images-and-intrinsic-sizing)
6. [Common mistakes & debugging](#common-mistakes--debugging)
7. [Further reading](#further-reading)
8. [Glossary](#glossary)
9. [Answers (self-test)](#answers-self-test)

---

## Fluid widths vs fixed widths

### What it is

A **fluid** layout uses percentages, `fr`, flex growth, or `auto` flows so tracks expand/shrink. A **fixed** layout pins sizes in `px` regardless of viewport (still useful for max constraints).

#### Why it exists / why it matters

Users do not share one viewport. Fluid systems degrade more gracefully across phones, tablets, ultra-wide monitors, and zoomed pages.

#### Pros and cons

- **Pros:** fewer hard breakpoints; better zoom behavior when paired with relative units.
- **Cons:** unconstrained fluid text can become too wide to read comfortably.

#### What happens without it / when misused

- `width: 1200px` on a container causes horizontal scrolling on phones.

#### Syntax and rules

```css
.page {
  width: min(1100px, 100% - 2rem);
  margin-inline: auto;
}
```

#### Examples

**Tiny — clamp line length**

```css
.article {
  max-width: 65ch;
}
```

**Tiny — min width safety**

```css
.card {
  min-width: 0; /* preview: flex/grid children often need this (Day 14) */
}
```

**Medium — responsive gutter**

```css
:root {
  --gutter: clamp(0.75rem, 2vw, 1.5rem);
}
```

#### Quick checks

1. What does `width: 100%` mean if the parent has padding?
2. Why is readable line length usually discussed in `ch`, not `px`?
3. When is a fixed `px` max still a good idea?

---

## `min-width`, `max-width`, and readable line length

### What it is

`max-width` caps growth; `min-width` prevents shrinking below a threshold (often used to keep touch targets or navigation rows usable).

#### Why it exists / why it matters

Typography becomes hard to scan when lines exceed ~70–90 characters (rule of thumb, depends on font).

#### Pros and cons

- **Pros:** simple, robust readability control.
- **Cons:** `min-width` on flex items can cause overflow if you forget `min-width: 0` in flex contexts (Day 14).

#### What happens without it / when misused

- Ultra-wide monitors render paragraphs the full width of the screen.

#### Syntax and rules

```css
.prose {
  max-width: 68ch;
}
```

#### Quick checks

1. Does `max-width` alone center a block?
2. What is one symptom of “too-wide measure”?

---

## Media queries: mobile-first vs desktop-first

### What it is

A **media query** applies CSS when a media condition matches, commonly `(min-width: …)` or `(max-width: …)`.

- **Mobile-first:** base styles target small screens; `min-width` queries add complexity as viewport grows.
- **Desktop-first:** base styles target large screens; `max-width` queries simplify for smaller screens.

#### Why it exists / why it matters

Different teams prefer different defaults; what matters is **consistency** within a project.

#### Pros and cons

- **Pros:** targeted overrides; can combine conditions (`(min-width: 700px) and (orientation: landscape)`).
- **Cons:** too many breakpoints create maintenance drag.

#### What happens without it / when misused

- “Random” widths (812px) with no design rationale.

#### Syntax and rules

```css
.nav__list {
  display: grid;
  gap: 0.5rem;
}

@media (min-width: 900px) {
  .nav__list {
    grid-auto-flow: column;
    justify-content: end;
  }
}
```

#### Quick checks

1. In mobile-first CSS, do you usually start with `min-width` or `max-width` queries?
2. What is one non-width media feature you might query?

---

## Breakpoint footguns (padding, nested wrappers, scrollbar width)

### What it is

Common responsive bugs come from **padding/border changing the available width** at specific breakpoints, nested `calc()` mistakes, and **`100vw`** including scrollbar width (causing subtle horizontal scroll).

#### Why it exists / why it matters

A layout can “snap” at a breakpoint because padding was added only at `min-width: 1024px`, shrinking the content box unexpectedly.

#### Pros and cons

- **Pros:** padding at large sizes improves whitespace.
- **Cons:** if you also set rigid widths, you can create overflow or misaligned grids.

#### What happens without it / when misused

- A page gains a horizontal scrollbar only on certain widths.

#### Syntax and rules

Prefer:

```css
.wrapper {
  padding-inline: var(--gutter);
}
```

over adding new padding only inside a `min-width` rule without recomputing widths.

#### Examples

**Tiny — avoid `100vw` for full bleed inner widths**

```css
.hero {
  width: 100%;
}
```

#### Quick checks

1. Why can `width: 100vw` cause horizontal scroll?
2. Name one fix when a new padding rule breaks a grid track sum.

---

## Responsive images and intrinsic sizing

### What it is

Images have intrinsic dimensions. In fluid layouts, `max-width: 100%` and `height: auto` preserve aspect ratio while fitting the container.

#### Why it exists / why it matters

Unconstrained images overflow small screens and wreck Cumulative Layout Shift if heights jump.

#### Pros and cons

- **Pros:** simple, widely supported baseline.
- **Cons:** large raster images still download bytes—use appropriate sources for production (`srcset` later).

#### What happens without it / when misused

- A 2400px screenshot overflows a phone viewport.

#### Syntax and rules

```css
img {
  max-width: 100%;
  height: auto;
}
```

#### Quick checks

1. What does `height: auto` do when `width` is constrained?
2. Why is `max-width: 100%` safer than `width: 100%` for unknown aspect ratios?

---

## Common mistakes & debugging

- Horizontal scroll appears “from nowhere” → search for `100vw`, negative margins, `position: fixed` widths.
- Breakpoint changes layout but not typography → consider fluid type (Day 16 preview).
- Forgetting **`box-sizing: border-box`** while mixing `%` widths and padding.

---

## Further reading

- MDN: [Responsive design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- MDN: [Using media queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries)
- MDN: [clamp()](https://developer.mozilla.org/en-US/docs/Web/CSS/clamp)

---

## Glossary

| Term | Meaning |
|------|---------|
| Breakpoint | Width/condition where layout rules change |
| Mobile-first | Start small screens, add complexity with `min-width` |
| Measure | Line length / readable width |
| Intrinsic size | Element’s natural size from content/replaced elements |

---

## Answers (self-test)

### Fluid widths

1. `100%` includes content box relative to parent; parent padding reduces available space for children depending on `box-sizing`—usually use border-box globally.
2. `ch` approximates character width for the current font—good proxy for readability.
3. Fixed `px` max is good for preventing ultra-wide line length and for art-directed containers.

### `min/max`

1. No—needs `margin-inline: auto` typically for centering block boxes.
2. Long lines, hard to track to next line, slower reading.

### Media queries

1. Mobile-first commonly uses **`min-width`** queries.
2. `prefers-reduced-motion`, `prefers-color-scheme`, `orientation`, etc.

### Footguns

1. `100vw` includes scrollbar gutter; content can exceed `100%` of visual viewport.
2. Reduce a track, switch to `auto`, use `minmax(0, 1fr)`, or move padding to a stable wrapper.

### Images

1. Height scales with width to preserve aspect ratio when width is constrained.
2. `width: 100%` can stretch some images awkwardly; `max-width` caps without forcing upscale beyond intrinsic width in many cases.
