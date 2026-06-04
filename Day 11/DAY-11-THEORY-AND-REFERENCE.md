# Day 11 — Cascade, Inheritance, Specificity, and Opacity

**Primary theme:** How browsers decide *which* CSS declaration applies when rules collide, how values flow down the tree via inheritance, and how transparency differs depending on whether you use `opacity` vs alpha channels in colors  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks (challenge tasks may run longer)  
**Related tasks:** `task-01-inheritance-and-custom-properties-playground`, `task-02-specificity-duel-scoreboard`, `task-03-opacity-stacking-clinic`, `task-04-cascade-specificity-lab`  
**Instruction alignment:** Maps to *Cascading and inheritance*, *Opacity*, and reinforces *CSS rules and selectors* from the master topic list.

---

## Overview

CSS is not “the last rule wins.” It is a **priority system** that compares declarations from different stylesheets, author styles, user styles, inline styles, animations, transitions, and browser defaults. For most day-to-day debugging, you live in a smaller slice: **author stylesheets**, where the cascade compares **importance** (`!important`), **origin layers** (later `@layer` blocks vs unlayered rules—preview only today), **specificity**, and finally **source order**.

Parallel to the cascade, **inheritance** answers a different question: when a property is not specified on an element, does it **reuse** a value from its parent? Inherited properties (`color`, `font-size`, many typography-related properties) create a “defaults flow” down the tree. Non-inherited properties snap to **initial** values unless you set them explicitly—this is why a `<button>` inside a colored `<div>` does not automatically inherit the same border or background.

**Opacity** is often taught as “make things see-through,” but it behaves like a **post-processing group**: `opacity` on a parent multiplies the effective transparency of all descendants together, which surprises people who expected “only the background” to fade. Alpha in `rgba()`/`hsla()` is usually attached to **a single property** (often `background-color`), which does not create the same grouping effect.

This day connects directly to layout debugging later: responsive rules (Day 13) and flex/grid (Days 14–16) frequently fail because a **more specific** selector from Day 05–10 still wins, or because `opacity` made hit-targets and text unintentionally faint.

---

## Day roadmap

