# Day 07 — Box Model, `box-sizing`, and Margin Collapse

**Primary theme:** How CSS boxes occupy space, how `border-box` changes the arithmetic, and why vertical margins sometimes “disappear” into each other  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks (challenge tasks may run longer)  
**Related tasks:** `task-01-box-model-measurement-sheet`, `task-02-margin-collapse-detective`, `task-03-border-box-migration-playground`, `task-04-triple-collapse-clinic`  
**Instruction alignment:** Maps to *CSS standards and the box model*, *`box-sizing`*, and the *margin collapse* behavior that underpins most “layout bugs” before Flex/Grid.

---

## Overview

Most beginners think CSS layout is about “putting divs in order.” Professionals know it is about **boxes**: every element generates rectangular areas that interact via **flow**, **positioning** (Day 08), and **formatting contexts**. The **box model** is the accounting spreadsheet for those rectangles: how much width/height is reserved for content vs padding vs border, and how margins create separation *without* painting a background.

`box-sizing: border-box` flips the default arithmetic so width/height include padding and border—this matches how designers think (“a 320px card” includes its padding). Without it, `width: 320px; padding: 16px` overflows the visual card width.

**Margin collapse** is the second half of today’s story: vertical margins between in-flow block boxes in the same formatting context often **combine** into a single margin rather than summing. This is not a browser bug; it is specified behavior that keeps typography pleasant (adjacent headings + paragraphs don’t double their spacing). It becomes painful when you expect additive margins in component systems.

This theory file is written to be **operationally useful**: after reading, you should be able to predict whether two margins will collapse, choose a fix that matches intent (BFC vs padding vs grid gap), and verify in DevTools.

---

## Day roadmap

