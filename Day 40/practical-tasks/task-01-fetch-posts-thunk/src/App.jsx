import PostsList from './components/PostsList.jsx'

export default function App() {
  return (
    <main>
      <h1>Posts lab (`createAsyncThunk`)</h1>
      <p>Wire `extraReducers` so loading, success, and failure states update the list.</p>
      <PostsList />
    </main>
  )
}
