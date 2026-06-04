import { useState } from 'react'
import TicketTimer from './components/TicketTimer.jsx'

export default function App() {
  const [mounted, setMounted] = useState(true)

  return (
    <main>
      <h1>Ticket timer</h1>
      <p>Use the toggle to mount/unmount the timer and verify cleanup stops the ticking.</p>
      <button type="button" onClick={() => setMounted((v) => !v)}>
        {mounted ? 'Unmount timer' : 'Mount timer'}
      </button>
      {mounted ? <TicketTimer /> : <p>Timer unmounted.</p>}
    </main>
  )
}
