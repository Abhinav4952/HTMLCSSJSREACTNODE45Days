import UserGreeting from './components/UserGreeting.jsx'

export default function App() {
  return (
    <main>
      <h1>Greeting lab</h1>
      <UserGreeting name="Avery" role="student" />
      <UserGreeting name="Jordan" />
    </main>
  )
}
