import { useState } from 'react'
import { useEffect } from 'react'
const STORAGE_KEY = 'day35-task04-theme'

export default function ThemeShell() {
  const [theme, setTheme] = useState(()=>{
    const storedTheme = localStorage.getItem(STORAGE_KEY);
    return storedTheme==='light' || storedTheme==='right'? storedTheme : 'light';
  })
  useEffect(()=>{
    localStorage.setItem(STORAGE_KEY,theme);
  },[theme])
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
