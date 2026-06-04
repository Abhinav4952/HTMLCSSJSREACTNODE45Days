# Task 1 — Function greeting with props

## Summary

You will implement a small **function component** that greets a user based on **`name`** and an optional **`role`** prop. The app already renders two sample rows from `App.jsx`; your job is to make `UserGreeting` read props correctly with sensible defaults.

## Learning goals

- Accept props in a function component using destructuring.
- Provide **default values** for missing props at the function boundary.
- Keep JSX readable and avoid mutating props.

## Provided files

- `package.json`, `vite.config.js`, `.npmrc`, `index.html` — Vite + React 18 starter (automatic JSX runtime).
- `src/main.jsx` — mounts `<App />` (do not change unless your instructor says so).
- `src/App.jsx` — passes example props to `UserGreeting` (reference usage).
- `src/components/UserGreeting.jsx` — **your primary edit surface** (contains `TODO`s).
- `src/index.css` — baseline styles.

## Prerequisites

- Day 34 theory sections on function components and JSX.

## What you will implement

1. `UserGreeting` accepts `name` and optional `role`.
2. When `name` is missing, show **Hello, guest**.
3. When `role` is present, show **Hello, &lt;name&gt; (&lt;role&gt;)** (for missing `name`, still apply the guest default before adding role).
4. Do not change the prop names used in `App.jsx`.

## Constraints

- Edit only files that contain `TODO(Day34-task01)` unless your instructor allows broader changes.
- Do **not** add Redux, React Router, or UI kits.
- Use **JavaScript + JSX** with the automatic JSX runtime (**no** `import React from 'react'` required in every file).

## Step-by-step guidance

1. Open `src/components/UserGreeting.jsx` and add destructured parameters to the function signature.
2. Choose defaults (`name` defaulting to `guest` display logic, etc.).
3. Format the final string with a single `<p>` (or similar) element.
4. Reload the dev server page and confirm both `<UserGreeting />` rows match the rubric.

## How to run and verify

### Install dependencies

From the repository root:

```bash
cd "Day 34/practical-tasks/task-01-function-greeting-props"
npm install
```

### Run the app (React / Vite)

```bash
npm run dev
```

Visit the URL Vite prints (usually `http://localhost:5173`).

### Optional production bundle check

```bash
npm run build
npm run preview
```

### Manual checks (all tasks)

- [ ] Dev server starts with **no** import or syntax errors before you solve TODOs (starter should already run).
- [ ] With `name="Avery"` and `role="student"`, output reads like: **Hello, Avery (student)** (exact punctuation flexible if rubric passes).
- [ ] With only `name="Jordan"`, output reads like: **Hello, Jordan** (no empty parentheses).
- [ ] `npm run build` completes without errors after your changes.

## `TODO` map

| Location | Done means |
|----------|------------|
| `UserGreeting.jsx` — parameter list | Props are accepted (`name`, optional `role`). |
| `UserGreeting.jsx` — greeting line | Correct string rules for defaults and optional role. |

## Submission checklist (Git)

- [ ] Only intentional files changed (typically `UserGreeting.jsx` only).
- [ ] No secrets committed.
- [ ] `npm run dev` shows the expected strings.

## Hints (optional)

<details>
<summary>Defaulting `name`</summary>

Default parameters in the function signature are usually clearer than branching everywhere: `function UserGreeting({ name = 'guest', role } = {})`.

Remember the displayed word should be **guest** when absent, not necessarily the literal prop value.

</details>
