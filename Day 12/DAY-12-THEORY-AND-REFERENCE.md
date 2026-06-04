# Day 12 — HTML5 Semantics, Containers, and Rich Inputs

**Primary theme:** Meaningful structure with HTML5 landmarks and safer forms using modern input types + built-in validation hooks  
**Estimated study time:** 2–3 hours theory + 4–7 hours tasks  
**Related tasks:** `task-01-semantic-skip-nav-article-page`, `task-02-landmarks-aside-nav-main`, `task-03-input-types-validation-clinic`, `task-04-constraint-validation-ux-patterns`  
**Instruction alignment:** Maps to *HTML5 tags*, *HTML5 input types*, and reinforces *forms and input tags* with accessibility expectations from the master topic list.

---

## Overview

Semantic HTML is not academic—it is **contractual communication** between your UI, browsers, assistive technologies, search engines, and future maintainers. A `<div>` tells nobody what it *means*. A `<main>` tells everyone where the primary content lives; a labeled `<input type="email">` tells mobile devices which keyboard to show and tells the browser which built-in validation rules are meaningful.

Day 12 pairs **structure** with **inputs**. You will practice choosing elements that create implicit landmarks, wiring skip-navigation patterns, and using validation attributes without immediately jumping to JavaScript frameworks.

---

## Day roadmap

