# Day 04 — Forms Foundation

**Primary theme:** Accessible HTML forms, control types, and HTTP method choice  
**Estimated study time:** 1–2 hours theory + 3–6 hours tasks  
**Related tasks:** `task-01-labeled-fieldset-form`, `task-02-html5-inputs-validation`, `task-03-textarea-select-buttons`, `task-04-get-post-method-lab`  
**Instruction alignment:** Maps to *Forms and input tags*; connects to later React controlled forms.

---

## Overview

Forms are the bridge between human intent and server processing. The browser gives you **built-in validation** and **keyboard affordances** for free if you pick the right elements and labels. Today focuses on **static HTML forms** (no backend required): you will still set `action` to a harmless placeholder or `#` where instructed and reason about **GET** (idempotent reads, bookmarkable query strings) vs **POST** (mutations, larger payloads).

---

## Day roadmap

1. [`<form>` attributes: `action`, `method`, `name`](#form-attributes-action-method-name)
2. [Labels, placeholders, and why placeholders are not labels](#labels-placeholders-and-why-placeholders-are-not-labels)
3. [Text inputs, text areas, selects, buttons](#text-inputs-text-areas-selects-buttons)
4. [HTML5 input types and validation attributes](#html5-input-types-and-validation-attributes)
5. [GET vs POST (conceptual)](#get-vs-post-conceptual)
6. [Common mistakes & debugging](#common-mistakes--debugging)
7. [Further reading](#further-reading)
8. [Glossary](#glossary)
9. [Answers (self-test)](#answers-self-test)

---

## `<form>` attributes: `action`, `method`, `name`

### What it is

`<form>` wraps controls that submit together. `action` is the URL that receives the submission; `method` is usually `get` or `post` (lowercase in HTML). `autocomplete` can tune browser heuristics.

#### Why it exists / why it matters

Without a form, pressing Enter in a field may not submit consistently. Grouping ensures one **Submit** button targets the correct handler.

#### Pros and cons

- **Pros:** Native keyboard flow (`tab`, `enter` to submit).
- **Cons:** Wrong `action` sends data to unexpected endpoints—use safe placeholders in labs.

#### What happens without it / when misused

- Missing `method` defaults to **GET**—surprising if you intended a mutation.

#### Syntax and rules

```html
<form action="https://example.com/search" method="get">
  <!-- controls -->
</form>
```

#### Examples

**Tiny — GET search**

```html
<form action="#" method="get">
  <label for="q">Query</label>
  <input id="q" name="q" type="search">
  <button type="submit">Search</button>
</form>
```

**Tiny — POST-ish lab**

```html
<form action="#" method="post">
  <button type="submit">Save</button>
</form>
```

**Medium — grouping**

```html
<form action="#" method="post" novalidate>
  <!-- novalidate only if you are teaching custom JS validation later; default in tasks: omit unless stated -->
</form>
```

#### Quick checks

1. Default `method` if omitted?
2. Why might you avoid a real `action` URL in classroom exercises?
3. Does HTML require uppercase `POST`?

---

## Labels, placeholders, and why placeholders are not labels

### What it is

`<label for="id">` references a control `id`. Wrapping a control inside `<label>` also works. **Placeholders** are short hints inside the field; they disappear when typed and are **not** a replacement for labels.

#### Why it exists / why it matters

Screen readers announce **labels** reliably; placeholder support is inconsistent for the accessibility name calculation.

#### Pros and cons

- **Pros:** Larger click/tap targets when label wraps input.
- **Cons:** Clicking misaligned custom widgets without labels breaks usability.

#### What happens without it / when misused

- Icon-only fields without `aria-label`/`label` are effectively unnamed for many AT users.

#### Syntax and rules

```html
<label for="email">Email</label>
<input id="email" name="email" type="email" autocomplete="email">
```

#### Examples

**Tiny — wrapped**

```html
<label>
  Remember me
  <input name="remember" type="checkbox">
</label>
```

**Tiny — `for`/`id`**

```html
<label for="pw">Password</label>
<input id="pw" name="password" type="password" minlength="10" required>
```

**Medium — `fieldset`**

```html
<fieldset>
  <legend>Shipping speed</legend>
  <label><input type="radio" name="speed" value="std"> Standard</label>
  <label><input type="radio" name="speed" value="exp"> Express</label>
</fieldset>
```

#### Quick checks

1. Name two ways to associate a label with an input.
2. Why is placeholder-only naming bad?
3. What element titles a `<fieldset>`?

---

## Text inputs, text areas, selects, buttons

### What it is

- `<input>` is a large family of types (`text`, `email`, `number`, …).
- `<textarea>` holds multi-line text; `rows`/`cols` are hints, CSS usually controls size.
- `<select>` offers discrete choices; `<option>` values submit.
- `<button type="button">` does not submit; `type="submit"` (default in many contexts) submits the nearest form.

#### Why it exists / why it matters

Correct `type` triggers appropriate keyboards on mobile (`inputmode`, `type="tel"`). Correct button types prevent accidental double submits during JS experiments.

#### Pros and cons

- **Pros:** Free validation UI for many types.
- **Cons:** `number` inputs carry locale quirks—still fine for learning with simple integers.

#### What happens without it / when misused

- `button` without `type` inside a form may default to submit—unexpected when you meant a toggle.

#### Syntax and rules

```html
<textarea name="notes" rows="6" maxlength="500"></textarea>
<select name="country">
  <option value="">Choose…</option>
  <option value="us">United States</option>
</select>
<button type="button">Preview</button>
<button type="submit">Send</button>
```

#### Examples

**Tiny — select**

```html
<select name="size">
  <option>S</option>
  <option>M</option>
</select>
```

**Tiny — textarea**

```html
<textarea name="bio" required></textarea>
```

**Medium — button types**

```html
<form action="#" method="post">
  <button type="submit">Submit</button>
  <button type="reset">Reset</button>
  <button type="button" onclick="/* later: avoid inline in real apps */">Help</button>
</form>
```

#### Quick checks

1. Default `type` for `<button>` inside `<form>`?
2. Which control should you use for 500 characters of feedback?
3. What attribute sets the submitted key for a text field?

---

## HTML5 input types and validation attributes

### What it is

Types like `email`, `url`, `tel`, `date`, and `number` enable basic client-side validation. Attributes: `required`, `min`, `max`, `step`, `pattern`, `minlength`, `maxlength`.

#### Why it exists / why it matters

Client validation improves UX; **server-side validation is still mandatory** for security (not implemented in these static tasks).

#### Pros and cons

- **Pros:** Fast feedback; less junk data.
- **Cons:** Regex in `pattern` can be inaccessible if error messages are poor—pair with visible help text.

#### What happens without it / when misused

- `pattern` without human-readable instructions frustrates users.

#### Syntax and rules

```html
<input name="age" type="number" min="18" max="120" step="1" required>
```

#### Examples

**Tiny — email**

```html
<input type="email" name="email" required>
```

**Tiny — pattern with title**

```html
<input
  name="code"
  pattern="[A-Z]{3}-\d{3}"
  title="Three uppercase letters, hyphen, three digits (e.g. ABC-123)"
>
```

**Medium — date**

```html
<label for="due">Due date</label>
<input id="due" name="due" type="date" required>
```

#### Quick checks

1. Can users bypass client-side validation?
2. What attribute gives a regex?
3. Why include `title` or visible text with `pattern`?

---

## GET vs POST (conceptual)

### What it is

- **GET:** parameters in URL query string; safe/idempotent reads; cacheable; bookmarkable.
- **POST:** body carries fields; used for writes, uploads, sensitive payloads (still not “secure” by itself—HTTPS matters).

#### Why it exists / why it matters

Using GET for password submission appears in server logs, browser history, and referrer headers—**unacceptable**.

#### Pros and cons

- **Pros:** GET is great for search/filter UX with shareable URLs.
- **Cons:** GET length limits are implementation-dependent—avoid huge payloads.

#### What happens without it / when misused

- Passwords in query strings; accidental caching of private data.

#### Syntax and rules

```html
<form method="get" action="#">
  <!-- fields become ?a=1&b=2 on submit in real servers -->
</form>
```

#### Examples

**Tiny — filter**

```html
<form method="get" action="#">
  <label for="tag">Tag</label>
  <input id="tag" name="tag" type="text">
  <button type="submit">Filter</button>
</form>
```

**Tiny — feedback**

```html
<form method="post" action="#">
  <label for="msg">Message</label>
  <textarea id="msg" name="message" required></textarea>
  <button type="submit">Send</button>
</form>
```

**Medium — conceptual**

| Scenario | Prefer |
|----------|--------|
| Search | GET |
| Login (still needs HTTPS + server) | POST |
| File upload | POST (`enctype="multipart/form-data"`) |

#### Quick checks

1. Which method should never carry secrets in the query string?
2. Why are GET forms bookmark-friendly?
3. Name one downside of POST for a pure read-only filter UI.

---

## Common mistakes & debugging

- Missing `id`/`for` pairs—clicking label should focus input.
- Submit buttons outside `<form>` without `form` attribute (HTML feature)—avoid confusion in early labs by keeping buttons inside.
- `name` missing on fields—nothing useful submits.

---

## Further reading

- [MDN — Forms guide](https://developer.mozilla.org/en-US/docs/Learn/Forms)
- [MDN — `<input>` types](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input)
- [MDN — `method` attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form#method)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Control** | Input element users interact with. |
| **Successful controls** | Named controls eligible for submission per HTML rules. |

---

## Answers (self-test)

**Form**

1. `get`.
2. Avoid leaking classroom drafts to unknown endpoints; use `#` or instructor-provided test URL.
3. HTML allows case-insensitive ASCII; convention is lowercase `get`/`post`.

**Labels**

1. `for`/`id` pairing; wrap control inside `<label>`.
2. Placeholder disappears; not always exposed as accessible name alone.
3. `<legend>`.

**Controls**

1. Often `submit` inside forms—**explicitly set** `type="button"` when not submitting.
2. `<textarea>`.
3. `name`.

**Validation**

1. Yes (DevTools, custom fetch, modified HTML).
2. `pattern`.
3. Users need human-readable constraints; regex errors alone are cryptic.

**GET vs POST**

1. Neither should put secrets in query strings; GET is especially visible—POST still requires HTTPS.
2. Query string encodes values in URL.
3. Not bookmarkable/filter URLs are harder to share—POST repeats need re-submit confirmations.
