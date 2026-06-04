# Day 02 — Text Semantics & Formatting

**Primary theme:** Meaningful text markup paired with readable CSS typography  
**Estimated study time:** 1–2 hours theory + 3–5 hours tasks  
**Related tasks:** `task-01-article-outline-headings`, `task-02-inline-semantics-and-lists`, `task-03-font-stack-and-line-height`, `task-04-inheritance-reading-page`  
**Instruction alignment:** Maps to *Text formatting tags and CSS text formatting*, *Cascading and inheritance (preview)* from the master topic list.

---

## Overview

Readable interfaces are mostly text. Browsers expose a **semantic layer** to assistive technologies through element choice, not through how bold something looks. Today you will align **meaning** (`<strong>` vs `<b>`) with **presentation** (CSS weights), build lists that scan well, and tune **line-height** and **font stacks** so multi-paragraph assignments remain pleasant on inexpensive laptops and phones.

---

## Day roadmap

1. [Semantic text elements](#semantic-text-elements)
2. [Paragraphs, quotations, and code snippets](#paragraphs-quotations-and-code-snippets)
3. [Lists: unordered, ordered, and description](#lists-unordered-ordered-and-description)
4. [CSS typography: stacks, size, weight, line-height](#css-typography-stacks-size-weight-line-height)
5. [Inheritance preview](#inheritance-preview)
6. [Common mistakes & debugging](#common-mistakes--debugging)
7. [Further reading](#further-reading)
8. [Glossary](#glossary)
9. [Answers (self-test)](#answers-self-test)

---

## Semantic text elements

### What it is

Elements like `<strong>`, `<em>`, `<mark>`, and `<abbr>` encode **intent**. `<strong>` indicates strong importance or urgency for the current context; `<em>` stresses **emphasis** that might change spoken inflection. `<mark>` highlights text referenced elsewhere (search hits, user selections). `<abbr title="...">` expands abbreviations for hover and assistive tech.

#### Why it exists / why it matters

Screen readers can change voice parameters for `<em>`/`<strong>`. Search engines use semantics as weak signals. When CSS fails to load, semantics still communicate structure.

#### Pros and cons

- **Pros:** Accessible defaults; meaningful DOM for scripts and tests.
- **Pros:** Clear separation of meaning (HTML) from skin (CSS).
- **Cons:** More element names to learn than “everything is a `<div>`”.
- **Cons:** Misusing `<strong>` for styling alone confuses non-visual users.

#### What happens without it / when misused

- Using `<b>`/`<i>` purely for bold/italic without semantic reason is not a crime, but **prefer** `strong`/`em` when the meaning matches.
- Styling `<span class="bold">` alone loses built-in semantics unless you add ARIA (heavier than picking the right tag).

#### Syntax and rules

```html
<p><strong>Due date:</strong> Friday, 17:00.</p>
<p>She said <em>maybe</em>—not a yes.</p>
<p>Search matched <mark>closure</mark> in paragraph two.</p>
<p><abbr title="HyperText Markup Language">HTML</abbr> is not a programming language.</p>
```

#### Examples

**Tiny**

```html
<strong>Warning:</strong> experimental feature.
```

**Tiny**

```html
<em>First</em> does not mean <em>most important</em>.
```

**Medium**

```html
<p>
  Press <kbd>Ctrl</kbd> + <kbd>S</kbd> to save. The shell printed
  <samp>OK: wrote 12 lines</samp> after running <code>npm test</code>.
</p>
```

#### Quick checks (self-test questions)

1. When is `<strong>` more appropriate than CSS `font-weight` alone on a `<span>`?
2. Difference between `<em>` and `<i>` in terms of default semantics?
3. What attribute belongs on `<abbr>` to provide expansion?

---

## Paragraphs, quotations, and code snippets

### What it is

`<p>` separates **paragraph-level** prose. `<blockquote>` marks extended quotations (often with `cite` URL attribute). `<q>` is for **inline** quotes. `<pre><code>` preserves whitespace for code blocks.

#### Why it exists / why it matters

Assistive technologies navigate by paragraph boundaries. Code formatted with `<pre>` avoids mangling indentation that `<p>` would collapse.

#### Pros and cons

- **Pros:** Predictable reading rhythm; better copy/paste from docs.
- **Cons:** Nested `<p>` inside `<p>` is invalid—split or use `<div>` with role carefully.

#### What happens without it / when misused

- Wall of `<br>` elements is hard to maintain and non-semantic.
- Using `<blockquote>` purely as a decorative indent without a quote misleads semantics.

#### Syntax and rules

```html
<blockquote cite="https://example.com/article">
  <p>One paragraph from the source.</p>
</blockquote>
<p>As Alan Perlis quipped, <q>Syntax sugar causes cancer of the semicolon.</q></p>
```

#### Examples

**Tiny — code phrase**

```html
Use the <code>line-height</code> property.
```

**Tiny — preformatted**

```html
<pre><code>git status
git diff</code></pre>
```

**Medium — blockquote with attribution**

```html
<figure>
  <blockquote>
    <p>Make it work, make it right, make it fast.</p>
  </blockquote>
  <figcaption>— Kent Beck (popular ordering)</figcaption>
</figure>
```

#### Quick checks

1. Why must you not nest `<p>` inside `<p>`?
2. When choose `<q>` instead of `<blockquote>`?
3. Which pair preserves spaces and newlines for multi-line shell output?

---

## Lists: unordered, ordered, and description

### What it is

`<ul><li>` for unordered sets, `<ol><li>` for sequences with meaningful order, `<dl><dt><dd>` for term/definition groups (also useful for metadata lists).

#### Why it exists / why it matters

Screen readers announce list length and position. Using `<ol>` for procedural steps reduces user error compared to manual “1.” prefixes inside `<p>`.

#### Pros and cons

- **Pros:** Built-in numbering styles; easy CSS hooks (`li + li` margins).
- **Cons:** Deeply nested lists hurt scanning—flatten when possible.

#### What happens without it / when misused

- Fake lists with `<div>` bullets harm accessibility unless remediated with ARIA (avoid).

#### Syntax and rules

```html
<ol>
  <li>Clone the repo.</li>
  <li>Open <code>Day 02</code> tasks.</li>
</ol>
```

#### Examples

**Tiny — unordered**

```html
<ul>
  <li>HTML</li>
  <li>CSS</li>
</ul>
```

**Tiny — description list**

```html
<dl>
  <dt>inheritance</dt>
  <dd>Some CSS properties take computed values from ancestors.</dd>
</dl>
```

**Medium — nested procedure**

```html
<ol>
  <li>Read theory
    <ul>
      <li>Skim roadmap first</li>
      <li>Deep-read one subsection</li>
    </ul>
  </li>
  <li>Open Task 01</li>
</ol>
```

#### Quick checks

1. Which list type announces “step 2 of 5” more reliably?
2. Name a good `<dl>` use case besides dictionary definitions.
3. Valid pattern: `<li>` directly inside `<ul>`—true or false?

---

## CSS typography: stacks, size, weight, line-height

### What it is

- **`font-family` list:** ordered fallbacks (`system-ui, -apple-system, Segoe UI, Roboto, sans-serif`).
- **`font-size`:** length in `px`, `rem`, etc. (you will deepen units on Day 06).
- **`font-weight`:** numeric (`100`–`900`) or keywords (`normal`, `bold`).
- **`line-height`:** unitless number (preferred multiplier) or length; controls vertical rhythm.

#### Why it exists / why it matters

Readable body copy typically uses `line-height` between `1.4` and `1.7`. Poor stacks cause **FOUC**-like font swapping and inconsistent metrics across OSes.

#### Pros and cons

- **Pros:** Unitless `line-height` inherits predictably as a multiplier.
- **Pros:** System font stacks avoid network latency.
- **Cons:** Over-tight line-height hurts dyslexic readers.
- **Cons:** Too many webfonts increase payload (later course days).

#### What happens without it / when misused

- `line-height: 1` on long essays reduces comprehension.
- Single-font stacks with rare fonts fall back to unexpected faces.

#### Syntax and rules

```css
body {
  font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  font-size: 1.05rem;
  line-height: 1.6;
}
```

#### Examples

**Tiny — stack**

```css
code, kbd, samp {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}
```

**Tiny — weight**

```css
strong {
  font-weight: 650;
}
```

**Medium — scale**

```css
h1 { font-size: 2rem; line-height: 1.2; }
h2 { font-size: 1.5rem; line-height: 1.25; }
p  { font-size: 1rem; line-height: 1.65; }
```

#### Quick checks

1. Why prefer unitless `line-height` for body text?
2. What does the browser do when the first font in a stack is missing a glyph?
3. Which property most affects vertical distance between wrapped lines?

---

## Inheritance preview

### What it is

Many CSS properties **inherit** into descendants: `color`, `font-family`, `font-size` (with caveats), `line-height` (when unitless). Others do not: `margin`, `border`, `background-color` on parent do not auto-paint children backgrounds.

#### Why it exists / why it matters

You can set a readable base on `body` and let articles inherit, overriding only where needed—less duplication, fewer drift bugs.

#### Pros and cons

- **Pros:** DRY typography; predictable defaults.
- **Cons:** Inherited `font-size` on nested elements with `em` compounds—watch Day 06 for `rem` guidance.

#### What happens without it / when misused

- Setting `color` on every `<p>` is noisy; missing `color` on `body` may fall back to user agent defaults inconsistently with your brand.

#### Syntax and rules

```css
body {
  color: #0f172a;
}
article a {
  color: #0369a1; /* overrides inherited body color */
}
```

#### Examples

**Tiny**

```css
body { font-family: system-ui, sans-serif; }
```

**Tiny — override**

```css
aside.note {
  font-family: Georgia, serif;
}
```

**Medium**

```css
body {
  color: #111827;
  line-height: 1.6;
}
main section.lede {
  font-size: 1.125rem; /* inherits line-height multiplier from body unless overridden */
}
```

#### Quick checks

1. Does `border` on `body` inherit to `p`?
2. If `body` sets `color`, does `span` inside `p` use that color by default?
3. Why can `em`-based `font-size` on nested lists become huge?

---

## Common mistakes & debugging

- **Invalid nesting:** `<p>` containing `<ul>` closes the `<p>` implicitly in HTML—structure lists outside paragraphs.
- **Fake headings:** giant bold `<p>`—use real heading levels.
- **Contrast:** light gray text on white—use DevTools Accessibility panel.

---

## Further reading

- [MDN — HTML text content elements](https://developer.mozilla.org/en-US/docs/Web/HTML/Element#inline_text_semantics)
- [MDN — font-family](https://developer.mozilla.org/en-US/docs/Web/CSS/font-family)
- [MDN — line-height](https://developer.mozilla.org/en-US/docs/Web/CSS/line-height)
- [MDN — Inheritance](https://developer.mozilla.org/en-US/docs/Web/CSS/inheritance)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Semantic element** | Tag chosen for meaning, not only appearance. |
| **Inheritance** | Child elements receive computed values for certain properties from ancestors. |
| **Font stack** | Ordered `font-family` fallback list. |

---

## Answers (self-test)

**Semantic text**

1. When the text carries importance/urgency beyond mere visual bolding.
2. `<em>` has emphasis semantics; `<i>` represents offset text without inherent emphasis (voice, technical term) per HTML—use the one that matches meaning.
3. `title` on `<abbr>`.

**Paragraphs / quotes**

1. Invalid HTML; parsers will auto-close earlier `<p>`.
2. Short inline quotations vs long cited excerpts.
3. `<pre>` (with `<code>` inside commonly).

**Lists**

1. `<ol>`.
2. Metadata key/value rows, FAQ question/answer pairs.
3. True.

**Typography**

1. It scales cleanly when `font-size` changes on descendants.
2. It tries the next font in the list for missing glyphs or families.
3. `line-height`.

**Inheritance**

1. No (border is not inherited).
2. Yes, unless a closer rule sets another `color`.
3. `em` compounds relative to parent computed size—nested levels multiply.
