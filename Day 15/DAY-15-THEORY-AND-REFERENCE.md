# Day 15 — Advanced Selectors, Transitions, and Motion

**Primary theme:** Attribute-driven styling, GPU-friendly motion (`transform`/`opacity`), keyframed animation, and user motion preferences (`prefers-reduced-motion`)  
**Estimated study time:** 2–4 hours theory + 4–7 hours tasks  
**Related tasks:** `task-01-attribute-selectors-file-picker`, `task-02-transition-transform-vs-layout`, `task-03-keyframes-respecting-prefers-reduced-motion`, `task-04-resize-custom-property-panel`  
**Instruction alignment:** Maps to *Attribute selectors*, *CSS transform/transition/animation*, and *resize where useful* from the master topic list.

---

## Overview

Modern UI motion is a performance and accessibility problem disguised as “polish.” **`width`, `height`, `top`, `left`**, and **layout-affecting margins** frequently trigger reflow when transitioned—fine for tiny demos, painful for real pages. In contrast, **`transform` and `opacity`** often compose well with the compositor (still not “free,” but generally the right default for micro-interactions).

Selectors evolve too: attribute selectors let you style `input[type="search"]`, `a[href^="https"]`, and `button[data-variant="danger"]` without inventing a class for every state.

This day also introduces **motion safety**: many users enable “Reduce motion” OS settings. Responsible CSS uses `@media (prefers-reduced-motion: reduce)` to replace flashy loops with instant state changes or subtle fades.

---

## Day roadmap

