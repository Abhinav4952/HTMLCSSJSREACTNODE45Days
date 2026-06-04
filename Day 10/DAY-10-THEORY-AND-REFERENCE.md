# Day 10 — Pseudo-classes & Pseudo-elements

**Primary theme:** Selecting by structure and decorating with generated content—without breaking accessibility or maintainability  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Related tasks:** `task-01-nth-child-vs-nth-of-type-trap`, `task-02-pseudo-element-icons-and-a11y`, `task-03-focus-visible-ring-customization`, `task-04-css-counters-outline-nav`  
**Instruction alignment:** Maps to *Pseudo-classes*, *Pseudo-elements*, and *`:focus-visible`*; introduces **CSS counters** lightly.

---

## Overview

Pseudo-classes and pseudo-elements look like tiny syntax sugar (`:hover`, `::before`), but they change **what you can express without JavaScript** and how tightly your CSS couples to HTML structure. `:nth-child(3n+1)` can be elegant—or it can become a landmine the moment someone inserts a wrapper `<div>` for layout.

This day separates two different skills:

1. **Selecting safely:** prefer `:nth-of-type` when you mean “every third paragraph,” and reserve `:nth-child` for cases where the child index truly matches your intent across mixed element types.
2. **Decorating responsibly:** `::before` can add icons, counters, and separators—but critical text should remain in the DOM for screen readers and search engines unless you fully understand the accessibility tradeoffs (and often even then, don’t).

---

## Day roadmap

