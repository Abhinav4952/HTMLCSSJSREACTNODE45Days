# Task 4 — `useEffect` + `localStorage` theme

## Summary

Persist a **`light` / `dark`** theme using **`localStorage`**. You will synchronize browser storage with React state using **`useEffect`**, being careful about **first render** vs **hydration from storage**.

## Learning goals

- Run **one-time initialization** logic safely.
- Persist derived UI preferences to **`localStorage`**.
- Ignore invalid stored values.

## Provided files

- `src/components/ThemeShell.jsx` — edit surface.
- `src/index.css` — `shell--light` / `shell--dark` styles.

## Prerequisites

- Day 35 theory: effects + cleanup mindset (no network here).

## What you will implement

1. On first load, read **`day35-task04-theme`** from `localStorage` (`STORAGE_KEY` constant already defined).
2. If stored value is **`light`** or **`dark`**, use it; otherwise default **`light`**.
3. Whenever **`theme`** changes (including after reading storage), persist with **`localStorage.setItem`**.

## Constraints

- Only edit files with `TODO(Day35-task04)`.
- Do not add Redux/router.

## Step-by-step guidance

1. Add `useEffect` import.
2. Decide whether initial read uses lazy `useState(() => ...)` **or** `useEffect` on mount—avoid double-setting loops.
3. Toggle button already flips theme; ensure persistence catches those updates.

## How to run and verify

```bash
cd "Day 35/practical-tasks/task-04-effect-theme-localstorage"
npm install
npm run dev
```

Optional:

```bash
npm run build
```

### Manual checks

- [ ] Toggle theme → reload page → theme restores.
- [ ] Manually set `localStorage` to garbage in DevTools → reload → app defaults to `light` without crashing.

## `TODO` map

| `ThemeShell.jsx` | Done means |
|------------------|------------|
| `useEffect` / initializer | Read + validate storage; persist updates. |

## Submission checklist (Git)

- [ ] No secrets in repo.

## Hints

<details>
<summary>Avoid infinite loops</summary>

An effect that sets state on every render without a dependency guard will loop. Tie writes to `[theme]` or use a lazy initializer for the read path.

</details>