1. [Attribute selectors: substring matching and case sensitivity](#attribute-selectors-substring-matching-and-case-sensitivity)
2. [`transform` vs layout properties](#transform-vs-layout-properties)
3. [`transition`: what can be interpolated smoothly](#transition-what-can-be-interpolated-smoothly)
4. [`@keyframes` + `animation` shorthand](#keyframes--animation-shorthand)
5. [`prefers-reduced-motion`](#prefers-reduced-motion)
6. [`resize` and overflow discipline](#resize-and-overflow-discipline)
7. [Common mistakes & debugging](#common-mistakes--debugging)
8. [Further reading](#further-reading)
9. [Glossary](#glossary)
10. [Answers (self-test)](#answers-self-test)

---

## Attribute selectors: substring matching and case sensitivity

### What it is

Attribute selectors match elements based on attribute presence/value:

- `[attr]` exists
- `[attr="value"]` exact
- `[attr^="pre"]` starts with
- `[attr$="suf"]` ends with
- `[attr*="mid"]` contains substring

#### Why it exists / why it matters

They reduce classitis for variants that already exist in markup (`type`, `href`, `data-*`).

#### Pros and cons

- **Pros:** styles track semantics encoded in attributes.
- **Cons:** can become brittle if attributes rename; specificity still applies.

#### What happens without it / when misused

- `[href*="login"]` accidentally matches unintended URLs.

#### Syntax and rules

```css
a[href^="https://"] {
  color: #16a34a;
}

input[type="search"] {
  border-radius: 999px;
}
```

Modern CSS supports **case-insensitive** attribute matching with an `i` flag in some contexts—verify browser targets before relying on it.

#### Quick checks

1. Which selector matches any `href` ending with `.pdf`?
2. Why should attribute selectors on `href` be careful with query strings?

---

## `transform` vs layout properties

### What it is

`transform` applies a geometric operation in **local coordinates** (translate/scale/rotate/skew) without changing layout flow the same way `top/left` does for in-flow elements.

#### Why it exists / why it matters

Micro-interactions (press, lift, slide) are smoother when they avoid layout.

#### Pros and cons

- **Pros:** great for hover/active feedback; compositor-friendly patterns.
- **Cons:** transforms affect stacking contexts; can confuse hit testing if scaled.

#### What happens without it / when misused

- Transitioning `width` on a card inside a flex row causes reflow jank.

#### Examples

**Tiny — translate on hover**

```css
.card:hover {
  transform: translateY(-2px);
}
```

#### Quick checks

1. Name one layout property that commonly causes jank when transitioned.
2. Does `transform` change document flow for in-flow elements?

---

## `transition`: what can be interpolated smoothly

### What it is

`transition` defines how property changes animate over time when a computed style changes due to state (hover, class toggles, etc.).

#### Syntax and rules

```css
.button {
  transition: transform 160ms ease, box-shadow 160ms ease;
}
```

Gotchas:

- Not all properties interpolate intuitively (`display` does not transition usefully).
- `transition: all` is convenient but can accidentally animate expensive properties.

#### Quick checks

1. Why is `transition: all` risky?
2. What is the difference between `ease` and `linear`?

---

## `@keyframes` + `animation` shorthand

### What it is

`@keyframes` defines named stages (`from`/`to` or percentages). `animation` applies it with duration, easing, iteration, direction, fill mode.

#### Why it exists / why it matters

Keyframes encode looping loaders, attention pulses, and progress shimmer (use responsibly).

#### Syntax and rules

```css
@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.03);
  }
  100% {
    transform: scale(1);
  }
}

.badge {
  animation: pulse 1.2s ease-in-out infinite;
}
```

#### Quick checks

1. What does `animation-fill-mode: forwards` do?
2. Why should infinite animations be rare in productivity UIs?

---

## `prefers-reduced-motion`

### What it is

A user preference media query indicating reduced motion should be used when implementing non-essential animation.

#### Syntax and rules

```css
@media (prefers-reduced-motion: reduce) {
  .badge {
    animation: none;
  }
}
```

#### Quick checks

1. Is reduced motion only for “medical” users?
2. Name one acceptable reduced-motion fallback.

---

## `resize` and overflow discipline

### What it is

`resize` allows users to drag-resize elements, typically paired with `overflow: auto` and a constrained box.

#### Pros and cons

- **Pros:** power-user ergonomics for panels/logs.
- **Cons:** discoverability; mobile doesn’t map well to drag resize.

#### Syntax and rules

```css
.panel {
  overflow: auto;
  resize: vertical;
  min-height: 160px;
}
```

#### Quick checks

1. Which overflow value is commonly required for `resize` to work sensibly?
2. Why should resizable panels still have `min-width: 0` in flex layouts?

---

## Common mistakes & debugging

- Animating **`width`/`height`** on large subtrees.
- Creating **new stacking contexts** unintentionally (`transform`, `opacity`, `filter`).
- Forgetting **reduced motion** for infinite animations.
- Attribute selector typos (`dataState` vs `data-state`).

---

## Further reading

- MDN: [Attribute selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors)
- MDN: [`transform`](https://developer.mozilla.org/en-US/docs/Web/CSS/transform)
- MDN: [Using CSS transitions](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_transitions/Using_CSS_transitions)
- MDN: [Using CSS animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animations/Using_CSS_animations)
- MDN: [`prefers-reduced-motion`](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
- MDN: [`resize`](https://developer.mozilla.org/en-US/docs/Web/CSS/resize)

---

## Glossary

| Term | Meaning |
|------|---------|
| Keyframes | Named animation stages |
| Easing | Speed curve over time |
| Compositor | Browser layer that paints some effects efficiently |
| Stacking context | Painted layer grouping affecting `z-index` interactions |

---

## Answers (self-test)

### Attribute selectors

1. `[href$=".pdf"]`
2. Query strings change substring matches; prefer classing stable URLs or parse server-side.

### Transform vs layout

1. `width`, `height`, `top`, `left` (many layout-affecting properties) are common jank sources.
2. `transform` affects rendering geometry but does not change normal flow positioning the way changing in-flow box sizes does.

### Transition

1. It can animate unexpected expensive properties if they change together.
2. `linear` is constant speed; `ease` is slower at ends (default-ish ease curve).

### Keyframes

1. Keeps final keyframe styles applied after animation completes (depending on context).
2. Infinite motion distracts and drains attention—reserve for true background processes.

### Reduced motion

1. No—many users prefer reduced motion for focus and comfort.
2. Disable animation, replace with instant state change, or shorten to a subtle opacity transition.

### Resize

1. Often `auto` or `scroll`.
2. Flex items default `min-width:auto`; resizable children still participate in flex min-content calculations.