1. [Pseudo-classes vs pseudo-elements (syntax + mental model)](#pseudo-classes-vs-pseudo-elements-syntax--mental-model)
2. [Structural pseudo-classes: `:first-child`, `:last-child`, `:nth-child()`](#structural-pseudo-classes-first-child-last-child-nth-child)
3. [`:nth-child()` vs `:nth-of-type()` (the trap)](#nth-child-vs-nth-of-type-the-trap)
4. [`:focus`, `:focus-within`, and `:focus-visible` (keyboard vs mouse)](#focus-focus-within-and-focus-visible-keyboard-vs-mouse)
5. [Pseudo-elements `::before` / `::after`: `content`, icons, and gotchas](#pseudo-elements-before--after-content-icons-and-gotchas)
6. [CSS counters: `counter-reset`, `counter-increment`, `counters()`](#css-counters-counter-reset-counter-increment-counters)
7. [Deep dive — generated content and the accessibility tree (honest boundaries)](#deep-dive--generated-content-and-the-accessibility-tree-honest-boundaries)
8. [Common mistakes & debugging](#common-mistakes--debugging)
9. [Further reading](#further-reading)
10. [Glossary](#glossary)
11. [Answers (self-test)](#answers-self-test)

---

## Pseudo-classes vs pseudo-elements (syntax + mental model)

### What it is

- **Pseudo-class** selects an element in a particular state or structural relation: `:hover`, `:focus-visible`, `:nth-child(2)`.
- **Pseudo-element** targets a sub-part of an element’s generated boxes: `::before`, `::after`, `::first-line`.

CSS3 syntax uses **double colon** for pseudo-elements (`::before`) to disambiguate; browsers often accept single colon for legacy reasons—prefer `::` in new stylesheets.

#### Why it exists / why it matters

Pseudo-classes reduce JS for simple interactions; pseudo-elements reduce DOM nodes for decoration.

#### Pros and cons

- **Pros:** fewer nodes; expressive styling.
- **Cons:** overuse makes CSS hard to refactor; structural selectors break when DOM changes.

#### Examples

```css
a:hover {
  text-decoration: underline;
}
```

```css
.note::before {
  content: "→ ";
}
```

#### Quick checks

1. Which one represents state: pseudo-class or pseudo-element?
2. Why prefer `::before` over `:before` in new code?

---

## Structural pseudo-classes: `:first-child`, `:last-child`, `:nth-child()`

### What it is

`:first-child` matches if the element is the **first child among all node types** (element siblings; text nodes don’t count as element siblings but whitespace text nodes can still affect “first child” surprises in XML serialization—HTML usually coalesces).

`:nth-child(an+b)` selects among all children with index formula.

#### Why it exists / why it matters

Lets you style table stripes, zebra lists, and repeating patterns without classes.

#### Examples

```css
tr:nth-child(even) td {
  background: #f8fafc;
}
```

#### Quick checks

1. Does `:nth-child` care about element tag names?

---

## `:nth-child()` vs `:nth-of-type()` (the trap)

### What it is

- `:nth-child(n)` filters by **index among all element children** (and checks element type matches selector before/after? Actually `:p:nth-child(2)` means: p is 2nd child overall AND is a p).
- `:nth-of-type(n)` filters by **index among siblings of that tag name**.

#### Why it exists / why it matters

Mixed DOM (sections, divs, paragraphs) makes `:nth-child` patterns explode.

#### Examples

```html
<section>
  <h2>Title</h2>
  <p>A</p>
  <p>B</p>
</section>
```

- `p:nth-child(2)` matches nothing (2nd child is not `p`).
- `p:nth-of-type(1)` matches `A`.

#### Quick checks

1. In the snippet above, does `p:nth-child(3)` match `B`?

---

## `:focus`, `:focus-within`, and `:focus-visible` (keyboard vs mouse)

### What it is

- `:focus` applies whenever focused.
- `:focus-within` matches if the element or a descendant is focused—great for highlighting containers.
- `:focus-visible` lets browsers heuristically show focus rings for keyboard users while reducing mouse-click ring noise (heuristics vary slightly by browser).

#### Why it exists / why it matters

Visible focus is a WCAG requirement; `:focus-visible` improves perceived polish.

#### Examples

```css
.btn:focus-visible {
  outline: 3px solid #0ea5e9;
  outline-offset: 2px;
}
```

#### Quick checks

1. When is `:focus-within` better than `:focus` for a `.field` wrapper?

---

## Pseudo-elements `::before` / `::after`: `content`, icons, and gotchas

### What it is

`::before`/`::after` generate boxes that are children of the element for formatting purposes; they require `content` (can be empty string for layout hacks).

#### Gotchas

- Generated content may not be copied by default in some clipboard operations.
- Icons as backgrounds lack easy recolor unless masks/SVG used.

#### Examples

```css
.external::after {
  content: " ↗";
  font-weight: 700;
}
```

---

## CSS counters: `counter-reset`, `counter-increment`, `counters()`

### What it is

Counters let you number headings or nav items with CSS.

```css
body {
  counter-reset: section;
}
h2 {
  counter-increment: section;
}
h2::before {
  content: counter(section) ". ";
}
```

---

## Deep dive — generated content and the accessibility tree (honest boundaries)

### What it is

Generated text can become accessible in some cases, but **do not** rely on `::before` for essential instructional text. Put instructional text in real DOM nodes.

### Why it matters

Course projects get audited; examiners flag “icon-only meaning.”

---

## Deep dive — three `:nth-child` riddles (worked)

### Riddle 1 — “Stripe only data rows”

If your table has `<thead>` and `<tbody>`, `tr:nth-child(even)` may count the header row depending on structure. Prefer:

- `tbody tr:nth-of-type(even)` (still depends on row types), or
- explicit classes, or
- `tbody tr:nth-child(even)` **only** if `<thead>` rows are not siblings in the same parent (they usually are siblings of `tbody`, not inside it—good), but if you incorrectly nest, you break patterns.

### Riddle 2 — “Every third card”

`.grid > *:nth-child(3n)` works only if **only cards** are direct children.

### Riddle 3 — “First paragraph after each h2”

Often easier with `:nth-of-type` on `p` combined with sibling patterns, or with `:has()` (supported in modern browsers) — optional advanced reading.

---

## Common mistakes & debugging

- Using `:nth-child` on tables with mixed `thead/tbody` rows without accounting for header rows.
- `content` missing → pseudo-element doesn’t show.
- Removing outlines without `:focus-visible` replacement.

---

## Further reading

- [MDN — Pseudo-classes](https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-classes)
- [MDN — Pseudo-elements](https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-elements)
- [MDN — :focus-visible](https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible)
- [MDN — Using CSS counters](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_counter_styles/Using_CSS_counters)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Generated content** | Text/icons inserted via `content` on `::before/::after`. |

---

## Answers (self-test)

**Pseudo basics**

1. Pseudo-class.
2. Double colon disambiguates pseudo-elements in CSS3+ style; clearer reading.

**nth**

1. `:nth-child` counts among element children regardless of tag (subject to full selector matching rules).

**trap snippet**

1. Yes: `p` is 3rd child overall (`h2`, `p A`, `p B`), so `p:nth-child(3)` matches `B`.

**focus**

1. When you want the whole field container highlighted while an inner input is focused.

**counters**

1. `counter-reset` establishes namespace; `counter-increment` bumps; `content: counter()` prints.
