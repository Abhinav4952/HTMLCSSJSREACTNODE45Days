import Badge from './components/Badge.jsx'

export default function App() {
  return (
    <main>
      <h1>Badge lab</h1>
      <p>
        <Badge label="Build passing" variant="success" icon="✓" />
      </p>
      <p>
        <Badge label="Needs review" variant="warn" />
      </p>
      <p>
        <Badge label="CI" variant="info" />
      </p>
    </main>
  )
}
