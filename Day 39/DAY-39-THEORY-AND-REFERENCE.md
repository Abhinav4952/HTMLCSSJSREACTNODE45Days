# Day 39 — Redux Core (Redux Toolkit)

**Primary theme:** Global **store**, **actions**, **reducers**, **immutability**, composing feature state with **slices**  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Related tasks:** `task-01-counter-slice-actions`, `task-02-theme-and-counter-combined`, `task-03-todo-list-redux`, `task-04-cart-selectors-total`  
**Instruction alignment:** Maps to *Redux core* (Day 39). This repository standardizes on **Redux Toolkit (RTK)** + **`react-redux`** for Days **39–40**.

---

## Overview

Local component state is perfect for UI that is owned by one subtree. **Redux** (with **RTK** today) shines when **many distant components** must read/write the same logical state, when you want **predictable update rules**, time-travel debugging, or middleware-heavy workflows. The tradeoff is **ceremony**: you describe updates as **events** (**actions**) handled by **pure reducers** that return the next state.

Redux Toolkit is the official, opinionated way to write modern Redux: less boilerplate, built-in **Immer** for “mutative-looking” reducer logic that remains safe, and utilities for async on Day 40.

---

## Day roadmap

1. [Why a store exists](#why-a-store-exists)
2. [Actions and reducers (pure updates)](#actions-and-reducers-pure-updates)
3. [`createSlice` in Redux Toolkit](#createslice-in-redux-toolkit)
4. [`configureStore` and multiple slices](#configurestore-and-multiple-slices)
5. [Connecting React: `Provider`, `useSelector`, `useDispatch`](#connecting-react-provider-useselector-usedispatch)
6. [Selectors and derived data](#selectors-and-derived-data)
7. [Redux DevTools (optional)](#redux-devtools-optional)
8. [Common mistakes & debugging](#common-mistakes--debugging)
9. [Further reading](#further-reading)
10. [Glossary](#glossary)
11. [Answers (self-test)](#answers-self-test)

---

## Why a store exists

### What it is

A **store** holds your app’s **global state tree** and exposes **`dispatch(action)`** to request updates.

#### Why it exists / why it matters

Prop drilling and ad-hoc context providers can sprawl. A store gives a **single write funnel** (`dispatch`) and a **single read API** (`getState` / selectors).

#### Pros and cons

- **Pros:** centralization; testable reducers; DevTools; middleware.
- **Cons:** boilerplate vs `useState`; risk of “everything global” anti-pattern.

#### What happens without it / when misused

Duplicated sources of truth (server cache in three places) cause inconsistent UI.

#### Quick checks

1. Name one symptom of putting **all** UI state in Redux unnecessarily.

---

## Actions and reducers (pure updates)

### What it is

An **action** is a plain object describing **what happened** (conventionally `type` + `payload`). A **reducer** is `(state, action) => newState` (RTK + Immer relaxes the “return newState” ergonomics but **logic must stay predictable**).

#### Why it exists / why it matters

Predictable updates simplify debugging: log actions, replay them, test reducers in isolation.

#### Pros and cons

- **Pros:** easy to unit test pure reducers.
- **Cons:** async is not Redux’s core—Day 40 adds **thunks** (`createAsyncThunk`).

#### What happens without it / when misused

**Mutating** `state` in classic Redux breaks time travel and subtle invariants. RTK + Immer helps, but you should still treat updates as intentional.

#### Quick checks

1. Should reducers perform `fetch` calls?

---

## `createSlice` in Redux Toolkit

### What it is

`createSlice({ name, initialState, reducers })` generates **action creators** and a **reducer** for one feature (“slice”).

#### Syntax and rules

```js
import { createSlice } from '@reduxjs/toolkit'

const slice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => {
      state.value += 1
    },
  },
})

export const { increment } = slice.actions
export default slice.reducer
```

#### Quick checks

1. What does Immer enable you to write inside a RTK reducer?

---

## `configureStore` and multiple slices

### What it is

`configureStore({ reducer: { featureA: aReducer, featureB: bReducer }})` combines slices into one tree (`state.featureA`, `state.featureB`).

#### Quick checks

1. Where do slice names appear in the default action `type` strings?

---

## Connecting React: `Provider`, `useSelector`, `useDispatch`

### What it is

`<Provider store={store}>` makes the store available. `useSelector` reads state; `useDispatch` returns `dispatch`.

#### Quick checks

1. Why wrap the app (or subtree) in `Provider` exactly once at the root in these tasks?

---

## Selectors and derived data

### What it is

A **selector** is a function `(state) => derivedValue`. RTK re-exports `createSelector` from Reselect for memoized derived values (e.g. cart totals).

#### Quick checks

1. When is memoization most valuable for selectors?

---

## Redux DevTools (optional)

`configureStore` enables DevTools integration in development builds by default in typical setups. Use DevTools to inspect **action history** and **state diffs**.

---

## Common mistakes & debugging

- Putting non-serializable values (functions, class instances) into state without discipline.
- Deriving expensive values inline in every render instead of memoized selectors when needed.
- Dispatching the wrong action shape—prefer generated action creators from slices.

---

## Further reading

- Redux Toolkit: [Getting Started](https://redux-toolkit.js.org/introduction/getting-started)
- Redux style guide: [Redux Essentials](https://redux.js.org/tutorials/essentials/part-1-overview-concepts)
- React Redux: [`Provider`, hooks](https://react-redux.js.org/api/hooks)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Store** | Holds global state; supports `dispatch` / `getState` |
| **Action** | Event object describing an update |
| **Reducer** | Pure function computing next state |
| **Slice** | Feature bundle: state + reducers + actions (RTK) |
| **Selector** | Reads or derives view-model data from state |

---

## Answers (self-test)

1. Extra rerenders, needless coupling, harder local encapsulation.
2. No—async belongs in middleware/thunks/listeners (Day 40).
3. “Mutative” updates that Immer records as immutable snapshots.
4. Typically `name/actionName`, e.g. `counter/increment`.
5. So all hooks resolve to the same store instance.
6. When derivation is costly or reference stability avoids child rerenders.
