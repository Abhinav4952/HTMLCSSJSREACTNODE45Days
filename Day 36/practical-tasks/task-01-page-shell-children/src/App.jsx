import PageShell from './components/PageShell.jsx'

export default function App() {
  return (
    <PageShell title="Course reader">
      <p>This paragraph is passed as JSX children into `PageShell`.</p>
      <p>Your goal is to ensure it renders inside the scrollable main region.</p>
    </PageShell>
  )
}
