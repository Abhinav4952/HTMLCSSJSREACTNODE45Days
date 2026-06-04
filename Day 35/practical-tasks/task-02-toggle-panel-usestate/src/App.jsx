import DisclosurePanel from './components/DisclosurePanel.jsx'

export default function App() {
  return (
    <main>
      <h1>Release notes</h1>
      <DisclosurePanel title="Day 35 — state basics">
        <p>
          Panels like this hide verbose content until the reader opts in. Your job is to make the toggle
          feel instant and predictable.
        </p>
      </DisclosurePanel>
    </main>
  )
}
