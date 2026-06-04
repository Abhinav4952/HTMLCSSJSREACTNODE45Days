import PostExplorer from './components/PostExplorer.jsx'

export default function App() {
  return (
    <main>
      <h1>Integration: post + comments</h1>
      <p>One thunk fetches two resources. Wire `extraReducers` so the article renders.</p>
      <PostExplorer />
    </main>
  )
}
