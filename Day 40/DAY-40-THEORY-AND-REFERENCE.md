# Day 40 — Redux Side Effects + Integration

**Primary theme:** Async updates with **`createAsyncThunk`**; **`extraReducers`**; error/loading UX; a small **multi-fetch integration**  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Related tasks:** `task-01-fetch-posts-thunk`, `task-02-profile-thunk-rejection`, `task-03-delayed-submit-order-thunk`, `task-04-post-detail-integration`  
**Instruction alignment:** Maps to *Redux side effects + integration* (Day 40). This course uses **RTK `createAsyncThunk`** (not legacy handwritten middleware) for async.

---

## Overview

Reducers must stay **fast and pure**; **`fetch`** does not belong inside a reducer. RTK’s **`createAsyncThunk`** dispatches **lifecycle actions** (`pending`, `fulfilled`, `rejected`) that you handle in **`extraReducers`** to update `status`, `error`, and cached domain data. Day 40 practices the most common production pattern: explicit **loading** and **failure** UI, then a slightly larger **integration** read that coordinates two HTTP calls behind one thunk.

---

## Day roadmap

1. [Why async is not “just dispatch in a reducer”](#why-async-is-not-just-dispatch-in-a-reducer)
2. [`createAsyncThunk` lifecycle](#createasyncthunk-lifecycle)
3. [Modeling `status` + `error` in slice state](#modeling-status--error-in-slice-state)
4. [`rejectWithValue` for structured errors](#rejectwithvalue-for-structured-errors)
5. [Integration thunks (parallel requests)](#integration-thunks-parallel-requests)
6. [Common mistakes & debugging](#common-mistakes--debugging)
7. [Further reading](#further-reading)
8. [Glossary](#glossary)
9. [Answers (self-test)](#answers-self-test)

---

## Why async is not “just dispatch in a reducer”

### What it is

Reducers should compute the next state synchronously from an action. Network latency and failures don’t fit that model cleanly.

#### Why it matters

Side effects in reducers break DevTools replay and make cancellation/navigation races harder to reason about.

#### Quick checks

1. Where should `fetch` live for RTK apps in this course?

---

## `createAsyncThunk` lifecycle

### What it is

`createAsyncThunk(typePrefix, async (arg, thunkAPI) => result)` auto-dispatches `pending`/`fulfilled`/`rejected` actions.

#### Quick checks

1. Which builder API is commonly used to listen to thunk actions in a slice?

---

## Modeling `status` + `error` in slice state

### What it is

A common pattern is `status: 'idle' | 'loading' | 'succeeded' | 'failed'` plus `error: string | null` (or structured error objects).

#### Quick checks

1. When should you reset `error` to `null`?

---

## `rejectWithValue` for structured errors

### What it is

Inside a thunk payload creator, return `rejectWithValue(details)` to attach a serializable error payload for reducers.

#### Quick checks

1. Why prefer serializable error shapes?

---

## Integration thunks (parallel requests)

### What it is

One thunk can **`await Promise.all([...])`** to fetch multiple resources that should commit to state together (or handle partial failures—pick a policy).

#### Quick checks

1. What is one risk of two sequential `await` fetches if the first succeeds and the second fails?

---

## Common mistakes & debugging

- Forgetting to handle **`pending`** (UI never shows loading).
- Treating **`action.payload`** vs **`action.error.message`** inconsistently between `rejectWithValue` and thrown errors.
- Double-fetch surprises in React **`StrictMode`** during development—use intentional triggers (buttons) in labs.

---

## Further reading

- RTK: [`createAsyncThunk`](https://redux-toolkit.js.org/api/createAsyncThunk)
- RTK: [`createSlice` extraReducers](https://redux-toolkit.js.org/api/createSlice#the-extrareducers-builder-callback-notation)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Thunk** | Async logic that can dispatch actions (here: `createAsyncThunk`) |
| **`extraReducers`** | Slice listens to external actions (including thunk lifecycles) |
| **`rejectWithValue`** | Attach structured failure info to `rejected` actions |

---

## Answers (self-test)

1. In thunks/listeners/effects—not reducers.
2. `extraReducers` with `builder.addCase(...)` (or `addMatcher`).
3. On new attempts (`pending`) and on success (`fulfilled`).
4. DevTools and logging remain useful; fewer surprises across environments.
5. You may need a cleanup policy (partial success) depending on product requirements.