1. [The standard box model: content, padding, border, margin](#the-standard-box-model-content-padding-border-margin)
2. [`box-sizing: content-box` vs `border-box`](#box-sizing-content-box-vs-border-box)
3. [Percentages, `auto`, and replaced elements (preview pitfalls)](#percentages-auto-and-replaced-elements-preview-pitfalls)
4. [Vertical margin collapsing: the core rules](#vertical-margin-collapsing-the-core-rules)
5. [Block formatting contexts (BFC) and `flow-root`](#block-formatting-contexts-bfc-and-flow-root)
6. [Negative margins: leverage vs footguns](#negative-margins-leverage-vs-footguns)
7. [DevTools: measuring boxes like an engineer](#devtools-measuring-boxes-like-an-engineer)
8. [Deep dive — collapsing through empty elements and `min-height: 0` teasers](#deep-dive--collapsing-through-empty-elements-and-min-height-0-teasers)
9. [Common mistakes & debugging](#common-mistakes--debugging)
10. [Further reading](#further-reading)
11. [Glossary](#glossary)
12. [Answers (self-test)](#answers-self-test)

---

## The standard box model: content, padding, border, margin

### What it is

For a typical block-level element, CSS layout thinks in layers:

1. **content box** — where text/images live; `width`/`height` usually refer here in `content-box` mode.
2. **padding box** — extends around content; painted with background color/image.
3. **border box** — extends around padding; border styles paint here.
4. **margin box** — extends around border; transparent, but participates in spacing.

`outline` and `box-shadow` are **not** part of the classic “size” for `width`/`height` in the same way as border (outline doesn’t occupy layout space; shadows can visually extend outside without affecting flow).

#### Why it exists / why it matters

If you mis-identify which box your `width` applies to, you will ship components that overflow their parent by exactly `2 × padding + 2 × border`—a classic “off by 32px” bug.

#### Pros and cons

- **Pros:** predictable layering; backgrounds and borders align intuitively.
- **Cons:** two different `box-sizing` modes in one codebase creates mental overhead.

#### What happens without it / when misused

- A “320px card” becomes 352px wide with 16px padding on each side in `content-box`.

#### Syntax and rules

```css
.demo {
  width: 320px;
  padding: 16px;
  border: 1px solid #cbd5e1;
  margin: 12px;
}
```

#### Examples

**Tiny — content box mental math**

```txt
border-box outer width (content-box mode) ≈ width + padding-left + padding-right + border-left + border-right
```

**Tiny — background fills padding**

```css
.panel {
  background: #f8fafc;
  padding: 1rem;
}
```

**Medium — inline vs block replaced elements**

```html
<img alt="" width="240" height="160" />
```

Images are replaced elements; their intrinsic size interacts with `max-width: 100%` patterns (responsive images later).

#### Quick checks

1. In `content-box`, does `width` include padding?
2. Which box paints `background-color` under default CSS backgrounds?
3. Does `outline` affect layout size between two adjacent blocks?

---

## `box-sizing: content-box` vs `border-box`

### What it is

- `content-box` (CSS default historically): `width`/`height` apply to **content** only.
- `border-box`: `width`/`height` apply to **border box** (including padding and border, not margin).

#### Why it exists / why it matters

`border-box` matches most UI component specs: “button is 40px tall” includes padding.

#### Pros and cons

- **Pros:** fewer overflow surprises in responsive grids.
- **Cons:** mixing modes across third-party widgets can confuse width calculations.

#### What happens without it / when misused

- Global `* { box-sizing: border-box; }` is common; forgetting it on a web component host can reintroduce `content-box`.

#### Syntax and rules

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}
```

#### Examples

**Tiny**

```css
.card {
  width: min(360px, 100%);
  padding: 1rem;
}
```

**Medium — two-column math**

```css
.col {
  width: 50%;
  padding: 1rem;
}
```

With `border-box`, two `50%` columns often fit; with `content-box`, they may overflow due to padding.

#### Quick checks

1. Which mode makes `width: 100%` inside a padded parent less likely to overflow?
2. Does `border-box` include margin in `width`?

---

## Percentages, `auto`, and replaced elements (preview pitfalls)

### What it is

Many properties accept percentages that resolve against **containing block** widths/heights—rules differ per property (Day 06 preview: vertical margin percentages use containing block **width**).

#### Why it exists / why it matters

This is the root of “why doesn’t `% height` work?” questions.

#### Pros and cons

- **Pros:** fluid layouts.
- **Cons:** requires knowing the containing block chain.

#### Examples

**Tiny**

```css
.child {
  height: 100%;
}
```

Only works if parent’s height is definite.

#### Quick checks

1. Why is `% height` often harder than `% width` in normal flow layouts?

---

## Vertical margin collapsing: the core rules

### What it is

In normal block flow, **adjacent vertical margins** of in-flow block-level boxes can **collapse** to the **maximum** of the participating margins (with additional rules for negative margins producing a sum algorithm).

Common cases:

- sibling `margin-bottom` + `margin-top`
- parent’s `margin-top` with first child’s `margin-top` (under conditions)
- empty blocks with only margins

#### Why it exists / why it matters

Typography spacing would become too airy if heading bottom margin and paragraph top margin always summed.

#### Pros and cons

- **Pros:** nicer default reading rhythm.
- **Cons:** layout systems that expect additive margins break unless you establish a formatting context.

#### What happens without it / when misused

- “I set `margin-top: 24px` on the section but nothing moved” because it collapsed with the child.

#### Syntax and rules (fixes, not “syntax”)

Pick one:

- `padding-top` on parent instead of margin on child
- `border-top` on parent (even 1px transparent)
- `display: flow-root` / new BFC (`overflow: hidden` etc.)
- use **gap** in flex/grid (later days) instead of margin stacks

#### Examples

**Tiny — collapse**

```css
h2 { margin: 0 0 12px; }
p { margin: 12px 0 0; }
/* collapsed vertical gap is 12px, not 24px */
```

**Medium — prevent parent/child collapse with padding**

```css
section {
  padding-top: 0.1px; /* classic hack; prefer flow-root today */
}
```

#### Quick checks

1. Do horizontal margins collapse between adjacent siblings in normal flow?
2. What is a modern, intentional way to create a new block formatting context for a component root?

---

## Deep dive — a margin-collapse decision tree (for the detective tasks)

### What it is

A practical recipe you can literally follow when spacing “doesn’t add up”:

1. **Confirm axis:** collapse applies to **vertical** margins in normal block flow in many common cases—not a universal rule for all layout modes.
2. **Identify participants:** list the two margins that touch at a boundary (sibling boundary, or first/last child boundary with parent).
3. **Check for BFC boundaries:** margins don’t collapse through certain separation conditions; `flow-root`, `overflow` not `visible`, `padding`, and `border` can change outcomes.
4. **Negative margins:** they don’t “cancel collapse”; they participate in a defined max/negative algorithm—use DevTools to see the computed result.
5. **Prefer non-collapsing spacing for systems:** `gap`, `padding`, or explicit grid tracks reduce mystery.

### Why it exists / why it matters

This is the difference between randomly tweaking numbers and making a **one-minute diagnosis** in DevTools.

### Examples

**Tiny — sibling collapse**

```html
<section>
  <h2 style="margin: 0 0 12px">Title</h2>
  <p style="margin: 12px 0 0">Body</p>
</section>
```

**Medium — internal vs external collapse**

```css
.card {
  display: flow-root;
}
```

> `flow-root` helps with **outer** margin behavior and containing floats, but **internal** adjacent siblings can still collapse with each other inside the same BFC. If you need guaranteed additive separation between internal siblings, use `padding` on a wrapper, `row-gap` in flex, or adjust margins so only one side carries the spacing responsibility.

### Quick checks

1. Does `flow-root` guarantee non-collapsing margins between a heading and paragraph inside the same card?
2. Name a spacing mechanism that does not collapse.

---

## Block formatting contexts (BFC) and `flow-root`

### What it is

A **BFC** is a region where internal layout rules are isolated: floats are contained, margins may not collapse through the boundary the same way, etc.

`display: flow-root` creates a BFC without the side effects of `overflow: hidden` (clipping).

#### Why it exists / why it matters

`flow-root` is the clean “component root” tool for stopping margin collapse from leaking.

#### Examples

```css
.component {
  display: flow-root;
}
```

#### Quick checks

1. Why might `overflow: hidden` be an undesirable BFC hack for a dropdown-heavy component?

---

## Negative margins: leverage vs footguns

### What it is

Negative margins pull boxes closer; used in “full bleed inside constrained container” patterns and some grid hacks.

#### Why it exists / why it matters

Can fix alignment, but can also cause overlap and pointer-event confusion.

#### Quick checks

1. Can negative margins break collapsing math? (Yes—negative margins participate in the max algorithm differently; learn by experimenting in DevTools today.)

---

## DevTools: measuring boxes like an engineer

### What it is

Use **Layout** panel overlays: margin (orange), border (yellow), padding (green), content (blue). Toggle them while toggling `box-sizing`.

#### Quick checks

1. Which color is margin in Firefox’s box model diagram?

---

## Deep dive — collapsing through empty elements and `min-height: 0` teasers

### What it is

Empty blocks with margins can collapse in surprising ways; also, flex items default `min-height: auto` can block shrinking (Day 14 preview)—not today’s main deliverable, but connected to “why spacing looks wrong.”

### Why it matters

Students often add empty `<div>` spacers—often an anti-pattern—then get unpredictable collapse.

### Examples

Avoid spacer divs; use gap, padding, or explicit layout.

---

## Common mistakes & debugging

- Assuming margins always add.
- Using `height: 100%` without establishing a height chain.
- Mixing `content-box` on some components only—standardize per repo unless forced.

---

## Further reading

- [MDN — Box model](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/The_box_model)
- [MDN — box-sizing](https://developer.mozilla.org/en-US/docs/Web/CSS/box-sizing)
- [MDN — Mastering margin collapsing](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_box_model/Mastering_margin_collapsing)
- [CSS2.1 collapsing margins spec (reference)](https://www.w3.org/TR/CSS21/box.html#collapsing-margins)

---

## Glossary

| Term | Meaning |
|------|---------|
| **BFC** | Block formatting context: isolates internal layout in several ways. |
| **Margin collapse** | Vertical margins combine per CSS rules instead of always summing. |

---

## Answers (self-test)

**Box model**

1. No in `content-box`—`width` is content width only.
2. Padding box (background defaults).
3. Outline does not affect layout box placement like border does (generally no layout size).

**box-sizing**

1. `border-box` (given typical responsive patterns).
2. No—margin is always outside the border box.

**Percent height**

1. Parent height is often `auto`, so percentage height can’t resolve as expected.

**Margin collapse**

1. No—horizontal margins do not collapse the same way in normal flow left/right separation contexts.
2. `display: flow-root` on the component root (preferred modern approach) among other BFC triggers.

**DevTools**

1. Orange for margin in many DevTools themes (Firefox/Chrome); always verify legend in your browser.

**Collapse decision tree (deep dive)**

1. No—`flow-root` does not automatically prevent internal sibling margin collapse; it mostly prevents collapse through the box’s outer boundary and helps contain floats.
2. Examples: `gap` in flex/grid; padding on a wrapper; single-sided margin ownership; `border-top` separation.
