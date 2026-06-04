# Day 37 — Forms in React

**Primary theme:** Controlled components; validation UX; checkboxes/radios; text areas with constraints  
**Estimated study time:** 2–3 hours theory + 4–8 hours tasks  
**Related tasks:** `task-01-controlled-email-field`, `task-02-signup-form-validate`, `task-03-preferences-checkboxes`, `task-04-textarea-bio-counter`  
**Instruction alignment:** Maps to *Forms in React* (Day 37).

---

## Overview

HTML forms post data to servers; React forms usually **intercept** input events, keep values in **state**, validate, then submit via `fetch` or a framework action. The controlled pattern (`value` + `onChange`) makes React the source of truth—great for instant validation, tricky if you fight the browser’s native behaviors without care.

---

## Day roadmap

1. [Controlled vs uncontrolled (focus: controlled)](#controlled-vs-uncontrolled-focus-controlled)
2. [Text inputs and textareas](#text-inputs-and-textareas)
3. [Checkboxes and radios](#checkboxes-and-radios)
4. [Validation UX patterns](#validation-ux-patterns)
5. [Common mistakes & debugging](#common-mistakes--debugging)
6. [Further reading](#further-reading)
7. [Glossary](#glossary)
8. [Answers (self-test)](#answers-self-test)

---

## Controlled vs uncontrolled (focus: controlled)

### What it is

A **controlled** input’s `value` comes from React state; updates go through `onChange`. An **uncontrolled** input keeps its own DOM state; React reads it via `ref` (less common in modern app forms).

#### Why it matters

Controlled inputs make derived UI (character counts, submit disabling) deterministic.

#### Pros and cons

- **Pros:** one source of truth; easy validation.
- **Cons:** more rerenders; must handle every keystroke path.

#### Quick checks

1. What two props are required for a basic controlled text field?

---

## Text inputs and textareas

### Syntax and rules

```jsx
<input value={email} onChange={(e) => setEmail(e.target.value)} />
```

Use `type="email"` when semantically appropriate; still validate in JS for UX.

#### Quick checks

1. Why is `defaultValue` usually avoided once you go controlled?

---

## Checkboxes and radios

### What it is

- Checkbox: boolean `checked` + `onChange` toggles.
- Radio group: several inputs share one piece of state (the selected `value`).

#### Quick checks

1. Do radio inputs each need a unique `name` attribute for native grouping?

---

## Validation UX patterns

### What it is

Show **inline errors** near fields, prefer `aria-invalid` and `aria-describedby` when you render error text IDs, and disable submit until requirements pass (or show explicit errors on submit—pick a consistent policy per task).

#### Quick checks

1. Why disable submit if the form is invalid?

---

## Common mistakes & debugging

- Forgetting `onChange` → React warns about switching controlled/uncontrolled.
- Using `value` without updating state → inputs appear “stuck”.
- Submit buttons defaulting to `submit` inside forms causing accidental reloads—use `type="button"` until you intentionally submit.

---

## Further reading

- React docs: [Forms](https://react.dev/reference/react-dom/components#form-related)
- MDN: [`<input>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input), [`<textarea>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Controlled input** | `value` driven by React state |
| **Validation UX** | Errors, focus management, disabled states |

---

## Answers (self-test)

1. `value` and `onChange` (for the minimal controlled text field pattern).
2. Mixing `defaultValue` with controlled `value` is a footgun—pick one model.
3. Radios should share a `name` for native grouping and accessibility tooling.
