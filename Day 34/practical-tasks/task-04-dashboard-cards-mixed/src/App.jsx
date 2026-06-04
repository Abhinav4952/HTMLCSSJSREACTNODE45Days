import MetricCard from './components/MetricCard.jsx'
import TeamNote from './components/TeamNote.jsx'

export default function App() {
  return (
    <main className="dashboard">
      <h1>Team pulse</h1>
      {/* TODO(Day34-task04): Wrap the three components below in a single parent <div className="grid"> so the CSS grid layout applies. */}
      <MetricCard title="Commits (7d)" value="128" />
      <MetricCard title="Open PRs" value="3" />
      <TeamNote author="Sam" body="Please review the accessibility checklist before Friday." />
    </main>
  )
}
