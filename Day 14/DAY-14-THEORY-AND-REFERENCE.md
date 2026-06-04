# Day 14 — Flexbox Layout

**Primary theme:** One-dimensional layout with explicit axis control, wrapping, flexing metrics, and flex-item overflow discipline (`min-width: 0`)  
**Estimated study time:** 2–3 hours theory + 4–7 hours tasks  
**Related tasks:** `task-01-flex-direction-alignment-playground`, `task-02-flex-wrap-order-toolbar`, `task-03-flex-metrics-dashboard-layout`, `task-04-flex-min-width-zero-sidebar`  
**Instruction alignment:** Maps to *Flexible Box Model (Flexbox)* and connects to *responsive design* (Day 13) + *box model* (Day 07).

---

## Overview

Flexbox solves a different problem than “randomly centering things.” It lays out items along a **main axis** (row or column) while distributing leftover space and aligning items on the **cross axis**. When you internalize axes, APIs like `justify-content` stop feeling like magic incantations and start feeling like **geometry**.

Dashboards stretch and shrink: `flex-grow` eats extra space, `flex-shrink` surrenders space under pressure, and `flex-basis` sets the negotiation starting point. The classic footgun is text truncation: flex items default to `min-width: auto`, which can refuse to shrink below content min-content width—leading to overflow. **`min-width: 0`** (or `overflow: hidden` in careful cases) restores predictable shrinking.

---

## Day roadmap

