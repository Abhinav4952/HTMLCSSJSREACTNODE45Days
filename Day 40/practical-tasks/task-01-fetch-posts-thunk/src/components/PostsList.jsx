import { useDispatch, useSelector } from 'react-redux'
import { fetchPosts } from '../features/posts/postsSlice.js'

export default function PostsList() {
  const dispatch = useDispatch()
  const { items, status, error } = useSelector((state) => state.posts)

  return (
    <section>
      <button type="button" onClick={() => dispatch(fetchPosts())}>
        Load posts
      </button>
      {status === 'loading' ? <p>Loading…</p> : null}
      {status === 'failed' ? <p role="alert">Error: {String(error)}</p> : null}
      <ol>
        {items.map((post) => (
          <li key={post.id}>
            <strong>{post.title}</strong>
          </li>
        ))}
      </ol>
    </section>
  )
}