1. [The cascade: importance, specificity, and source order](#the-cascade-importance-specificity-and-source-order)
2. [Inheritance, initial values, and `inherit` / `unset`](#inheritance-initial-values-and-inherit--unset)
3. [Specificity: how the browser “scores” selectors](#specificity-how-the-browser-scores-selectors)
4. [`!important`: escape hatch vs long-term debt](#important-escape-hatch-vs-long-term-debt)
5. [`opacity` vs `rgba()` / `hsla()` alpha](#opacity-vs-rgba--hsla-alpha)
6. [Custom properties (`--*`) as a cascade-aware tool](#custom-properties---as-a-cascade-aware-tool)
7. [Common mistakes & debugging](#common-mistakes--debugging)
8. [Further reading](#further-reading)
9. [Glossary](#glossary)
10. [Answers (self-test)](#answers-self-test)

---

## The cascade: importance, specificity, and source order

### What it is

The **cascade** is the algorithm that resolves conflicting declarations for the same element and same property. At a high level (author stylesheet world), compare candidates in this order:

1. **Origin and importance** (whether a declaration is `!important`, and where it came from).
2. **Specificity** (for normal declarations, higher specificity wins).
3. **Source order** (later wins if specificity ties).

Think of it like a **tie-break ladder**: you only go to the next rung if the current rung is tied.

#### Why it exists / why it matters

Without a deterministic cascade, stylesheets would be fragile: load order would randomly change appearance. The cascade lets you set **broad defaults** and **narrow overrides** predictably—*if* you understand specificity.

#### Pros and cons

- **Pros:** predictable resolution; supports progressive enhancement; enables design tokens via custom properties.
- **Cons:** mental overhead; “mystery overrides” when specificity is invisible in JSX/CSS modules; `@layer` adds another dimension in modern CSS.

#### What happens without it / when misused

- You add a class like `.active { color: red }` but an `#id` rule keeps winning—looks like “CSS is broken.”
- You import a component library and its selectors out-specificity your local utilities.

#### Syntax and rules

```css
/* Later file + later rule tends to win *when specificity ties* */
.card {
  color: #0f172a;
}

.card {
  color: #1e293b;
}
```

Gotchas:

- Inline styles (`style="..."`) generally beat stylesheet rules in specificity terms (except `!important` duels).
- Specificity is computed **per selector** in a comma-separated list, not “the whole rule.”

#### Examples

**Tiny — source order tie-break**

```css
p {
  margin: 0;
}
p {
  margin: 1rem; /* wins if specificity is equal */
}
```

**Tiny — specificity beats source order**

```css
p.note {
  color: #334155;
}

article p {
  color: #0f172a; /* loses to .class if both match the same <p class="note">… depends on DOM; example illustrates class vs 2 elements */
}
```

**Medium — realistic override stack**

```html
<section class="panel" id="billing">
  <p class="warn">Past due</p>
</section>
```

```css
#billing p {
  color: #b45309;
}
.panel p.warn {
  color: #c2410c;
}
```

Which wins depends on specificity counts—compute before guessing.

#### Quick checks

1. If two selectors have equal specificity, what breaks the tie?
2. Does the cascade compare selectors across *different properties*?
3. If a rule appears earlier in a file but has higher specificity, can a later, weaker rule override it?

---

## Inheritance, initial values, and `inherit` / `unset`

### What it is

**Inheritance** copies *computed values* from parent to child for selected properties. If a child does not specify `color`, it often inherits the parent’s computed `color`.

**Initial** values are spec-defined defaults for each property when nothing applies.

Keywords:

- `inherit` — force inheritance even for non-inherited properties.
- `initial` — use the property’s initial value.
- `unset` — acts like `inherit` if the property inherits, otherwise like `initial`.

#### Why it exists / why it matters

Inheritance lets you set typography once on `body` and have paragraphs match—without repeating `color` on every tag.

#### Pros and cons

- **Pros:** less repetition; consistent branding.
- **Cons:** “invisible” dependencies—moving DOM nodes changes inherited values; form controls have special default styling.

#### What happens without it / when misused

- You set `color` on a wrapper and wonder why `<input>` text color did not change the way you expected (UA styles + properties differ).
- You rely on inherited `font-size` for nested `em` sizing and get compounding surprises (review Day 06 units).

#### Syntax and rules

```css
body {
  color: #0f172a;
  font-family: system-ui, sans-serif;
}

.card {
  border: 1px solid #cbd5e1; /* not inherited */
}
```

#### Examples

**Tiny — explicit inherit**

```css
button.reset {
  font: inherit;
  color: inherit;
}
```

**Tiny — unset to wipe component-local oddities**

```css
.widget * {
  all: unset; /* powerful / dangerous; mostly demo-only */
}
```

**Medium — custom property inheritance bridge**

```css
:root {
  --accent: #2563eb;
}
.card {
  --accent: #7c3aed; /* descendants inherit the *value* at cascade time */
  border-color: var(--accent);
}
```

#### Quick checks

1. Is `border-width` inherited by default?
2. Does `inherit` on `border-color` pull the parent’s border color even if border is not normally inherited?
3. Why can nested `em` font sizes compound even when `font-size` “looks inherited”?

---

## Specificity: how the browser “scores” selectors

### What it is

**Specificity** is a scoring system for selectors. The classic model (simplified) counts:

- **IDs** (`#app`)
- **Classes, attributes, pseudo-classes** (`.btn`, `[type="email"]`, `:hover`)
- **Types and pseudo-elements** (`div`, `::before`)

Inline styles and `!important` live outside this simple triple, but for stylesheet rules the triple dominates debugging.

Mental model: compare as **tuple** lexicographically: bigger in the first column wins; if tied, compare second; then third.

#### Why it exists / why it matters

Specificity prevents “random last rule” while still allowing broad-to-narrow styling.

#### Pros and cons

- **Pros:** stable; explainable in code review.
- **Cons:** easy to escalate (`#id` arms race); utility frameworks sometimes hide complexity.

#### What happens without it / when misused

- You ship a design system utility `.mt-4` but an old `#sidebar .mt-4` never loses—utility “does not work.”

#### Syntax and rules

```css
/* 1 id, 0 classes, 1 type => (1,0,1) simplified view */
#app header {
  padding: 1rem;
}

/* 0 ids, 2 classes, 1 type */
header.site-nav.sticky {
  padding: 0.75rem;
}
```

Gotchas:

- `:where()` contributes **0 specificity** (modern reset trick).
- `:not()`’s specificity is the **most specific** of its arguments (modern CSS).

#### Examples

**Tiny — attribute selector counts like a class**

```css
input[type="checkbox"] {
  accent-color: #2563eb;
}
```

**Tiny — pseudo-class counts like a class**

```css
a:visited {
  color: #64748b;
}
```

**Medium — why “more selectors” is not always “more specific”**

```css
div div div p {
  color: #111827; /* many types, still weak vs one class */
}
.lede {
  color: #0f172a;
}
```

#### Quick checks

1. Which is typically stronger: one class or three element selectors?
2. Does `::before` count like a pseudo-element in the third column?
3. Why is `:where(.btn)` weaker than `.btn`?

---

## `!important`: escape hatch vs long-term debt

### What it is

Appending `!important` to a declaration raises it into a high-priority bucket within its origin. Duels become “`!important` vs `!important`,” then specificity still matters, then source order.

#### Why it exists / why it matters

User stylesheets and accessibility tooling sometimes need to win. In app CSS, it is mostly an emergency override.

#### Pros and cons

- **Pros:** can unblock urgent production hotfixes.
- **Cons:** creates arms races; breaks component encapsulation expectations; makes DevTools “winning rule” harder to reason about.

#### What happens without it / when misused

- Two libraries both use `!important` on `display`, and your layout becomes non-composable.

#### Syntax and rules

```css
.hidden {
  display: none !important;
}
```

Prefer: fix specificity, use layers (`@layer`), split stylesheets, or refactor selector coupling.

#### Examples

**Tiny — legitimate utility**

```css
.sr-only {
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  overflow: hidden !important;
}
```

**Medium — debt pattern (avoid)**

```css
.card .title {
  color: #0f172a !important;
}
#legacy-app .card .title {
  color: #334155 !important;
}
```

#### Quick checks

1. If both sides use `!important`, what breaks the tie?
2. Why does adding `!important` to a fix often force more `!important` later?
3. Name one safer alternative for most app CSS conflicts.

---

## `opacity` vs `rgba()` / `hsla()` alpha

### What it is

- **`opacity`** sets transparency for the **entire element subtree as a group** (including text and descendants), and also affects stacking/hit testing in nuanced ways.
- **`rgba()`/`hsla()`** alpha typically affects **one painted layer** (commonly background) without forcing the entire subtree to become a single transparency group.

#### Why it exists / why it matters

Overlays, disabled states, and glassmorphism need predictable transparency. The wrong tool creates unreadable text and “ghost clicks.”

#### Pros and cons

- **Pros (`opacity`):** simple API; animatable; consistent fade for complex subtree UIs.
- **Cons (`opacity`):** multiplies down the tree; can make text illegible; can interact with stacking contexts unexpectedly.
- **Pros (alpha colors):** local effect; better for tinted backgrounds without fading text.
- **Cons (alpha colors):** blending math is still easy to get wrong when stacking multiple translucent layers.

#### What happens without it / when misused

- Parent `opacity: 0.5` + child `opacity: 0.5` does **not** “add back” clarity; effective child appearance is weaker than expected.
- You animate `width` + `opacity` together and jank appears—often prefer `transform` (Day 15).

#### Syntax and rules

```css
.fade-group {
  opacity: 0.85;
}

.tint {
  background-color: rgb(37 99 235 / 0.15);
}
```

#### Examples

**Tiny — readable disabled button (prefer alpha background)**

```css
button[disabled] {
  background-color: rgb(148 163 184 / 0.35);
  color: #0f172a;
}
```

**Tiny — fade a whole card including text**

```css
.card.is-busy {
  opacity: 0.55;
}
```

**Medium — stacked translucent panels**

```html
<section class="stack">
  <div class="panel a"></div>
  <div class="panel b"></div>
</section>
```

```css
.stack {
  position: relative;
}
.panel {
  position: absolute;
  inset: 0;
}
.panel.a {
  background: rgb(59 130 246 / 0.35);
}
.panel.b {
  background: rgb(244 63 94 / 0.25);
}
```

#### Quick checks

1. If a parent has `opacity: 0.4` and a child sets `opacity: 1`, can the child appear fully opaque relative to the page background?
2. Which approach is usually better for “dim the background behind a modal” without fading modal text?
3. Name one accessibility risk of lowering `opacity` on interactive controls.

---

## Custom properties (`--*`) as a cascade-aware tool

### What it is

Custom properties (“CSS variables”) are **inherited** by default and participate in the cascade like normal properties, but their substitution via `var()` happens at computed-value time in ways that enable theming.

#### Why it exists / why it matters

They reduce duplication and let you propagate tokens down a subtree—while still allowing local overrides.

#### Pros and cons

- **Pros:** great for themes; avoids selector wars for repeated values.
- **Cons:** invalid at computed-value time can invalidate whole declarations; easy to typo `--`.

#### What happens without it / when misused

- You set `--gap: 12px` only on desktop media query and forget a base value—layout collapses on mobile.

#### Syntax and rules

```css
:root {
  --space-3: 0.75rem;
}
.grid {
  gap: var(--space-3);
}
```

#### Examples

**Tiny — fallback**

```css
.card {
  padding: var(--card-pad, 1rem);
}
```

**Medium — component-scoped token**

```css
.alert--warn {
  --accent: #f59e0b;
  border-left: 4px solid var(--accent);
}
```

#### Quick checks

1. Are custom properties inherited by default?
2. What happens if `var(--missing)` has no fallback and `--missing` is undefined?
3. Why are custom properties useful when specificity is tight?

---

## Common mistakes & debugging

- **Mystery color** inherited from `body` via a long chain—use DevTools “Computed” and click through to the winning declaration.
- **Specificity escalation** with `#ids` to beat a library—prefer structure + layers + refactoring.
- **Opacity on parent** makes all children faint—use alpha backgrounds instead.
- **Assuming `!important` ends debates**—it often relocates the debate into harder-to-debug places.
- **Forgetting pseudo-class specificity**—`:focus-visible` matters for accessible focus rings (Day 10).

**Debugging workflow:** Inspect element → **Computed** tab → trace active property → note **which selector** won → check specificity tuple → check for `!important` → check inheritance chain for custom properties.

---

## Further reading

- MDN: [Cascade](https://developer.mozilla.org/en-US/docs/Web/CSS/Cascade)
- MDN: [Specificity](https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity)
- MDN: [inheritance](https://developer.mozilla.org/en-US/docs/Web/CSS/inheritance)
- MDN: [`opacity`](https://developer.mozilla.org/en-US/docs/Web/CSS/opacity)
- MDN: [Using CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- W3C CSS Cascade spec (advanced): search “CSS Cascading and Inheritance Level 5” for `@layer` details.

---

## Glossary

| Term | Meaning |
|------|---------|
| Cascade | Conflict resolution algorithm for competing declarations |
| Specificity | Score tuple used to compare selector strength |
| Inherited property | Property whose computed value can propagate to descendants if unset |
| Initial value | Spec default when no declaration applies |
| `!important` | Boosts declaration priority within an origin |
| Alpha | Transparency channel in colors (`/ 0.5` modern syntax) |
| Stacking context | Painted layer grouping influenced by `opacity`, `transform`, `z-index`, etc. |

---

## Answers (self-test)

### The cascade

1. **Source order** (later wins) when specificity and importance buckets tie (within the same layer/origin context).
2. No—cascade resolves **per property** independently.
3. Yes—higher specificity beats later weaker rules.

### Inheritance

1. No—`border-width` is not inherited by default.
2. Yes—`inherit` forces the parent computed value for that property.
3. `em` resolves against inherited `font-size`; nested `em` compounds because each level’s computed font-size becomes the context for the next.

### Specificity

1. One class generally beats three type selectors (class column beats type column).
2. Yes—pseudo-elements count in the “element/pseudo-element” bucket in the classic model.
3. `:where()` contributes zero specificity; `:where(.btn)` is weaker than `.btn`.

### `!important`

1. Specificity still applies among `!important` rules in the same layer/origin; then source order.
2. Competitors respond with more `!important`, raising cleanup cost.
3. Refactor selectors, adopt `@layer`, reduce `#id` coupling, or split concerns into components.

### Opacity vs alpha

1. No—child `opacity` is multiplied by ancestors; you cannot “cancel” parent group opacity with `opacity: 1` on the child relative to the page.
2. Often `rgba()`/`hsla()` on overlays + normal text opacity, or layered backgrounds (Day 15 transitions help).
3. Text/contrast can fall below WCAG thresholds; controls can look disabled when they are not.

### Custom properties

1. Yes—inherited by default (unless you use `@property` advanced cases outside today’s scope).
2. The declaration using `var()` may become invalid at computed time.
3. You can override a token with a simple rule even when selectors are hard to change—tokens cascade independently of unrelated specificity battles *when used as values* (still normal cascade for the `--x` declaration itself).
