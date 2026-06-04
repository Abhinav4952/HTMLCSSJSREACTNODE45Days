# Day 34 — React Components & Props

**Primary theme:** Building UI from reusable pieces; passing data with props; function vs class components; PropTypes for development-time contracts  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Related tasks:** `task-01-function-greeting-props`, `task-02-badge-proptypes`, `task-03-class-welcome-banner`, `task-04-dashboard-cards-mixed`  
**Instruction alignment:** Maps to *React components & props* from the master topic list (Day 34).

---

## Overview

React helps you build interactive UIs by **splitting screens into components**: independent, reusable pieces that receive **inputs (props)** and return **descriptions of UI (JSX)**. On Day 34 you focus on the **read model**: given stable props, your component renders predictable markup. You will see both **function components** (the modern default) and **class components** (still common in older apps and useful for mental models that connect to lifecycle on Day 35).

This day intentionally avoids client-side **state** (Day 35) and routers/state libraries so you can solidify **composition** and **prop discipline** first.

---

## Day roadmap

1. [Why React: UI as a function of data](#why-react-ui-as-a-function-of-data)
2. [JSX and the automatic runtime](#jsx-and-the-automatic-runtime)
3. [Function components and props](#function-components-and-props)
4. [Class components (read-only render path)](#class-components-read-only-render-path)
5. [PropTypes and default values](#proptypes-and-default-values)
6. [Common mistakes & debugging](#common-mistakes--debugging)
7. [Further reading](#further-reading)
8. [Glossary](#glossary)
9. [Answers (self-test)](#answers-self-test)

---

## Why React: UI as a function of data

### What it is

A **component** is a reusable unit that returns UI. For many teams, the core habit is: **UI = f(data)** where `data` includes props (and later state, context, and server data).

#### Why it exists / why it matters

Large apps change constantly. Without components, copy-paste markup drifts; a single “button style” update becomes a repo-wide archaeology project. Components localize change.

#### Pros and cons

- **Pros:** reuse; testable boundaries; encourages consistent patterns.
- **Cons:** indirection (many small files); prop drilling (addressed later with composition/context/Redux as appropriate).

#### What happens without it / when misused

Monolithic templates with hidden globals become impossible to reason about under concurrency and feature flags.

#### Syntax and rules

- Prefer **pure** presentational components: given the same props, return the same tree (until you introduce intentional side effects with hooks—later days).

#### Examples

**Tiny — mental model**

```txt
props -> component -> JSX -> (React reconciles to DOM)
```

**Tiny — pseudo-code**

```js
function PriceTag({ currency, amount }) {
  return <span>{currency} {amount.toFixed(2)}</span>
}
```

#### Quick checks

1. If props change, what part of your code should react first: the parent or the child?
2. Name one reason small components beat one giant `renderPage()` function.

---

## JSX and the automatic runtime

### What it is

**JSX** is syntactic sugar for `React.createElement` calls (or the modern equivalent via the automatic JSX runtime). With Vite + `@vitejs/plugin-react`, you typically **do not** need `import React from 'react'` in every file.

#### Why it exists / why it matters

JSX keeps UI structure visually similar to HTML while staying JavaScript-expressive (map lists, conditionals, call functions).

#### Pros and cons

- **Pros:** readable trees; tooling can lint a11y and types (if TypeScript).
- **Cons:** `className` vs `class`, `htmlFor` vs `for`—HTML attribute mismatches trip beginners.

#### What happens without it / when misused

Wrong file extension (`*.js` without JSX config) or missing plugin configuration can cause parse errors at build time.

#### Syntax and rules

- One root parent per return (or use fragments `<>...</>`).
- Always close tags: `<img />`, `<br />`.
- JavaScript expressions use `{}`.

#### Examples

**Tiny**

```jsx
export default function App() {
  const title = 'Day 34'
  return <h1>{title}</h1>
}
```

**Tiny — fragment**

```jsx
return (
  <>
    <h1>Title</h1>
    <p>Body</p>
  </>
)
```

**Medium — conditional**

```jsx
function Notice({ message, isError }) {
  if (!message) return null
  return <p role={isError ? 'alert' : undefined}>{message}</p>
}
```

#### Quick checks

1. When do you use `className` instead of `class` in React?
2. What does `return null` mean for the rendered output?

---

## Function components and props

### What it is

A **function component** is a function named like a component (`PascalCase`) that accepts a **props object** and returns JSX.

#### Why it exists / why it matters

Props are the primary way parents configure children: labels, URLs, feature toggles, and rendered variants—without global variables.

#### Pros and cons

- **Pros:** simple mental model; easy to colocate styles and markup; works naturally with hooks later.
- **Cons:** destructuring defaults can hide “required prop” mistakes unless you add PropTypes/TypeScript/tests.

#### What happens without it / when misused

**Mutating props** (e.g. `props.items.push(x)`) creates cross-component bugs and breaks React’s change-detection assumptions.

#### Syntax and rules

```jsx
function Avatar({ src, alt, size = 40 }) {
  return <img width={size} height={size} src={src} alt={alt} />
}
```

**Gotcha:** `children` is just another prop—explicitly accept it when you wrap content.

#### Examples

**Tiny — spread carefully**

```jsx
function Button({ label, ...rest }) {
  return <button type="button" {...rest}>{label}</button>
}
```

**Tiny — lists (preview)**

```jsx
<ul>
  {items.map((item) => (
    <li key={item.id}>{item.label}</li>
  ))}
</ul>
```

**Medium — composition preview**

```jsx
function Page({ header, children }) {
  return (
    <div>
      {header}
      <main>{children}</main>
    </div>
  )
}
```

#### Quick checks

1. Are props mutable if you assign `props.x = 1`?
2. Why should list items usually have a `key`?

---

## Class components (read-only render path)

### What it is

A **class component** extends `React.Component` (or `PureComponent`) and implements at least `render()` that returns JSX. Props are available as `this.props`.

#### Why it exists / why it matters

Many production codebases still contain class components. Reading them—and migrating them thoughtfully—is a real skill. Day 35 connects classes to lifecycle; today focus on **rendering from props**.

#### Pros and cons

- **Pros:** explicit instance model; familiar to OOP-trained developers; legacy interoperability.
- **Cons:** more boilerplate than functions; hooks do not work inside classes.

#### What happens without it / when misused

Calling `this.props.foo = 'bar'` is still mutation—never do this.

#### Syntax and rules

```jsx
import { Component } from 'react'

export default class Hello extends Component {
  render() {
    const { name } = this.props
    return <p>Hello, {name}</p>
  }
}
```

#### Examples

**Tiny**

```jsx
class ClockFace extends Component {
  render() {
    return <span>{this.props.timeLabel}</span>
  }
}
```

**Medium — default-ish behavior via render logic**

```jsx
class Banner extends Component {
  render() {
    const title = this.props.title ?? 'Untitled'
    return <header><h1>{title}</h1></header>
  }
}
```

#### Quick checks

1. Where do class components read incoming configuration from?
2. Which hook-centric patterns are **not** available inside a class `render()`?

---

## PropTypes and default values

### What it is

**`prop-types`** is a runtime type-checking package for props (development aid). It does **not** replace TypeScript for large teams, but it is lightweight for JS-first courses.

#### Why it exists / why it matters

Misspelled prop names and wrong shapes are among the fastest ways to waste an afternoon. PropTypes surfaces many mistakes in the console during development.

#### Pros and cons

- **Pros:** incremental adoption; readable schemas at the component boundary.
- **Cons:** runtime cost in dev; no static guarantees in CI unless you add other tools.

#### What happens without it / when misused

Overly loose `PropTypes.any` defeats the purpose; treat `any` as a last resort.

#### Syntax and rules

```jsx
import PropTypes from 'prop-types'

function Score({ value }) {
  return <output>{value}</output>
}

Score.propTypes = {
  value: PropTypes.number.isRequired,
}
```

**Note:** `defaultProps` on function components is **deprecated** in newer React docs patterns; prefer default parameters in the function signature.

#### Examples

**Tiny — oneOf**

```jsx
Row.propTypes = {
  variant: PropTypes.oneOf(['compact', 'comfortable']),
}
```

**Tiny — arrayOf**

```jsx
List.propTypes = {
  tags: PropTypes.arrayOf(PropTypes.string),
}
```

**Medium — shape**

```jsx
Card.propTypes = {
  author: PropTypes.shape({
    name: PropTypes.string.isRequired,
    handle: PropTypes.string,
  }).isRequired,
}
```

#### Quick checks

1. When do PropType warnings appear: in production builds or primarily in development?
2. Name one prop type you would mark `isRequired` for a primary heading component.

---

## Common mistakes & debugging

- **Mutating props or props nested objects** — treat props as frozen; clone/update in state later (Day 35).
- **Wrong component name casing** — components must be `PascalCase`; `userRow` vs `UserRow` changes meaning.
- **Missing `key` in lists** — console warnings; worse bugs on Day 38 when stateful inputs reorder.
- **Assuming PropTypes runs in production** — do not rely on it as a security boundary.
- **Forgetting `type="button"`** on buttons inside forms (Day 37 goes deeper).

---

## Further reading

- React docs (latest): [Describing the UI](https://react.dev/learn/describing-the-ui), [Passing Props](https://react.dev/learn/passing-props-to-a-component)
- MDN: [Introducing JSX (legacy guide area)](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Client-side_JavaScript_frameworks/React_getting_started) — skim alongside official React docs
- `prop-types` package README: [https://www.npmjs.com/package/prop-types](https://www.npmjs.com/package/prop-types)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Component** | Reusable UI unit returning JSX |
| **Props** | External inputs to a component (parent → child) |
| **JSX** | JS syntax extension for UI trees |
| **Reconciliation** | React’s process of matching UI updates (deepened Day 38) |
| **PropTypes** | Development-time prop validators |

---

## Answers (self-test)

1. The child re-renders when the parent passes new props; the child should not “pull” props from globals.
2. Small components localize changes, enable reuse, and simplify testing/review.
3. Use `className` in React DOM.
4. `return null` renders nothing for that component subtree.
5. Props should be treated as immutable; mutation breaks invariants.
6. Keys help React identify which list item is which across updates.
7. Class components read `this.props`.
8. Hooks cannot be used in class `render()`; use class lifecycle methods or convert to functions.
9. Primarily development; production may strip or reduce warnings depending on tooling.
10. `title` or `children` depending on design—anything required for accessible output.
