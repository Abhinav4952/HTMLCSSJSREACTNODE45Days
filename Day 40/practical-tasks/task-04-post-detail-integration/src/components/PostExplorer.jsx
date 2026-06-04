import { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { fetchPostBundle } from '../features/detail/detailSlice.js'

export default function PostExplorer() {
  const dispatch = useDispatch()
  const { post, comments, status, error } = useSelector((state) => state.detail)
  const [postId, setPostId] = useState(1)

  return (
    <section>
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
        <label>
          Post id:{' '}
          <select value={postId} onChange={(e) => setPostId(Number(e.target.value))}>
            {[1, 2, 3, 4, 5].map((id) => (
              <option key={id} value={id}>
                {id}
              </option>
            ))}
          </select>
        </label>
        <button type="button" onClick={() => dispatch(fetchPostBundle(postId))}>
          Load post + comments
        </button>
      </div>
      {status === 'loading' ? <p>Loading…</p> : null}
      {status === 'failed' ? <p role="alert">Error: {String(error)}</p> : null}
      {post ? (
        <article style={{ marginTop: '1rem' }}>
          <h2 style={{ marginBottom: '0.35rem' }}>{post.title}</h2>
          <p>{post.body}</p>
          <p>
            <strong>Comments loaded:</strong> {comments.length}
          </p>
        </article>
      ) : null}
    </section>
  )
}
