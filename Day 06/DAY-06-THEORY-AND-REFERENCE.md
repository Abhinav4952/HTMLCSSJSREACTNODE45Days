# Day 06 — Shadows & CSS Units

**Primary theme:** Light, depth, and scale—how shadows communicate affordance, and how CSS length units anchor geometry to the viewport, root font size, or element-local font metrics  
**Estimated study time:** 2–3 hours theory + 4–7 hours tasks (Task 03–04 intentionally longer)  
**Related tasks:** `task-01-shadow-studio-cards`, `task-02-fluid-type-clamp-and-viewport`, `task-03-em-rem-compounding-trap`, `task-04-css-length-math-lab`  
**Instruction alignment:** Maps to *Box and text shadow* and *CSS units* from the master topic list; introduces **fluid type** patterns you will reuse on responsive days.

---

## Overview

On real products, “pretty shadows” are rarely decoration for its own sake. Shadows answer **where** an element sits in space: flat on the page, raised like a button, inset like a well, or highlighted like a focused control. Misused shadows add noise, reduce contrast, and can even harm motion-sensitive users when paired with animation (later days).

Units are the **coordinate system** of your stylesheet. `px` is stable but ignores user font preferences unless you build around them; `rem` tracks the root and is the usual baseline for scalable UI; `em` is powerful for component-local scaling but **compounds** inside nested typography; `vw`/`vh` tie layout to the viewport—powerful for hero typography and full-bleed sections, but hazardous when used naïvely for critical text sizes (small viewports + large `vw` can produce unreadably small type unless clamped).

Today’s theory is intentionally **long and concrete**: you should finish it with “rules of thumb” you can apply without memorizing every edge case, and with a mental checklist for debugging shadows/units regressions in DevTools.

---

## Day roadmap

