import { useSelector } from 'react-redux'
import Counter from './components/Counter.jsx'
import ThemeToggle from './components/ThemeToggle.jsx'

export default function App() {
  const mode = useSelector((state) => state.theme.mode)

  return (
    <div data-theme={mode} className="app-root">
      <main>
        <h1>Combined slices lab</h1>
        <p>The counter slice is complete. Implement the theme slice so the toggle flips the page chrome.</p>
        <ThemeToggle />
        <Counter />
      </main>
    </div>
  )
}