1. [Flex containers and items: `display: flex`](#flex-containers-and-items-display-flex)
2. [Main axis vs cross axis + `flex-direction`](#main-axis-vs-cross-axis--flex-direction)
3. [Distribution: `justify-content`, `align-items`, `gap`](#distribution-justify-content-align-items-gap)
4. [Wrapping + ordering: `flex-wrap`, `order`](#wrapping--ordering-flex-wrap-order)
5. [Growing/shrinking: `flex-grow`, `flex-shrink`, `flex-basis`, `flex`](#growingshrinking-flex-grow-flex-shrink-flex-basis-flex)
6. [The `min-width: auto` footgun + `min-width: 0`](#the-min-width-auto-footgun--min-width-0)
7. [Common mistakes & debugging](#common-mistakes--debugging)
8. [Further reading](#further-reading)
9. [Glossary](#glossary)
10. [Answers (self-test)](#answers-self-test)

---

## Flex containers and items: `display: flex`

### What it is

A **flex container** is an element with `display: flex` (or `inline-flex`). Its in-flow children become **flex items** arranged according to flex rules.

#### Why it exists / why it matters

Flexbox is the default tool for toolbars, split panes, centering unknown heights, and many “component-scale” layouts.

#### Pros and cons

- **Pros:** powerful alignment; handles unknown content sizes well.
- **Cons:** one-dimensional—complex 2D macro layouts may want Grid (later courses).

#### What happens without it / when misused

- People nest many flex containers unnecessarily, making debugging harder.

#### Syntax and rules

```css
.row {
  display: flex;
  gap: 0.75rem;
}
```

#### Examples

**Tiny — inline-flex chip row**

```css
.chips {
  display: inline-flex;
  gap: 0.35rem;
}
```

#### Quick checks

1. Does `inline-flex` create a block-level box or inline-level box?
2. What is a flex item?

---

## Main axis vs cross axis + `flex-direction`

### What it is

- Default `flex-direction: row` → main axis is horizontal (in LTR), cross axis vertical.
- `flex-direction: column` flips them.

#### Why it exists / why it matters

Most “why doesn’t `justify-content` vertical center???” bugs are axis confusion.

#### Pros and cons

- **Pros:** easy vertical centering in a full-height column flex.
- **Cons:** `column` + tall content can create surprising scroll areas if `min-height` not handled.

#### Syntax and rules

```css
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
```

#### Quick checks

1. In a row flex, does `justify-content` affect horizontal or vertical distribution (LTR)?
2. What does `row-reverse` change besides visual order?

---

## Distribution: `justify-content`, `align-items`, `gap`

### What it is

- `justify-content` distributes items along the **main axis**.
- `align-items` aligns items along the **cross axis** (in the cross direction within each line).
- `gap` separates items without margin hacks.

#### Why it exists / why it matters

These properties encode common UX patterns: space-between headers, centered heroes, evenly spaced toolbars.

#### Syntax and rules

```css
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}
```

#### Quick checks

1. What is the difference between `align-items` and `align-self`?
2. Why prefer `gap` over adding right-margins to every item except last?

---

## Wrapping + ordering: `flex-wrap`, `order`

### What it is

`flex-wrap: wrap` allows additional flex lines when items exceed the container’s main size. `order` changes **painting/source order** within flex sorting (accessibility caution).

#### Why it exists / why it matters

Responsive toolbars often wrap instead of shrinking unreadably.

#### What happens without it / when misused

- Reordering only visually can confuse keyboard users if focus order does not match reading order—use sparingly.

#### Syntax and rules

```css
.toolbar {
  flex-wrap: wrap;
}
```

#### Quick checks

1. Does `order` change tab order?
2. When is wrapping preferable to horizontal scroll?

---

## Growing/shrinking: `flex-grow`, `flex-shrink`, `flex-basis`, `flex`

### What it is

- `flex-grow` — how eagerly an item consumes free space on the main axis.
- `flex-shrink` — how willingly it surrenders space under pressure.
- `flex-basis` — starting size before distributing free space (`auto`, `0`, lengths).

#### Syntax and rules

```css
.sidebar {
  flex: 0 0 260px;
}

.main {
  flex: 1 1 auto;
}
```

#### Quick checks

1. What does `flex: 1` commonly expand to in longhand?
2. Why is `flex-basis: 0` sometimes used with `flex-grow` patterns?

---

## The `min-width: auto` footgun + `min-width: 0`

### What it is

Flex items default to `min-width: auto`, meaning they won’t shrink below their content’s minimum intrinsic width (long words, preformatted text, wide tables).

#### Why it exists / why it matters

This is the #1 “flex overflow” bug in dashboards.

#### Syntax and rules

```css
.panel {
  min-width: 0;
}
```

#### Quick checks

1. Name one symptom that `min-width: 0` fixes in a flex row layout.
2. What are risks of pairing `min-width: 0` with zero shrink (`flex-shrink: 0`)?

---

## Common mistakes & debugging

- Using `justify-content` for cross-axis centering in a row flex (often need `align-items`).
- Expecting `align-items: stretch` to stretch wrapped lines the way Grid does—flex lines differ.
- Long unbroken strings overflow—add `overflow-wrap: anywhere` where appropriate.

---

## Further reading

- MDN: [Basic concepts of flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox)
- MDN: [`flex`](https://developer.mozilla.org/en-US/docs/Web/CSS/flex)
- MDN: [min-width](https://developer.mozilla.org/en-US/docs/Web/CSS/min-width)

---

## Glossary

| Term | Meaning |
|------|---------|
| Main axis | Primary flex layout axis |
| Cross axis | Perpendicular axis |
| Flex item | Child participating in flex layout |
| `gap` | Spacing between items/lines |

---

## Answers (self-test)

### Flex container

1. `inline-flex` makes an **inline-level** flex container.
2. A child in-flow box participating in flex layout for that container.

### Axes

1. Horizontal in LTR row flex.
2. Reverses main-start/main-end; can affect scroll anchoring and reading order—use carefully.

### Distribution

1. `align-self` overrides `align-items` for a single item.
2. `gap` avoids “last item margin” bugs and is symmetric.

### Wrap/order

1. `order` does not change DOM/tab order by itself; focus order follows DOM—visual reorder can mismatch.
2. When items would become unusably narrow or when wrapping improves scanability.

### Flex metrics

1. Typically `flex: 1 1 0%` vs `1 1 auto` depends on author intent—many styleguides treat `flex: 1` as `1 1 0%` or `1 1 auto`—know your codebase.
2. `flex-basis: 0` makes free-space distribution more “purely grow-based” in some patterns.

### `min-width`

1. Prevents flex item from shrinking below content min width; causes overflow in split layouts.
2. Can hide overflow if paired with overflow clipping—watch accessibility.