1. [Sectioning content: `header`, `nav`, `main`, `footer`, `aside`, `section`, `article`](#sectioning-content-header-nav-main-footer-aside-section-article)
2. [Grouping content: `figure`/`figcaption`, lists, and when `div` is still OK](#grouping-content-figurefigcaption-lists-and-when-div-is-still-ok)
3. [HTML5 input types and why they matter](#html5-input-types-and-why-they-matter)
4. [Constraint validation attributes (built-in)](#constraint-validation-attributes-built-in)
5. [Accessible forms: labels, errors, and focus](#accessible-forms-labels-errors-and-focus)
6. [Common mistakes & debugging](#common-mistakes--debugging)
7. [Further reading](#further-reading)
8. [Glossary](#glossary)
9. [Answers (self-test)](#answers-self-test)

---

## Sectioning content: `header`, `nav`, `main`, `footer`, `aside`, `section`, `article`

### What it is

HTML5 **sectioning elements** carve a document into meaningful regions:

- `header` — introductory content for nearest sectioning context (not always page-top).
- `nav` — major navigation blocks (you may have more than one; label them accessibly when needed).
- `main` — **primary** content unique to the page; should appear **at most once** without `hidden`.
- `footer` — tail content: meta, links, copyright.
- `aside` — tangential content (sidebars, pull quotes) related to surrounding content.
- `section` — thematic grouping *with a heading* (avoid empty “div replacement”).
- `article` — self-contained composition (blog post, card article, forum post).

#### Why it exists / why it matters

Landmarks let screen reader users jump efficiently (“go to main”). Search engines infer page intent. CSS selectors become clearer: `main article h1` reads like English.

#### Pros and cons

- **Pros:** accessibility, maintainability, better default outline behavior when headings are sane.
- **Cons:** misuse (`<section>` everywhere) creates noisy landmark trees; multiple `main` mistakes break AT navigation.

#### What happens without it / when misused

- Everything is `<div>`: users hear “generic container” repeatedly; your team loses scanability in code review.

#### Syntax and rules

```html
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header>…</header>
  <nav aria-label="Primary">…</nav>
  <main id="main">…</main>
  <aside>…</aside>
  <footer>…</footer>
</body>
```

Gotchas:

- Do not place `header`/`footer` semantics above `<body>`.
- `main` must not be a descendant of `article` in some patterns—check your information architecture; if unsure, keep `main` as the page wrapper and place articles inside.

#### Examples

**Tiny — article with header/footer**

```html
<article>
  <header><h2>Release notes</h2></header>
  <p>…</p>
  <footer><p>Published <time datetime="2026-06-04">Jun 4, 2026</time></p></footer>
</article>
```

**Tiny — aside as related links**

```html
<aside aria-label="Related docs">
  <ul>…</ul>
</aside>
```

**Medium — two nav regions**

```html
<nav aria-label="Primary">…</nav>
<nav aria-label="Footer">…</nav>
```

#### Quick checks

1. How many visible `main` elements should a single view typically have?
2. Should a site-wide sidebar usually be `aside` or `nav`?
3. What is a practical reason to duplicate `nav` blocks (header + footer)?

---

## Grouping content: `figure`/`figcaption`, lists, and when `div` is still OK

### What it is

Not everything needs a landmark. `figure` + `figcaption` associate captions with media or code blocks. Lists (`ul`/`ol`) encode real sequences. `div` remains appropriate for **presentational** grouping when no semantic element exists.

#### Why it exists / why it matters

Captions and list semantics survive CSS failure and assistive tech modes.

#### Pros and cons

- **Pros:** clearer DOM; better copy/paste and reader modes.
- **Cons:** wrong list element harms semantics (`div` soup with `role="list"` is a smell unless justified).

#### What happens without it / when misused

- Code samples without `pre`/`code` structure become inaccessible walls of text.

#### Syntax and rules

```html
<figure>
  <pre><code>npm test</code></pre>
  <figcaption>Run tests from the task folder.</figcaption>
</figure>
```

#### Examples

**Tiny — ordered steps**

```html
<ol>
  <li>Read theory</li>
  <li>Edit TODOs</li>
  <li>Verify in browser</li>
</ol>
```

#### Quick checks

1. When is `div` the correct choice?
2. What element pairs with `figcaption`?

---

## HTML5 input types and why they matter

### What it is

Input types (`type="email"`, `url`, `tel`, `number`, `range`, `date`, `color`, etc.) change **UI widgets**, **keyboard** layouts, and **baseline validation** behavior.

#### Why it exists / why it matters

Mobile users get usable keyboards; desktop users get structured data earlier; you write less bespoke parsing for simple cases.

#### Pros and cons

- **Pros:** better UX; some validation for free.
- **Cons:** `number` has oddities (`e`, step mismatches); not all types are equally supported—always degrade gracefully.

#### What happens without it / when misused

- `type="text"` for emails yields garbage data and poor mobile UX.

#### Syntax and rules

```html
<label for="q">Search</label>
<input id="q" name="q" type="search" autocomplete="off">

<label for="dob">Date of birth</label>
<input id="dob" name="dob" type="date">
```

Gotchas:

- Always pair `label for` with stable `id`s.
- `name` is still required for forms that submit traditionally.

#### Examples

**Tiny — numeric input**

```html
<label for="qty">Quantity</label>
<input id="qty" name="qty" type="number" inputmode="numeric" min="1" max="99" step="1" value="1">
```

**Tiny — slider**

```html
<label for="vol">Volume</label>
<input id="vol" name="vol" type="range" min="0" max="100" value="40">
```

**Medium — URL with placeholder guidance**

```html
<label for="repo">Repository URL</label>
<input id="repo" name="repo" type="url" placeholder="https://github.com/org/project" required>
```

#### Quick checks

1. Which attribute connects a `<label>` to an `<input>`?
2. Why might `type="number"` be wrong for credit card digits?
3. Name one input type that changes mobile keyboard layout.

---

## Constraint validation attributes (built-in)

### What it is

Attributes like `required`, `min`, `max`, `step`, `minlength`, `maxlength`, and `pattern` enable the browser’s **constraint validation API** (`checkValidity()`, `reportValidity()`, validity pseudo-classes in CSS).

#### Why it exists / why it matters

You get immediate feedback without shipping a JS bundle—still pair with accessible messaging for production sites.

#### Pros and cons

- **Pros:** fast feedback; shared rules between client and (if mirrored) server.
- **Cons:** client-side validation is **not security**; patterns can be wrong or overly strict.

#### What happens without it / when misused

- Users submit empty required fields; `pattern` rejects valid international names.

#### Syntax and rules

```html
<label for="email">Email</label>
<input id="email" name="email" type="email" required autocomplete="email">

<label for="zip">ZIP (US demo)</label>
<input id="zip" name="zip" inputmode="numeric" pattern="\d{5}" maxlength="5" title="5 digits">
```

Gotchas:

- `title` on `pattern` fields is not a full a11y strategy—visible help text is better.
- `novalidate` on `<form>` disables native checks—use intentionally.

#### Examples

**Tiny — minlength**

```html
<label for="bio">Bio</label>
<textarea id="bio" name="bio" minlength="20" maxlength="280" required></textarea>
```

**Medium — range + output**

```html
<label for="score">Score</label>
<input id="score" name="score" type="range" min="0" max="10" value="7">
<output for="score">7</output>
```

#### Quick checks

1. Does `required` apply to hidden inputs?
2. What does `novalidate` do?
3. Why should `pattern` be used cautiously for names?

---

## Accessible forms: labels, errors, and focus

### What it is

Accessible forms ensure every control has a **programmatic name** (usually `<label>`), errors are **perceivable** (not color-only), and focus order matches reading order.

#### Why it exists / why it matters

Keyboard and AT users must be able to discover errors and fix fields without hunting.

#### Pros and cons

- **Pros:** better conversion; fewer support tickets.
- **Cons:** visible error text takes layout space—design for it early.

#### What happens without it / when misused

- Placeholder-only “labels” disappear when typing; users forget what a field was for.

#### Syntax and rules

```html
<label for="pw">Password</label>
<input id="pw" name="password" type="password" autocomplete="new-password" required aria-describedby="pw-help">
<p id="pw-help">At least 12 characters.</p>
```

#### Examples

**Tiny — `:focus-visible` ring**

```css
:where(input, textarea, select):focus-visible {
  outline: 3px solid #2563eb;
  outline-offset: 2px;
}
```

#### Quick checks

1. Why are placeholders poor substitutes for labels?
2. What does `aria-describedby` connect?
3. What is wrong with error messages that are red text only?

---

## Common mistakes & debugging

- Multiple `main` elements without `hidden` → invalid landmark tree.
- `h1` everywhere inside list cards → heading outline noise; prefer stepped headings per component rules.
- `pattern` without human-readable instructions → angry users.
- `type="number"` for non-numeric identifiers (leading zeros).
- Missing `autocomplete` on login/register flows → worse password manager UX.

---

## Further reading

- MDN: [Document and website structure](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Document_and_website_structure)
- MDN: [`<main>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/main)
- MDN: [Input types](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#input_types)
- MDN: [Constraint validation](https://developer.mozilla.org/en-US/docs/Web/HTML/Constraint_validation)
- MDN: [ARIA: `aria-describedby`](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-describedby)

---

## Glossary

| Term | Meaning |
|------|---------|
| Landmark | Major navigable region (`main`, `nav`, etc.) |
| Constraint validation | Browser checks for field validity |
| `inputmode` | Hint for virtual keyboard layout |
| `autocomplete` | Hint for autofill tokens |

---

## Answers (self-test)

### Sectioning

1. Typically **one** visible `main` per page view.
2. Sidebars are often `aside` if tangential; use `nav` if primarily link navigation.
3. Footer nav repeats utility links when users finish reading—common and OK with distinct `aria-label`s.

### Grouping

1. When no semantic element matches and you need a hook for styling/layout only.
2. `figure`.

### Input types

1. `for` on `<label>` matches `id` on control.
2. Leading zeros and non-numeric semantics; use `text` + `inputmode="numeric"` sometimes.
3. `email`, `url`, `tel`, etc.

### Constraint validation

1. Hidden inputs participate depending on `disabled`/`hidden` nuances—be careful; often use server validation for hidden fields.
2. Disables native validation for that form submit.
3. Many real human names fail naive patterns—document and test inclusively.

### Accessible forms

1. Placeholders disappear; low contrast; not always announced as a name.
2. Help text element id(s) for additional description.
3. Color-only errors fail WCAG—add text/icons and programatic association.
