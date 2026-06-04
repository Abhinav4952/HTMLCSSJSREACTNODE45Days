# Day 08 — Positioning & Stacking Context (Intro)

**Primary theme:** Taking elements out of normal flow on purpose—without losing predictability  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Related tasks:** `task-01-static-relative-playground`, `task-02-absolute-containing-block-challenge`, `task-03-fixed-header-sticky-sidebar`, `task-04-stacking-context-z-index-mystery`  
**Instruction alignment:** Maps to *Positioning* and an **intro** to stacking contexts that you will revisit when overlays/modals arrive in later UI tasks.

---

## Overview

Normal document flow is wonderful for reading order and accessibility, but some UI patterns require **out-of-flow** placement: badges on cards, sticky section headers, persistent app headers, and tooltips. CSS positioning is the toolkit—but it is also where beginners lose days because **the containing block** and **stacking contexts** are invisible until you learn to read them.

This day is intentionally framed as **engineering mechanics**, not memorization:

- `relative` keeps the element in flow but creates a positioning reference for descendants.
- `absolute` removes the element from flow and positions it relative to a **containing block** chosen by a rule chain—not “the parent.”
- `fixed` anchors to the viewport (mostly), except when transforms create a containing block elsewhere.
- `sticky` is a hybrid: in-flow until a threshold, then “sticks” like fixed—until an ancestor clips it.

The theory below includes **failure-first examples** (what breaks, why, how DevTools shows it). Use them as checklists while debugging Tasks 02 and 04.

---

## Day roadmap

