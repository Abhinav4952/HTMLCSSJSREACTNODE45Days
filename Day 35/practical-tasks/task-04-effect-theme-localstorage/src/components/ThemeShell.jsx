import { useState } from 'react'

const STORAGE_KEY = 'day35-task04-theme'

// TODO(Day35-task04): Import `useEffect` from `react`.
// TODO(Day35-task04): On initial mount, read `localStorage.getItem(STORAGE_KEY)`.
//       If the stored value is exactly `'light'` or `'dark'`, use it as the initial theme via `useState(initializer)` **or** by setting state once in an effect (pick one approach—avoid infinite loops).
//       If missing/invalid, default to `'light'`.
// TODO(Day35-task04): Whenever `theme` changes after interactions, persist with `localStorage.setItem(STORAGE_KEY, theme)`.
//       Ensure this runs for user toggles (and also covers the initial load case if you hydrate from storage).
export default function ThemeShell() {
  const [theme, setTheme] = useState('light')

  return (
    <div className={`shell shell--${theme}`}>
      <header style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <h1 style={{ margin: 0, fontSize: '1.25rem' }}>Theme persistence lab</h1>
        <button type="button" onClick={() => setTheme((t) => (t === 'light' ? 'dark' : 'light'))}>
          Toggle theme
        </button>
      </header>
      <p>Current theme: {theme}</p>
      <p>After you finish, reloading the page should restore the last theme.</p>
    </div>
  )
}
