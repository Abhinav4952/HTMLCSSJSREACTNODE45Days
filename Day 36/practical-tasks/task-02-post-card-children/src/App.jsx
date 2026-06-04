import PostCard from './components/PostCard.jsx'

export default function App() {
  return (
    <main>
      <h1>Newsroom</h1>
      <PostCard title="Campus Wi-Fi maintenance">
        <p>Wireless access points in Building C will restart between 02:00–03:00.</p>
        <p>Please save work locally if you are on-site during the window.</p>
      </PostCard>
    </main>
  )
}
