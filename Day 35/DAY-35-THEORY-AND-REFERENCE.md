# Day 35 — React State & Lifecycle

**Primary theme:** Local UI state with `useState`; side effects with `useEffect`; class lifecycle methods as the historical mirror (`componentDidMount` / `componentWillUnmount`)  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Related tasks:** `task-01-hooks-counter-usestate`, `task-02-toggle-panel-usestate`, `task-03-class-timer-lifecycle`, `task-04-effect-theme-localstorage`  
**Instruction alignment:** Maps to *State & lifecycle* (Day 35). Lifecycle **deepening** with reconciliation/keys returns on **Day 38** per course map notes.

---

## Overview

On Day 34, UI was mostly a function of **props**. Real interfaces also need **memory** that belongs to a component subtree: open/closed panels, counters, field values before submit, timers, and transient “loading” flags. In modern React, **`useState`** and **`useEffect`** express most component-local patterns. You will still see **`this.state` / `setState`** and lifecycle methods in older code—so this day gives you both **hooks-first skills** and a **class-shaped mental model** that matches how engineers discuss mount/unmount behavior in code review.

---

## Day roadmap

1. [What “state” means in React](#what-state-means-in-react)
2. [`useState` in function components](#usestate-in-function-components)
3. [Effects: `useEffect` and cleanup](#effects-useeffect-and-cleanup)
4. [Class components: `setState` + lifecycle mirrors](#class-components-setstate--lifecycle-mirrors)
5. [Common mistakes & debugging](#common-mistakes--debugging)
6. [Further reading](#further-reading)
7. [Glossary](#glossary)
8. [Answers (self-test)](#answers-self-test)

---

## What “state” means in React

### What it is

**State** is data that can change over time and should trigger UI updates when it changes. Unlike props (owned by the parent), local state is **owned by the component** (or lifted to an ancestor when multiple siblings need it—Day 36).

#### Why it exists / why it matters

Interactivity is literally “the UI changes when something changes.” React batches updates and reconciles output efficiently (Day 38).

#### Pros and cons

- **Pros:** colocated logic; predictable rerenders when you follow rules of hooks.
- **Cons:** too much local state makes sharing hard—plan lifts early.

#### What happens without it / when misused

Deriving everything from `window` globals or mutating the DOM manually undermines React’s model and creates bugs.

#### Syntax and rules

- Prefer **immutable updates** for state values (especially objects/arrays): copy-then-change patterns.

#### Examples

**Tiny — immutability sketch**

```js
setItems((prev) => [...prev, newItem])
```

**Tiny — never mutate state**

```js
// bad: state.count++ ; setState(state)
```

#### Quick checks

1. Does changing props always require `useState` in the child?
2. Name one symptom of mutating an array you stored in React state.

---

## `useState` in function components

### What it is

`useState(initial)` returns `[value, setter]`. Calling the setter schedules a re-render with the new value.

#### Why it exists / why it matters

It is the simplest way to introduce memory into function components without classes.

#### Pros and cons

- **Pros:** ergonomic; works with TypeScript/PropTypes later.
- **Cons:** stale closures if you capture state incorrectly in async handlers (mitigate with functional updates).

#### What happens without it / when misused

Calling `useState` conditionally breaks hook ordering—React will error.

#### Syntax and rules

```jsx
const [open, setOpen] = useState(false)
```

**Gotcha:** functional updates `setCount(c => c + 1)` are safest inside intervals/timeouts.

#### Examples

**Tiny — toggle**

```jsx
<button type="button" onClick={() => setOpen((v) => !v)}>
  {open ? 'Close' : 'Open'}
</button>
```

**Tiny — counter**

```jsx
const [n, setN] = useState(0)
```

**Medium — controlled field preview (Day 37 expands)**

```jsx
const [text, setText] = useState('')
return <input value={text} onChange={(e) => setText(e.target.value)} />
```

#### Quick checks

1. Why must hooks be called unconditionally?
2. When should you prefer `setCount(c => c + 1)` over `setCount(count + 1)`?

---

## Effects: `useEffect` and cleanup

### What it is

`useEffect(() => { ... }, deps)` runs **after paint** (by default) to express side work: timers, subscriptions, logging, syncing to `localStorage`, fetching.

#### Why it exists / why it matters

Rendering should stay pure; effects isolate imperative world interactions.

#### Pros and cons

- **Pros:** explicit dependency list encourages correctness (with ESLint plugin in real teams).
- **Cons:** dependency arrays are easy to get subtly wrong without linting discipline.

#### What happens without it / when misused

Leaked intervals/subscriptions cause memory leaks and duplicate network calls.

#### Syntax and rules

```jsx
useEffect(() => {
  const id = window.setInterval(tick, 1000)
  return () => window.clearInterval(id)
}, [])
```

#### Examples

**Tiny — mount-only**

```jsx
useEffect(() => {
  console.info('mounted')
}, [])
```

**Tiny — on prop change**

```jsx
useEffect(() => {
  // run when userId changes
}, [userId])
```

#### Quick checks

1. What does returning a function from `useEffect` do?
2. What does an empty dependency array mean?

---

## Class components: `setState` + lifecycle mirrors

### What it is

Classes keep state in `this.state` and update via `this.setState(partialOrUpdater)`. Lifecycle methods like **`componentDidMount`** and **`componentWillUnmount`** bracket a component’s presence in the tree.

#### Why it exists / why it matters

You will read and maintain legacy code; you will also reason about “cleanup on unmount” even when writing hooks.

#### Pros and cons

- **Pros:** explicit lifecycle hooks for some patterns.
- **Cons:** more boilerplate; async `setState` merging can confuse beginners.

#### What happens without it / when misused

Forgetting to clear an interval in `componentWillUnmount` leaks timers.

#### Syntax and rules

```jsx
componentWillUnmount() {
  if (this.timerId) window.clearInterval(this.timerId)
}
```

#### Examples

**Tiny — setState**

```js
this.setState((prev) => ({ count: prev.count + 1 }))
```

#### Quick checks

1. Which lifecycle is the usual place to start a repeating timer in a class?
2. Where must that timer be cleared?

---

## Common mistakes & debugging

- **Stale state in async handlers** — use functional updates.
- **Missing effect cleanup** — duplicate intervals on StrictMode double-invoke in dev (learn the pattern anyway).
- **Deriving state you already have** — don’t store `fullName` if it is always `first + last` unless profiling demands memoization.
- **Using `useEffect` for everything** — many things are better as event handlers.

---

## Further reading

- React docs: [State: A Component’s Memory](https://react.dev/learn/state-a-components-memory), [Lifecycle of Reactive Effects](https://react.dev/learn/lifecycle-of-reactive-effects)
- React docs (reference): [`useState`](https://react.dev/reference/react/useState), [`useEffect`](https://react.dev/reference/react/useEffect)
- MDN: [`Window.localStorage`](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) (used carefully in Task 4)

---

## Glossary

| Term | Meaning |
|------|---------|
| **State** | Component-owned mutable data that triggers UI updates |
| **Effect** | Post-render side work (`useEffect`) |
| **Cleanup** | Function returned from an effect to undo subscriptions/timers |
| **`setState`** | Class API for scheduling state updates |

---

## Answers (self-test)

1. No—props drive rerenders from parent changes; local `useState` is for child-owned interactive memory.
2. UI may not update; React relies on immutability assumptions for change detection in practice.
3. Hooks rely on call order across renders; conditional calls break the association.
4. In async/timers, functional updates avoid stale captured values.
5. Cleanup runs before re-running the effect (if deps changed) and on unmount.
6. Run on mount and not re-run on ordinary rerenders (unless StrictMode dev behaviors).
7. `componentDidMount` (or constructor for some cases—prefer mount for browser APIs).
8. `componentWillUnmount` (or modern `componentWillUnmount` still used for cleanup in classes).