1. [Normal flow vs out-of-flow (what actually changes)](#normal-flow-vs-out-of-flow-what-actually-changes)
2. [`position: relative` — local offsets + containing-block establishment](#position-relative--local-offsets--containing-block-establishment)
3. [`position: absolute` — containing blocks, shrink-to-fit, and scroll](#position-absolute--containing-blocks-shrink-to-fit-and-scroll)
4. [`position: fixed` — viewport anchoring and transform traps](#position-fixed--viewport-anchoring-and-transform-traps)
5. [`position: sticky` — thresholds, overflow clipping, and accessibility notes](#position-sticky--thresholds-overflow-clipping-and-accessibility-notes)
6. [Stacking contexts: what `z-index` really competes within](#stacking-contexts-what-z-index-really-competes-within)
7. [Deep dive — `isolation: isolate` and intentional stacking](#deep-dive--isolation-isolate-and-intentional-stacking)
8. [DevTools: positioning + layers panels (browser-dependent)](#devtools-positioning--layers-panels-browser-dependent)
9. [Common mistakes & debugging](#common-mistakes--debugging)
10. [Further reading](#further-reading)
11. [Glossary](#glossary)
12. [Answers (self-test)](#answers-self-test)

---

## Normal flow vs out-of-flow (what actually changes)

### What it is

**In-flow** boxes participate in block/inline layout and affect siblings. **Out-of-flow** (`absolute`, `fixed`, and floated elements historically) are laid out separately; siblings act as if out-of-flow elements don’t take space (except `relative`, which *does* reserve space).

#### Why it exists / why it matters

Out-of-flow is how you overlay UI without rewriting document order—but it increases the burden to manage **keyboard focus order** and **screen reader reading order** (later React days revisit portals and focus traps).

#### Pros and cons

- **Pros:** precise placement; sticky headers; badges.
- **Cons:** easier to create overlapping unreadable text and clipped focus rings.

#### What happens without it / when misused

- `absolute` without offsets can “stick” where static position would be—surprising.

#### Examples

**Tiny — relative nudges**

```css
.note {
  position: relative;
  top: 2px;
}
```

**Tiny — absolute removes space**

```css
.card {
  position: relative;
}
.badge {
  position: absolute;
  top: 10px;
  right: 10px;
}
```

#### Quick checks

1. Which `position` value still occupies its original gap in the layout?
2. Which values remove the element from normal flow (in the usual sense)?

---

## `position: relative` — local offsets + containing-block establishment

### What it is

`relative` offsets the box visually from its normal position while keeping its **layout footprint** as if it were not offset (unless you change too much). Importantly, `position: relative` (with `z-index` not `auto` in some cases) can participate in stacking contexts.

#### Why it exists / why it matters

It is the standard way to create a **local coordinate system** for absolutely positioned children.

#### Examples

```css
.frame {
  position: relative;
}
```

#### Quick checks

1. Does `top: 10px` on `relative` remove the element from flow?

---

## `position: absolute` — containing blocks, shrink-to-fit, and scroll

### What it is

An absolutely positioned element’s containing block is usually the nearest ancestor with **position not static**—but there are exceptions (transforms, filters, perspective, etc., can create containing blocks).

#### Why it exists / why it matters

Misidentifying the containing block is the #1 reason “`right: 0` is not aligning to my card.”

#### Examples

**Medium — wrong ancestor**

```css
.page { position: relative; }
.card { /* position static */ }
.badge { position: absolute; right: 0; top: 0; }
```

If `.page` is the nearest positioned ancestor, the badge aligns to `.page`, not `.card`.

#### Quick checks

1. If no positioned ancestor exists, what becomes the containing block for `absolute`?

---

## `position: fixed` — viewport anchoring and transform traps

### What it is

`fixed` usually anchors to the **viewport**, but if an ancestor has certain properties (e.g. `transform`), the fixed element may become fixed relative to that ancestor instead.

#### Quick checks

1. Name one CSS property on an ancestor that can break the “fixed to viewport” mental model.

---

## `position: sticky` — thresholds, overflow clipping, and accessibility notes

### What it is

`sticky` is like `relative` until scrolling crosses a threshold; then it behaves like `fixed` within its **sticky containing block** (nearest scrollport + certain ancestor constraints).

#### What happens without it / when misused

- An ancestor with `overflow: hidden` can prevent sticky from ever engaging.

#### Quick checks

1. Why might `sticky` never “stick” even though you set `top: 0`?

---

## Stacking contexts: what `z-index` really competes within

### What it is

A **stacking context** is a 3D sorting bucket. `z-index` only compares between elements **in the same context** (with caveats). New contexts are created by positioned elements with `z-index` not `auto`, flex/grid items with z-index, `opacity < 1`, `transform`, `filter`, and more.

#### Why it exists / why it matters

This is why a `z-index: 9999` child can still sit under a neighbor’s background: it’s in a different context.

#### Examples

**Tiny**

```css
.modal {
  position: fixed;
  inset: 0;
  z-index: 50;
}
```

#### Quick checks

1. If two siblings are both `position: relative` with `z-index` 1 and 2, which paints on top?

---

## Deep dive — `isolation: isolate` and intentional stacking

### What it is

`isolation: isolate` creates a **new stacking context** without needing hacks like `z-index: 0` on transformed parents in some cases.

### Why it matters

It helps teams build predictable overlay layers inside a component.

### Example

```css
.dropdownShell {
  position: relative;
  isolation: isolate;
}
```

---

## DevTools: positioning + layers panels (browser-dependent)

### What it is

Chrome’s **Layers** panel and Firefox’s **3D view** (where available) help visualize stacking. Always verify with computed `z-index` and ancestor properties.

---

## Deep dive — worked positioning recipes (copy/paste patterns)

### Recipe A — “Badge in top-right of card”

```css
.card {
  position: relative;
}
.badge {
  position: absolute;
  top: 10px;
  right: 10px;
}
```

### Recipe B — “Modal overlay covers viewport”

```css
.scrim {
  position: fixed;
  inset: 0;
  background: rgb(2 6 23 / 0.55);
}
```

### Recipe C — “Sticky section heading inside article”

```css
.article {
  /* avoid overflow:hidden on ancestors */
}
.article h2 {
  position: sticky;
  top: 0;
  background: #fff;
}
```

### Why these belong in Day 08

They are the three most common “first real UI” patterns that expose containing blocks and stacking immediately.

---

## Common mistakes & debugging

- Forgetting `position: relative` on intended anchor.
- Using huge `z-index` ladders instead of isolating contexts.
- `overflow: hidden` clipping sticky and focus outlines.

---

## Further reading

- [MDN — position](https://developer.mozilla.org/en-US/docs/Web/CSS/position)
- [MDN — containing block](https://developer.mozilla.org/en-US/docs/Web/CSS/Containing_block)
- [MDN — stacking context](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_positioned_layout/Understanding_z-index/Stacking_context)
- [CSS Positioned Layout](https://www.w3.org/TR/css-position-3/) (reference)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Containing block** | Rectangle used as a reference for sizing/positioning (depends on layout mode). |
| **Stacking context** | Isolated z-index sorting bucket. |

---

## Answers (self-test)

**Flow**

1. `relative` (still occupies original footprint).
2. `absolute`, `fixed` (and historically floats—out of normal flow in a different way).

**relative**

1. No—layout gap remains as if not offset (visual paint shifts).

**absolute**

1. The initial containing block / viewport-related rules per spec chain (simplified: viewport box in many cases).

**fixed trap**

1. Example: `transform` on an ancestor.

**sticky**

1. An ancestor may clip or prevent sticky behavior; sticky needs room to move within its scrollport.

**stacking**

1. `z-index: 2` sibling paints above `z-index: 1` if both establish comparable stacking participation rules.
