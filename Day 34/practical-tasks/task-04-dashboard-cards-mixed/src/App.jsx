import MetricCard from './components/MetricCard.jsx'
import TeamNote from './components/TeamNote.jsx'

export default function App() {
  return (
    <main className="dashboard">
      <h1>Team pulse</h1>
      <div className="grid">
        <MetricCard title="Commits (7d)" value="128" />
        <MetricCard title="Open PRs" value="3" />
        <TeamNote author="Sam" body="Please review the accessibility checklist before Friday." />
      </div>
    </main>
  )
}