1. [Light, elevation, and layered `box-shadow`](#light-elevation-and-layered-box-shadow)
2. [`text-shadow`: readability, depth, and failure modes](#text-shadow-readability-depth-and-failure-modes)
3. [Absolute units: `px`, `pt` (mention only), physical units](#absolute-units-px-pt-mention-only-physical-units)
4. [Font-relative units: `rem` vs `em` (compounding)](#font-relative-units-rem-vs-em-compounding)
5. [Viewport units: `vw`, `vh`, `vmin`, `vmax`, and the *small/large/dynamic* viewport variants (conceptual)](#viewport-units-vw-vh-vmin-vmax-and-the-small-large-dynamic-viewport-variants-conceptual)
6. [Fluid typography with `clamp()`](#fluid-typography-with-clamp)
7. [Accessibility & user settings that intersect units](#accessibility--user-settings-that-intersect-units)
8. [DevTools workflows: what to inspect when shadows/units “look wrong”](#devtools-workflows-what-to-inspect-when-shadowsunits-look-wrong)
9. [Common mistakes & debugging](#common-mistakes--debugging)
10. [Further reading](#further-reading)
11. [Glossary](#glossary)
12. [Answers (self-test)](#answers-self-test)

---

## Light, elevation, and layered `box-shadow`

### What it is

`box-shadow` paints one or more drop shadows **around the element’s border box** (subject to `border-radius`). Each shadow list entry can specify:

- **inset** (inner shadow),
- **offset-x / offset-y**,
- **blur-radius**,
- **spread-radius**,
- **color**.

Multiple shadows are separated by commas; the **first** listed is painted **on top** in the stacking sense for overlapping shadow regions (think painter’s algorithm between shadow layers).

#### Why it exists / why it matters

Humans infer **elevation** from subtle cues: a card “floats” when its shadow is soft and displaced downward; a pressed button reads as inset. Material-style UIs historically used many layered shadows; flatter systems still use **one** carefully tuned shadow for separation.

Shadows also create **focus affordance** when combined with `:focus-visible` outlines—but be careful: relying *only* on shadow for focus can fail in high-contrast themes or for users who disable shadows.

#### Pros and cons

- **Pros:** Vector crisp at any DPI; easy to tweak live in DevTools.
- **Pros:** Multiple layers can mimic ambient + key light cheaply.
- **Cons:** Too-strong shadows reduce perceived contrast and look “muddy” on low-quality displays.
- **Cons:** Large blur radii can hurt performance on huge elements or when many animated shadows exist (GPU fill-rate costs).

#### What happens without it / when misused

- **Muddy stacking:** identical offsets with huge blur on similar colors produces a gray smear.
- **False affordance:** heavy shadow on non-interactive panels can look clickable.
- **WCAG contrast issues:** dark shadow on dark text is rare, but colored shadows on small text can reduce legibility.

#### Syntax and rules

Canonical modern pattern (two-layer elevation):

```css
.card {
  box-shadow:
    0 1px 2px rgb(15 23 42 / 0.08),
    0 8px 24px rgb(15 23 42 / 0.08);
}
```

Inset panel:

```css
.inset {
  box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.6);
}
```

Spread can fake a “border” without affecting layout:

```css
.ring {
  box-shadow: 0 0 0 3px #0ea5e9;
}
```

#### Examples

**Tiny — single shadow**

```css
button {
  box-shadow: 0 1px 0 rgb(15 23 42 / 0.12);
}
```

**Tiny — inset “well”**

```css
input {
  box-shadow: inset 0 1px 2px rgb(15 23 42 / 0.12);
}
```

**Medium — focus ring pattern (outline still recommended)**

```css
.card:focus-visible {
  outline: 2px solid #0ea5e9;
  outline-offset: 2px;
  box-shadow: 0 0 0 4px rgb(14 165 233 / 0.25);
}
```

**Medium — “ambient + key”**

```css
.sheet {
  border-radius: 12px;
  box-shadow:
    0 0 0 1px rgb(15 23 42 / 0.06),
    0 10px 30px rgb(2 6 23 / 0.18);
}
```

**Large — interactive elevation steps (conceptual)**

```css
.btn {
  box-shadow: 0 1px 1px rgb(15 23 42 / 0.08);
  transform: translateY(0);
}
.btn:hover {
  box-shadow: 0 6px 18px rgb(2 6 23 / 0.12);
  transform: translateY(-1px);
}
.btn:active {
  box-shadow: inset 0 2px 6px rgb(2 6 23 / 0.12);
  transform: translateY(0);
}
```

> Note: combine shadow changes with motion preferences (`prefers-reduced-motion`) on real projects (you’ll formalize this on later days).

#### Quick checks (self-test)

1. In a multi-layer `box-shadow`, if two shadows overlap, which layer tends to appear visually dominant where they conflict?
2. Name one disadvantage of using only `box-shadow` as a focus indicator.
3. What does the `spread` radius do that blur cannot do alone?

---

## `text-shadow`: readability, depth, and failure modes

### What it is

`text-shadow` applies blur-based shadows to glyph outlines. It supports multiple comma-separated layers, each with **x-offset, y-offset, blur-radius, color** (no spread).

#### Why it exists / why it matters

`text-shadow` can improve **readability** of text on busy photography backgrounds (subtle dark halo behind light text), or add stylistic depth for headings. It is *not* a replacement for sufficient color contrast against the immediate background.

#### Pros and cons

- **Pros:** Cheap halo effect without extra DOM.
- **Pros:** Multiple layers can create crisp “stroke-like” edges when offsets are tiny and blur is small.
- **Cons:** Large blur on body text looks smudged and reduces reading speed.
- **Cons:** Overused glow reads dated and can trigger discomfort for some users when animated.

#### What happens without it / when misused

- **Glow on long paragraphs:** cognitive load increases; keep glow on headings or single-line hero text.
- **Rainbow glow stacks:** accessibility and brand consistency suffer.

#### Syntax and rules

```css
.hero {
  color: #f8fafc;
  text-shadow: 0 2px 18px rgb(2 6 23 / 0.55);
}
```

Tiny offsets + small blur mimic outline:

```css
h1 {
  text-shadow:
    0 1px 0 rgb(2 6 23 / 0.25),
    0 -1px 0 rgb(2 6 23 / 0.12);
}
```

#### Examples

**Tiny — readability halo**

```css
.on-photo {
  text-shadow: 0 1px 2px rgb(2 6 23 / 0.8);
}
```

**Tiny — “letterpress” (very subtle)**

```css
h2 {
  color: #334155;
  text-shadow: 0 1px 0 rgb(255 255 255 / 0.65);
}
```

**Medium — two-layer heading glow**

```css
.display {
  text-shadow:
    0 0 1px rgb(2 6 23 / 0.35),
    0 18px 40px rgb(2 6 23 / 0.35);
}
```

#### Quick checks

1. Why should long body copy avoid large `text-shadow` blur?
2. What is a legitimate readability use of `text-shadow` over photography?
3. Does `text-shadow` affect layout box size?

---

## Absolute units: `px`, `pt` (mention only), physical units

### What it is

A **CSS pixel** (`px`) is an **absolute** unit in CSS semantics: it does *not* mean “one hardware pixel” on all devices; it is the canonical “css px” anchoring other units. For authoring UI, `px` is still common for **borders**, **shadows**, and fine-tuned spacing.

`pt` and physical units (`cm`, `in`) show up in print stylesheets; screen UI rarely uses them.

#### Why it exists / why it matters

`px` is stable when you need **1px hairlines** or pixel-perfect shadow offsets. Design tools often export px.

#### Pros and cons

- **Pros:** predictable; great for thin borders and shadow offsets.
- **Cons:** does not scale with user root font size changes unless you pair px-based layout with rem-based typography intentionally.
- **Cons:** can encourage “fixed” layouts if used for everything.

#### What happens without it / when misused

- **Everything in px:** users who set large default fonts may still see small text if font sizes are locked in px.

#### Syntax and rules

```css
.rule {
  border-top: 1px solid #e2e8f0;
}
```

#### Examples

**Tiny**

```css
:root {
  --hairline: 1px;
}
```

**Tiny — shadow offsets in px**

```css
.elev {
  box-shadow: 0 10px 24px rgb(2 6 23 / 0.12);
}
```

**Medium — mixing px borders with rem padding**

```css
.card {
  border: 1px solid #e2e8f0;
  padding: 1rem;
}
```

#### Quick checks

1. In CSS, does `1px` always map 1:1 to a device hardware pixel?
2. Name one property where px remains a strong default choice.
3. Why might an all-px typography scale be problematic for accessibility?

---

## Font-relative units: `rem` vs `em` (compounding)

### What it is

- **`rem`**: “root em” — relative to the **root element** (`<html>`) computed font-size (browser default often 16px unless changed).
- **`em`**: relative to **this element’s** computed font-size (which may have been set by a parent in `em`, so it can compound).

#### Why it exists / why it matters

`rem` is the workhorse for **component padding + typography** that should respect user font scaling. `em` is excellent for **proportional scales inside a component** (padding em tied to local heading size).

#### Pros and cons

- **Pros (rem):** predictable scaling; minimal surprise in nested trees.
- **Pros (em):** local scaling—if heading grows, spacing tied in em grows harmoniously.
- **Cons (em):** nested lists / nested components with font-size in em can explode/shrink unintentionally.
- **Cons:** mixing em padding with em font-size on ancestors requires mental multiplication.

#### What happens without it / when misused

Nested pattern:

```html
<div class="wrap">
  <div class="wrap">
    <p>Text</p>
  </div>
</div>
```

If `.wrap { font-size: 0.9em; }`, nested wraps compound: \(0.9^n\) shrinks quickly.

#### Syntax and rules

```css
html {
  font-size: 100%;
}
h1 {
  font-size: 2rem;
}
.callout {
  font-size: 0.95rem;
  padding: 1rem; /* rem padding: tied to root, not callout font-size */
}
.local {
  font-size: 1.25em;
  padding: 1em; /* padding tied to .local’s computed font-size */
}
```

#### Examples

**Tiny — rem padding**

```css
button {
  padding: 0.5rem 0.75rem;
}
```

**Tiny — em line height**

```css
p {
  font-size: 1rem;
  line-height: 1.6; /* unitless preferred; still related to font-size */
}
```

**Medium — em-based “chip” scales with parent**

```css
.toolbar {
  font-size: 0.875rem;
}
.chip {
  font-size: 1em;
  padding: 0.25em 0.5em;
  border-radius: 999px;
}
```

**Medium — rem-based “card” avoids compounding**

```css
.card {
  font-size: 1rem;
  padding: 1.25rem;
}
.card h2 {
  font-size: 1.25rem;
}
```

#### Quick checks

1. If `html { font-size: 100%; }` and user sets browser default to 20px, what is `1rem`?
2. Why does `em` padding on a child depend on that child’s computed font-size?
3. Name a UI pattern where `em` is nicer than `rem`.

---

## Viewport units: `vw`, `vh`, `vmin`, `vmax`, and the *small/large/dynamic* viewport variants (conceptual)

### What it is

- `1vw` = 1% of the **viewport width**
- `1vh` = 1% of the **viewport height**
- `vmin` / `vmax` pick smaller/larger of vw and vh

Modern mobile browsers complicate `vh` due to dynamic browser chrome; CSS has introduced **svh/lvh/dvh** (small/large/dynamic viewport height units). You should know they exist even if you mostly author with `clamp()` + `rem` today.

#### Why it exists / why it matters

Viewport units enable **full-bleed** sections and fluid headlines (“10vw titles”) that feel cinematic.

#### Pros and cons

- **Pros:** responsive without many breakpoints for some effects.
- **Cons:** `vw` typography can violate readability minima on narrow screens unless clamped.
- **Cons:** `100vh` panels can overflow under mobile browser UI unless using `dvh`/`svh` patterns.

#### What happens without it / when misused

- Headline `font-size: 6vw` on a 320px phone → tiny math if you expected “big type” incorrectly—always clamp.

#### Syntax and rules

```css
.hero-title {
  font-size: clamp(1.75rem, 2.8vw + 1rem, 3.25rem);
}
```

Full-bleed width:

```css
.full {
  width: 100vw;
  margin-inline: calc(50% - 50vw);
}
```

> The `full` pattern is powerful but can create horizontal scroll if combined with vertical scrollbars in some layouts—treat as advanced; your Day 06 tasks avoid it unless explicitly requested.

#### Examples

**Tiny — min/max fluid padding**

```css
section {
  padding-inline: clamp(1rem, 4vw, 2.5rem);
}
```

**Tiny — vmin-based icon grid gap**

```css
.grid {
  gap: clamp(0.5rem, 1.5vmin, 1rem);
}
```

**Medium — safe hero height (conceptual)**

```css
.hero {
  min-height: min(70vh, 720px);
}
```

#### Quick checks

1. Why is raw `font-size: 8vw` risky for accessibility?
2. What does `vmin` measure on a phone in portrait?
3. Name one reason `100vh` is sometimes frustrating on mobile browsers.

---

## Fluid typography with `clamp()`

### What it is

`clamp(MIN, PREFERRED, MAX)` chooses:

- `MIN` if `PREFERRED` is smaller,
- `MAX` if `PREFERRED` is larger,
- otherwise `PREFERRED`.

A common preferred value uses `vw` plus a rem offset to “tilt” the slope.

#### Why it exists / why it matters

Fluid type reduces the number of breakpoints you maintain while keeping text within readable bounds—**if** you choose MIN/MAX responsibly.

#### Pros and cons

- **Pros:** smooth scaling across viewport widths.
- **Cons:** bad coefficients can still produce too-small text inside nested containers if you confuse container width with viewport width.

#### Syntax and rules

```css
h1 {
  font-size: clamp(1.75rem, 0.6rem + 2.2vw, 3rem);
}
```

#### Examples

**Tiny — fluid gap**

```css
.stack > * + * {
  margin-top: clamp(0.75rem, 0.2rem + 1.6vw, 1.5rem);
}
```

**Medium — fluid container**

```css
.page {
  width: min(1100px, calc(100% - clamp(1rem, 4vw, 3rem)));
  margin-inline: auto;
}
```

#### Quick checks

1. In `clamp(1rem, 2vw, 3rem)`, which argument is evaluated first conceptually?
2. Why add a rem term inside the preferred value (e.g. `0.75rem + 2vw`)?
3. What is a symptom of choosing `MIN` too small for body text?

---

## Accessibility & user settings that intersect units

### What it is

Users may change:

- default font size,
- minimum font size,
- page zoom,
- forced colors / high contrast.

Your `rem`/`em` choices mostly respect font size changes; raw `vw` sizing may **not**.

#### Why it exists / why it matters

WCAG is not “px compliance only”—user scaling is part of real-world accessibility.

#### Pros and cons

- **Pros:** `rem` typography + adequate contrast survives more user settings.
- **Cons:** viewport-only sizing fights user overrides unless bounded.

#### What happens without it / when misused

- Tiny text that passes a design mock at 1440px but fails human readability at 320px.

#### Syntax and rules

Prefer:

```css
p {
  font-size: clamp(1rem, 0.95rem + 0.2vw, 1.125rem);
}
```

#### Examples

**Tiny — respect focus**

```css
:focus-visible {
  outline: 3px solid;
  outline-offset: 2px;
}
```

#### Quick checks

1. Which unit tracks user’s root font-size changes most directly for element font sizes?
2. Why is `clamp()` considered an accessibility tool when used correctly?
3. Should animated shadow pulses ever be unconditional?

---

## DevTools workflows: what to inspect when shadows/units “look wrong”

### What it is

A practical checklist:

1. **Computed** panel: verify computed `font-size` on nested `em` elements.
2. **Layout** panel: margin/border/padding boxes for unexpected spacing (Day 07 deepens).
3. Toggle **prefers-color-scheme** emulation: shadows that looked fine in light mode may disappear on dark backgrounds.

#### Why it exists / why it matters

Most “CSS bugs” are actually **wrong assumptions about computed values**—especially `em` and percentage padding.

#### Pros and cons

- **Pros:** DevTools turns guessing into measurement.
- **Cons:** too many toggles; learn a repeatable checklist instead.

#### What happens without it / when misused

- Students tweak shadow blur randomly instead of measuring offset/blur ratio against a reference card.

#### Syntax and rules

Use box model overlay; copy computed styles into notes.

#### Examples

**Tiny — console math**

```js
// If root font is 16px, how many px is 1.25rem?
1.25 * 16; // 20
```

#### Quick checks

1. Which DevTools tab shows the cascade winner for a shadow overridden by another rule?
2. What computed value should you read first when debugging `em` surprises?

---

## Deep dive — designing shadow “ramps” like a tiny design system

### What it is

Instead of inventing a new shadow for every card, define **3–5 elevation levels** as CSS variables:

```css
:root {
  --shadow-1: 0 1px 2px rgb(15 23 42 / 0.08);
  --shadow-2: 0 6px 18px rgb(2 6 23 / 0.12);
  --shadow-3: 0 18px 48px rgb(2 6 23 / 0.16);
}
```

### Why it exists / why it matters

Consistency is how users learn what is interactive, what is background, and what is “selected.” Random shadows are a common symptom of multiple authors or copy/paste drift.

### Pros and cons

- **Pros:** one place to tune brand elevation when background color changes.
- **Cons:** over-parameterizing shadows (10 variables) is hard to maintain—keep the ramp small.

### What happens without it / when misused

- Cards in the same page look like they belong to different products.

### Syntax and rules

Map components to levels:

- static panels: `--shadow-1`
- hoverable cards: `--shadow-2` on hover
- modals: `--shadow-3`

### Examples

**Tiny — tokenized**

```css
.card {
  box-shadow: var(--shadow-1);
}
.card:hover {
  box-shadow: var(--shadow-2);
}
```

**Medium — dark mode swap**

```css
:root[data-theme="dark"] {
  --shadow-2: 0 10px 30px rgb(0 0 0 / 0.55);
}
```

### Quick checks

1. Why is a “shadow ramp” easier to maintain than per-component magic numbers?
2. What is a simple rule for deciding hover elevation vs resting elevation?

---

## Deep dive — `calc()`, percentages, and “where is the percentage measured?”

### What it is

Many properties accept percentages that resolve against **different reference axes**:

- `margin-top: 10%` resolves against the **width** of the containing block (CSS quirk historically—true for vertical margins too in normal flow).
- `height: 50%` often needs an explicit parent height chain to resolve predictably.

`calc()` combines incompatible units safely:

```css
width: calc(100% - 2rem);
```

### Why it exists / why it matters

This is a frequent source of “my % height doesn’t work” bugs that students blame on units day—but it’s really **percentage resolution rules**.

### Pros and cons

- **Pros:** `calc()` expresses intent (“full width minus gutter”) clearly.
- **Cons:** nested `calc()` becomes hard to read—split into variables when possible.

### What happens without it / when misused

- `height: 100%` on children without a definite parent height yields `auto` behavior surprises.

### Examples

**Tiny**

```css
.main {
  width: min(1100px, calc(100% - 2rem));
}
```

**Medium**

```css
.sidebar {
  flex: 0 0 calc(240px + 2vw);
}
```

### Quick checks

1. For normal-flow elements, percentage vertical margins resolve against which axis of the containing block?
2. Why does `height: 100%` fail surprisingly often on `body > div` layouts?

---

## Study drills (optional but recommended)

1. Take one shadow from a product you like; recreate it with **two** comma-separated layers in DevTools until it’s visually close.
2. Build a 3-level type scale using **only** `rem`, then rebuild using **only** `em` inside a wrapper—observe compounding.
3. Take a `clamp()` headline and graph its computed `font-size` at 320px, 768px, 1280px widths using DevTools.

---

## Common mistakes & debugging

- **Shadow mud:** blur too large relative to offset; reduce blur or lower alpha.
- **Double shadows on nested rounded cards:** children inherit none, but visually looks stacked—check backgrounds.
- **`em` explosion:** nested `font-size: 0.9em` stacks—switch inner to `rem` or stop nesting font-size changes.
- **`vw` too small:** clamp MIN too low—raise MIN to a readable body size.
- **Horizontal scroll with `100vw`:** scrollbar width issues—avoid `100vw` full-bleed hacks until taught.

---

## Further reading

- [MDN — box-shadow](https://developer.mozilla.org/en-US/docs/Web/CSS/box-shadow)
- [MDN — text-shadow](https://developer.mozilla.org/en-US/docs/Web/CSS/text-shadow)
- [MDN — CSS values and units](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Values_and_units)
- [MDN — clamp()](https://developer.mozilla.org/en-US/docs/Web/CSS/clamp)
- [W3C — CSS Values and Units Module](https://www.w3.org/TR/css-values-4/) (reference; skim “font-relative” and “viewport”)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Layered shadow** | Comma-separated multiple `box-shadow` / `text-shadow` entries. |
| **`rem`** | Relative to root element font size. |
| **`em`** | Relative to this element’s computed font size (compounds when font-size itself is in em). |
| **`clamp()`** | Chooses bounded value between MIN and MAX around a preferred expression. |

---

## Answers (self-test)

**`box-shadow`**

1. Earlier-listed shadows paint “above” later ones where they overlap (painter’s algorithm for shadows).
2. Shadows may be suppressed or imperceptible in some high-contrast modes; prefer visible outlines too.
3. Spread grows/shrinks the shadow shape uniformly before blur, enabling tight “rings”.

**`text-shadow`**

1. Large blur reduces edge clarity and reading speed.
2. Halo behind glyphs to separate text from busy imagery.
3. No—text-shadow is a paint effect; it doesn’t change layout metrics.

**`px`**

1. No—CSS px maps through device pixel ratio and zoom transforms.
2. 1px borders/hairlines; precise shadow offsets.
3. User font preferences may not propagate into px-locked typography.

**`rem`/`em`**

1. 20px (assuming rem resolves against 20px root).
2. Because `em` uses the element’s own computed font-size as its basis, and padding in em uses that same basis.
3. Padding that should scale with local heading size inside a component.

**Viewport units**

1. It can go below readable minima on small screens without clamping.
2. The smaller of vw and vh in the current orientation.
3. Mobile browser UI shows/hides, changing visible viewport height; `vh` can be “too tall”.

**`clamp()`**

1. The browser computes the preferred value, then clamps it—conceptually: compute preferred, then min/max bound.
2. Adds a baseline in rem so preferred isn’t purely viewport-driven.
3. Users see uncomfortably small body copy at common phone widths.

**DevTools**

1. **Computed** shows winning declarations; **Styles** shows cascade and struck-through rules.
2. Computed `font-size` on the element before judging `em` padding.

**Shadow ramp**

1. One tuning pass updates many components; fewer arbitrary values.
2. Hover elevation should be one step above resting, not a different species of shadow unless intentionally dramatic.

**Percent/`calc()`**

1. The **width** of the containing block (CSS percentage margin rule in normal flow).
2. Percent height needs an explicit height chain; many parents only have `min-height` or `auto` height, so percentage height can’t resolve as expected.
