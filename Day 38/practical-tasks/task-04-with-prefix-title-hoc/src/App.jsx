import SectionCard from './components/SectionCard.jsx'
import { withBracketedTitle } from './hoc/withBracketedTitle.jsx'

const BracketedSection = withBracketedTitle(SectionCard)

export default function App() {
  return (
    <main>
      <h1>HOC lab</h1>
      <BracketedSection title="Announcements">
        <p>Holiday schedule will post next week.</p>
      </BracketedSection>
    </main>
  )
}
