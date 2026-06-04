# Day 36 — Composition & Children

**Primary theme:** `props.children`, layout shells, decomposition, lifting state to coordinate siblings  
**Estimated study time:** 2–3 hours theory + 4–8 hours tasks  
**Related tasks:** `task-01-page-shell-children`, `task-02-post-card-children`, `task-03-lifted-filter-state`, `task-04-dashboard-three-slot-layout`  
**Instruction alignment:** Maps to *Composition & children* (Day 36).

---

## Overview

Composition is how you scale React: **small pieces** combine into pages without inheritance trees. The special prop **`children`** (and explicit “slot” props holding elements) let containers own layout while leaves own content. When two siblings must reflect the same changing value—like a search field and a filtered list—you **lift state** to their parent and pass props down.

---

## Day roadmap

1. [What composition is](#what-composition-is)
2. [`children` and layout shells](#children-and-layout-shells)
3. [Explicit slots vs `children`](#explicit-slots-vs-children)
4. [Lifting state](#lifting-state)
5. [Common mistakes & debugging](#common-mistakes--debugging)
6. [Further reading](#further-reading)
7. [Glossary](#glossary)
8. [Answers (self-test)](#answers-self-test)

---

## What composition is

### What it is

**Composition** means building components by nesting them: `<Page><Header/><Main/></Page>` rather than inheriting UI from a mega base class.

#### Why it exists / why it matters

It matches how design systems ship: tokens + primitives + recipes.

#### Pros and cons

- **Pros:** flexibility; avoids fragile inheritance.
- **Cons:** prop drilling if every layer must forward props (later mitigations exist).

#### Examples

**Tiny**

```jsx
<Card>
  <CardTitle>Hello</CardTitle>
</Card>
```

#### Quick checks

1. Why is composition preferred over deep class inheritance for UI?

---

## `children` and layout shells

### What it is

`children` is the elements between a component’s opening/closing tags.

#### Syntax and rules

```jsx
function Shell({ title, children }) {
  return (
    <div>
      <h1>{title}</h1>
      <main>{children}</main>
    </div>
  )
}
```

#### Quick checks

1. Can a component accept both `children` and other props?

---

## Explicit slots vs `children`

### What it is

Sometimes you want **named regions**: `left`, `main`, `right` props each holding a React node.

#### Why it matters

Avoids ambiguous ordering when multiple distinct regions are required.

#### Quick checks

1. When are explicit slot props clearer than nested `children` alone?

---

## Lifting state

### What it is

Move state to the **lowest common ancestor** of components that must read/write it together.

#### Examples

**Tiny**

```jsx
function Parent() {
  const [q, setQ] = useState('')
  return (
    <>
      <SearchBar value={q} onChange={setQ} />
      <Results query={q} />
    </>
  )
}
```

#### Quick checks

1. If two sibling components both need `count`, where should `useState` live?

---

## Common mistakes & debugging

- Putting unrelated state deep in a leaf when a sibling also needs it—lift instead.
- Rendering `children` twice accidentally (duplicated portals/lists).

---

## Further reading

- React docs: [Passing JSX as children](https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children), [Sharing state between components](https://react.dev/learn/sharing-state-between-components)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Composition** | Building UIs by nesting components |
| **`children`** | Slot content between tags |
| **Lifted state** | State moved up to coordinate siblings |

---

## Answers (self-test)

1. Composition is flexible and avoids rigid inheritance coupling.
2. Yes—`children` is just another prop with special JSX syntax.
3. When regions are distinct and order/clarity matters (nav vs body vs side panels).
4. In their parent (or higher), then pass props down.
