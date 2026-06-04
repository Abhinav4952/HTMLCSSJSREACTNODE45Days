# Day 01 — Basic Page Structure & Metadata

**Primary theme:** Valid HTML5 document shell, essential metadata, and correct loading of CSS and JavaScript  
**Estimated study time:** 1–2 hours theory + 3–5 hours tasks  
**Related tasks:** `task-01-minimal-valid-document`, `task-02-head-metadata-basics`, `task-03-external-assets-defer-async`, `task-04-structured-profile-page`  
**Instruction alignment:** Maps to *Basic HTML page structure*, *Document Type Definition; HTML vs XHTML*, *Metadata, styles, scripts (`<meta>`, `<link>`, `<script>`, defer/async)* from the master topic list.

---

## Overview

Every web page is a contract between you, the browser, and (often) search engines and assistive technologies. The invisible first lines of your file—doctype, charset, language on `<html>`—determine parsing mode, text decoding, and accessibility defaults. Getting the skeleton right prevents an entire class of “it works on my machine” bugs when content is copied into CMS templates, email clients, or SSR frameworks. Today you will build reflexes for a minimal **valid** document and for **metadata** that helps users and machines understand the page before any layout or script runs.

---

## Day roadmap

1. [Document type declaration and the `<html>` root](#document-type-declaration-and-the-html-root)
2. [HTML5 versus XHTML-style markup in practice](#html5-versus-xhtml-style-markup-in-practice)
3. [The `<head>`: metadata, title, icons, and social previews](#the-head-metadata-title-icons-and-social-previews)
4. [The `<body>` and high-level document semantics](#the-body-and-high-level-document-semantics)
5. [Linking CSS and JavaScript (`<link>`, `<script>`, `defer`, `async`)](#linking-css-and-javascript-link-script-defer-async)
6. [Common mistakes & debugging](#common-mistakes--debugging)
7. [Further reading](#further-reading)
8. [Glossary](#glossary)
9. [Answers (self-test)](#answers-self-test)

---

## Document type declaration and the `<html>` root

### What it is

The **document type declaration** (`<!DOCTYPE html>` in HTML5) is a single line at the very top of the file that tells the browser to use **standards mode** for layout and scripting. The `<html>` element wraps the entire document; it accepts a `lang` attribute (e.g. `lang="en"`) that guides pronunciation for screen readers and hyphenation.

#### Why it exists / why it matters

Historically, browsers had “quirks mode” for legacy pages without a doctype. Missing or wrong doctypes produced inconsistent box model behavior and subtle JavaScript differences. Declaring HTML5 gives you the most predictable baseline across evergreen browsers.

#### Pros and cons

- **Pros:** Standards mode; predictable CSS; matches documentation and tutorials written for HTML5.
- **Pros:** `lang` improves accessibility and can help search engines infer audience.
- **Cons:** None meaningful for new projects—always include `<!DOCTYPE html>`.
- **Cons / tradeoffs:** Very old intranet pages sometimes relied on quirks mode; migrating them requires testing (not your default for new work).

#### What happens without it / when misused

- Omitting `<!DOCTYPE html>` may trigger **quirks mode**: margins, widths, and table layout can diverge from MDN examples.
- Omitting `lang` does not break rendering, but hurts screen reader UX and can reduce clarity for translation tools.

#### Syntax and rules

- First bytes of the file: `<!DOCTYPE html>` (case-insensitive in HTML5, but uppercase is conventional).
- Next: `<html lang="en">` … `</html>` wrapping `<head>` then `<body>` (order is fixed: head before body).

#### Examples

**Tiny — minimal valid HTML5**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Example</title>
  </head>
  <body>
    <p>Hello.</p>
  </body>
</html>
```

**Tiny — wrong order (invalid / avoid)**

```html
<!DOCTYPE html>
<html lang="en">
  <body><p>Oops</p></body>
  <head><title>Too late</title></head>
</html>
```

**Medium — language choice**

```html
<!DOCTYPE html>
<html lang="es-MX">
  <head>
    <meta charset="utf-8" />
    <title>Catálogo</title>
  </head>
  <body>
    <p>Bienvenido.</p>
  </body>
</html>
```

#### Quick checks (self-test questions)

1. What mode does the browser aim for when `<!DOCTYPE html>` is present?
2. Why is `lang` on `<html>` recommended even if all visible text is English?
3. Where must `<head>` appear relative to `<body>` in a valid document?

---

## HTML5 versus XHTML-style markup in practice

### What it is

**XHTML** was an XML serialization of HTML: strict nesting, lowercase elements, self-closing tags with a trailing slash (`<br />`), and MIME type `application/xhtml+xml` in theory. **HTML5** is the living HTML standard: more forgiving parsing rules in `.html` files, optional trailing slashes on void elements, and case-insensitive tag names—while still encouraging consistent, readable style.

#### Why it exists / why it matters

You will still see XHTML habits in older templates, React’s JSX (XML-like rules), and SVG embedded in HTML. Understanding the difference prevents confusion when a validator or formatter complains about “unclosed” tags in one context but not another.

#### Pros and cons

- **Pros (HTML5 text/html):** Faster authoring; browsers recover gracefully from small mistakes during learning.
- **Pros (XHTML mindset):** Strict nesting and explicit closes improve readability and interop with XML pipelines.
- **Cons:** Mixing serializations without understanding MIME types and parsing leads to subtle bugs in edge cases.
- **Cons:** Over-relying on browser error correction hides mistakes until you use a stricter tool.

#### What happens without it / when misused

- Serving XHTML with wrong headers can cause browsers to show XML parse errors instead of rendering.
- Copy-pasting XHTML into JSX without adjusting attribute names (`class` → `className`) breaks builds.

#### Syntax and rules

- For **this course’s static `.html` files**, use HTML5 conventions: `<!DOCTYPE html>`, lowercase tags, optional but consistent self-closing on void elements (`<meta charset="utf-8">` is fine).
- Boolean attributes in HTML5: `checked` instead of `checked="checked"` (both valid; pick one style and stay consistent).

#### Examples

**Tiny — HTML5 void element**

```html
<meta charset="utf-8">
<img src="logo.svg" alt="Logo">
```

**Tiny — JSX-style (not raw HTML file)**

```jsx
// In React JSX, self-closing is required for components and img/br/input
<img src="logo.svg" alt="Logo" />
```

**Medium — conceptual comparison**

| Concern | HTML5 `text/html` | Classic XHTML 1.0 |
|--------|-------------------|---------------------|
| Parsing | HTML rules (forgiving) | XML rules (strict) |
| `/>` on voids | Optional | Expected in XML serialization |
| Error on typo | Often still renders | May not render as XML |

#### Quick checks (self-test questions)

1. Why might `<br>` appear with and without `/>` in different codebases?
2. Name one place XML-like rules still influence front-end developers today.
3. Should you serve the same file as both `text/html` and `application/xhtml+xml` without a reason?

---

## The `<head>`: metadata, title, icons, and social previews

### What it is

The `<head>` holds **machine-oriented** information: character encoding, viewport for mobile layout, title shown in tabs, linked stylesheets, preloaded fonts, JSON-LD, Open Graph tags for social cards, and favicons. Nothing in `<head>` is directly visible as page content, but it shapes how the page loads and how it is summarized elsewhere.

#### Why it exists / why it matters

Search engines and social platforms read `<meta>` and `<link rel="canonical">` before executing your JavaScript. Mobile browsers use `viewport` to decide initial scale. Wrong or missing `charset` can mangle punctuation in user-generated content.

#### Pros and cons

- **Pros:** Central place to declare global behavior once per navigation.
- **Pros:** Social meta tags improve click-through when links are shared.
- **Cons:** Too many blocking `<script>` tags in `<head>` without `defer` delays first paint (you will fix this with loading strategies on later days too).
- **Cons:** Duplicate or conflicting meta tags confuse crawlers.

#### What happens without it / when misused

- Missing `<meta charset="utf-8">` risks **mojibake** (e.g. “café” shown incorrectly) if bytes are interpreted as a legacy encoding.
- Missing `viewport` makes mobile users see a tiny desktop-scaled page.
- Empty or generic `<title>` hurts tab navigation and SEO.

#### Syntax and rules

- Put `charset` in the first 1024 bytes of the document (place it early in `<head>`).
- Typical mobile-friendly viewport:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

#### Examples

**Tiny — smallest responsible head**

```html
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Order #1042 — Acme Shop</title>
</head>
```

**Tiny — description for search snippets**

```html
<meta name="description" content="Practice lab for graduate web course, Day 01.">
```

**Medium — Open Graph (optional pattern)**

```html
<meta property="og:title" content="Day 01 Lab">
<meta property="og:description" content="Document structure practice.">
<meta property="og:type" content="website">
```

#### Quick checks (self-test questions)

1. Why should `charset` appear early?
2. What user-visible string comes from `<title>`?
3. Name two meta tags that affect mobile layout or scaling.

---

## The `<body>` and high-level document semantics

### What it is

The `<body>` contains **visible** (or visually hidden but accessibility-exposed) content: headings, paragraphs, navigation landmarks, main content, footers, and embedded media. Even on Day 01, prefer a simple outline: one logical `<h1>` per view where possible, then `<h2>` for sections, without skipping levels.

#### Why it exists / why it matters

Landmarks and heading order are the backbone of keyboard and screen reader navigation. Semantic structure also helps readers skim long assignments in the browser.

#### Pros and cons

- **Pros:** Clear outline improves accessibility and maintainability.
- **Pros:** Matches how CSS cascade and future layout modules attach to elements.
- **Cons:** Over-nesting `<div>` wrappers without semantics obscures structure (you will refine semantics on later days).

#### What happens without it / when misused

- Multiple unlabeled `<h1>` elements confuse assistive tech outline views.
- Putting primary text only inside `<div>` with no headings makes long instructional pages hard to navigate.

#### Syntax and rules

- Use `<main>` once per page when representing primary content (pattern used in tasks when appropriate).
- Pair interactive controls with labels (preview of Day 04).

#### Examples

**Tiny — minimal body**

```html
<body>
  <p>Visible text lives here.</p>
</body>
```

**Tiny — landmark sketch**

```html
<body>
  <header><h1>Course lab</h1></header>
  <main>
    <p>Primary instructions…</p>
  </main>
  <footer><p>Footer note</p></footer>
</body>
```

**Medium — heading outline**

```html
<body>
  <main>
    <h1>Day 01 submission</h1>
    <section aria-labelledby="sec-a">
      <h2 id="sec-a">Part A</h2>
      <p>…</p>
    </section>
    <section aria-labelledby="sec-b">
      <h2 id="sec-b">Part B</h2>
      <p>…</p>
    </section>
  </main>
</body>
```

#### Quick checks (self-test questions)

1. Which landmark element should wrap the primary unique content of a page?
2. Why is skipping heading levels (e.g. `<h1>` then `<h3>`) discouraged?
3. Where do `<header>` and `<footer>` usually live relative to `<main>`?

---

## Linking CSS and JavaScript (`<link>`, `<script>`, `defer`, `async`)

### What it is

- `<link rel="stylesheet" href="styles.css">` pulls CSS **without** blocking HTML parsing after modern browser optimizations, but CSS still participates in render blocking when needed for first paint.
- `<script src="app.js">` **without** `defer` or `async` is **classic blocking**: the browser fetches and runs the script before continuing to parse HTML below it.
- **`defer`:** script downloads in parallel, runs **after** HTML is fully parsed, preserves document order among deferred scripts.
- **`async`:** script downloads in parallel, runs **as soon as** it is ready—order between multiple async scripts is not guaranteed; best for independent analytics snippets, not your app bundle that mutates the DOM on load.

#### Why it exists / why it matters

Script placement and loading flags directly affect **First Contentful Paint** and race conditions (“cannot read property of null” when script runs before DOM nodes exist).

#### Pros and cons

- **Pros:** `defer` on `<script src>` in `<head>` is the modern default for bundled apps.
- **Pros:** `async` isolates third-party code that should not delay your render pipeline.
- **Cons:** Misusing `async` for dependent scripts causes intermittent bugs.
- **Cons:** Inline scripts without `defer` still block if placed early.

#### Syntax and rules

```html
<link rel="stylesheet" href="/styles/base.css">
<script src="/scripts/metrics.js" async></script>
<script src="/scripts/main.js" defer></script>
```

Place DOM-dependent logic in `defer` scripts or at the end of `<body>` (both patterns are valid; pick one style per project).

#### Examples

**Tiny — blocking script (avoid for authored app JS)**

```html
<script src="legacy-blocker.js"></script>
```

**Tiny — deferred app script**

```html
<script src="app.js" defer></script>
```

**Medium — order demonstration concept**

```html
<script>
  window.LOG = window.LOG || [];
  window.LOG.push("inline head runs when parsed");
</script>
<script src="a.js" defer></script>
<script src="b.js" defer></script>
<!-- If a.js and b.js both use defer, they run in document order after parse -->
```

#### Quick checks (self-test questions)

1. When should you prefer `defer` over `async` for two scripts that both touch the same DOM?
2. Where does a blocking `<script>` without `defer`/`async` in `<head>` run relative to parsing the rest of the document?
3. Which attribute pair preserves execution order among multiple external files?

---

## Common mistakes & debugging

- **Quirks mode symptoms:** widths look “off” compared to tutorials—check `<!DOCTYPE html>`.
- **Wrong characters:** verify `<meta charset="utf-8">` and that your editor saves UTF-8.
- **Script “cannot find element”:** script ran before DOM—use `defer` or move script to end of `<body>`.
- **Styles not loading:** typo in `href`, wrong relative path, or hard refresh cached 404 (`Cmd+Shift+R` / `Ctrl+Shift+R`).

---

## Further reading

- [MDN — Document structure](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Document_and_website_structure)
- [MDN — `<meta>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta)
- [MDN — Script loading strategies](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#attributes)
- [WHATWG HTML standard (single-page)](https://html.spec.whatwg.org/multipage/)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Standards mode** | Browser layout mode aligned with modern CSS specifications. |
| **Quirks mode** | Legacy compatibility layout mode triggered by missing/incorrect doctype. |
| **Metadata** | Data about the document (charset, description, viewport). |
| **`defer` / `async`** | Attributes controlling when external scripts execute. |

---

## Answers (self-test)

**Document type / `<html>`**

1. Standards mode (approximately; doctype selects between quirks and limited-quirks vs standards in browser engines).
2. Screen readers use `lang` for pronunciation; it also documents intent for translation and indexing.
3. `<head>` must appear before `<body>`.

**HTML vs XHTML**

1. Different authoring conventions and serializer expectations; JSX requires XML-like closing rules.
2. JSX, SVG integration, some CMS exports.
3. No—pick a deliberate serialization unless you have a rare pipeline requirement.

**`<head>`**

1. So the byte scanner picks UTF-8 before decoding the rest of the file.
2. The browser tab title and default bookmark label.
3. Example answers: `charset`, `viewport` (also accept theme-color, etc.).

**`<body>` / semantics**

1. `<main>` for primary content (once per document in typical patterns).
2. Assistive technologies expose a heading tree; skips confuse navigation.
3. Typically as siblings inside `<body>`: `<header>`, `<main>`, `<footer>` is a common pattern.

**Scripts**

1. When scripts depend on each other or on the full DOM—`defer` runs in order after parse.
2. Before subsequent HTML is parsed (blocking).
3. `defer` (multiple deferred scripts run in document order).
