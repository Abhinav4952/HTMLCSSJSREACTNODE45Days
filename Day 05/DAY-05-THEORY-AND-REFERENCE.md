# Day 05 — CSS Selectors & Decoration

**Primary theme:** Selector fluency plus decorative borders/backgrounds and typographic emphasis via CSS  
**Estimated study time:** 1–2 hours theory + 3–6 hours tasks  
**Related tasks:** `task-01-selector-practice-board`, `task-02-borders-backgrounds-cards`, `task-03-text-decoration-transform-banner`, `task-04-product-card-gallery`  
**Instruction alignment:** Maps to *CSS rules and selectors* and *CSS decoration: border, background, text-decoration, text-transform*.

---

## Overview

CSS is two skills at once: **selecting the right nodes** and **assigning the right properties**. Today you will practice combinators that mirror HTML structure (child vs descendant) and decoration properties that establish affordance: cards look clickable, banners look promotional, and uppercase labels read as **labels**, not shouting body text—`text-transform` should pair with letter-spacing cautiously.

---

## Day roadmap

1. [Simple selectors: type, class, id](#simple-selectors-type-class-id)
2. [Combinators: descendant, child, adjacent sibling](#combinators-descendant-child-adjacent-sibling)
3. [Borders, radii, and backgrounds](#borders-radii-and-backgrounds)
4. [`text-decoration` and `text-transform`](#text-decoration-and-text-transform)
5. [Common mistakes & debugging](#common-mistakes--debugging)
6. [Further reading](#further-reading)
7. [Glossary](#glossary)
8. [Answers (self-test)](#answers-self-test)

---

## Simple selectors: type, class, id

### What it is

- **Type:** `p { }` selects all paragraphs.
- **Class:** `.badge { }` selects elements with `class="badge"` (multiple classes space-separated).
- **ID:** `#app { }` selects the unique element with that `id` (unique per document).

#### Why it exists / why it matters

Low-specificity selectors (type/class) scale better than `#`-heavy stylesheets. IDs are still invaluable for **in-page anchors** and `label for` wiring.

#### Pros and cons

- **Pros:** Classes compose; utilities in later frameworks build on this idea.
- **Cons:** Overly generic type selectors (`div { }`) cause unintended cascade hits.
- **Cons:** IDs have high specificity—harder to override later.

#### What happens without it / when misused

- `#header` repeated twice in one document is invalid HTML and brittle for styling.

#### Syntax and rules

```css
button.primary { }
#modal-host { }
```

#### Examples

**Tiny**

```css
a {
  color: #0369a1;
}
```

**Tiny**

```css
.tag {
  display: inline-block;
  padding: 0.1rem 0.4rem;
  border-radius: 999px;
}
```

**Medium**

```css
article.lede > p:first-of-type {
  font-size: 1.125rem;
}
```

#### Quick checks

1. Which selector tends to have the highest specificity among type/class/id?
2. Can one element carry multiple classes?
3. When is an ID attribute required beyond styling?

---

## Combinators: descendant, child, adjacent sibling

### What it is

- **Descendant (`A B`):** `B` anywhere inside `A`.
- **Child (`A > B`):** `B` direct child of `A` only.
- **Adjacent sibling (`A + B`):** `B` immediately follows `A` sharing the same parent.

#### Why it exists / why it matters

Child combinators avoid “leaky” rules that recolor nested links inside callouts. Adjacent sibling patterns power **label + error** dyads.

#### Pros and cons

- **Pros:** Mirrors DOM structure; fewer classes sometimes.
- **Cons:** Brittle if markup refactors change nesting.

#### What happens without it / when misused

- `nav a` styles every link in nested mega-menus when you only wanted top-level—tighten with `>`.

#### Syntax and rules

```css
nav > a { }
h2 + p { }
.card .title { }
```

#### Examples

**Tiny — child**

```css
ul.checklist > li {
  list-style: square;
}
```

**Tiny — adjacent**

```css
input:invalid + .error {
  color: #b91c1c;
}
```

**Medium**

```css
section.pricing .tier.featured {
  border-color: #0ea5e9;
}
```

#### Quick checks

1. Difference between `.card .title` and `.card > .title`?
2. Does `h2 + p` match a paragraph separated from `h2` by a `<div>`?
3. Name a good use for `+` in forms.

---

## Borders, radii, and backgrounds

### What it is

`border`, `border-radius`, `background-color`, and layered `background` shorthand including gradients.

#### Why it exists / why it matters

Borders communicate boundaries; radius communicates “soft” UI vs sharp tools; backgrounds set grouping and mood.

#### Pros and cons

- **Pros:** Cheap performance vs images for simple cards.
- **Cons:** Too many box shadows + borders can look noisy.

#### What happens without it / when misused

- `outline: none` on focusable elements without replacement harms keyboard users—do not remove outlines in these tasks.

#### Syntax and rules

```css
.card {
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  background-color: #ffffff;
}
```

#### Examples

**Tiny**

```css
hr.section {
  border: 0;
  border-top: 1px dashed #cbd5e1;
}
```

**Tiny**

```css
.panel {
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
}
```

**Medium**

```css
.pill {
  border-radius: 999px;
  padding: 0.25rem 0.75rem;
  border: 1px solid #94a3b8;
}
```

#### Quick checks

1. Property to round corners?
2. How to get only a top border without drawing other sides explicitly as solid lines?
3. Why avoid removing `:focus` outlines in homework unless you replace them?

---

## `text-decoration` and `text-transform`

### What it is

`text-decoration-line/color/thickness` (shorthand `text-decoration`) underlines, overlines, line-through. `text-transform: uppercase` changes **rendered** case; underlying DOM text remains mixed case if typed that way.

#### Why it exists / why it matters

Uppercase microcopy with increased `letter-spacing` is a common “label” look. Underlines on links are a default affordance—changing link styles should preserve discoverability.

#### Pros and cons

- **Pros:** Quick typographic hierarchy without changing content strings.
- **Cons:** ALL CAPS BODY TEXT HURTS READABILITY.
- **Cons:** `line-through` can be mistaken for disabled content—use sparingly.

#### What happens without it / when misused

- Removing underline from links without another cue confuses users.

#### Syntax and rules

```css
.muted-link {
  text-decoration: underline dotted;
}
.kicker {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.75rem;
}
```

#### Examples

**Tiny**

```css
abbr {
  text-decoration: underline dotted;
}
```

**Tiny**

```css
h1 {
  text-transform: none;
}
```

**Medium**

```css
nav a {
  text-decoration: none;
  border-bottom: 2px solid transparent;
}
nav a:hover,
nav a:focus-visible {
  border-color: currentColor;
}
```

#### Quick checks

1. Does `text-transform` change the submitted value of an `<input>`?
2. Name an accessible alternative to underline removal for links.
3. Which decoration often signals deleted pricing?

---

## Common mistakes & debugging

- **Specificity wars:** prefer adding a class over chaining long selectors.
- **Collapsed margins:** adjacent vertical margins of siblings can collapse—Day 07 deepens this.
- **Contrast:** light gray uppercase labels—verify contrast ratio.

---

## Further reading

- [MDN — CSS selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)
- [MDN — border](https://developer.mozilla.org/en-US/docs/Web/CSS/border)
- [MDN — text-decoration](https://developer.mozilla.org/en-US/docs/Web/CSS/text-decoration)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Combinator** | Symbol combining simple selectors (`>`, `+`, ` `). |
| **Specificity** | Algorithm ranking which rule wins on conflicts (preview; Day 11 deepens). |

---

## Answers (self-test)

**Simple selectors**

1. ID selectors beat classes and types in the cascade specificity calculation (simplified answer).
2. Yes (`class="btn primary"`).
3. Accessible name targets for `label for`, in-page anchors, ARIA references.

**Combinators**

1. Descendant vs direct child only.
2. No—`+` requires immediate adjacency for element nodes (text nodes can interfere in some edge cases; default answer: no).
3. Error message immediately after an invalid field.

**Borders/backgrounds**

1. `border-radius`.
2. `border-top: 1px solid ...` with other borders zero/none, or `border` shorthand variants.
3. Keyboard users lose visible focus—illegal for accessibility in most product contexts.

**Text**

1. No—mostly visual; still be careful with copy/paste expectations.
2. Provide another distinct visual cue (`border-bottom`, `background`, `outline` on `:focus-visible`).
3. `line-through` often used for old prices.
