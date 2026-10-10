import { useEffect, useState } from 'react'
import { apiRequest } from '../../api/client'
import './Home.css'

/**
 * Home page demonstrates FE ↔ BE integration with useEffect + apiRequest.
 * (This project uses Context for auth, not Redux.)
 *
 * Prerequisites for a live message:
 * - backend/.env has a valid MONGO_URI
 * - backend is running (`npm run dev` in backend/)
 */
export default function Home() {
  const [message, setMessage] = useState('')
  const [status, setStatus] = useState('idle')
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    async function load() {
      setStatus('loading')
      setError(null)
      try {
        const data = await apiRequest('/api/welcome')
        if (!cancelled) {
          setMessage(data.message || 'Welcome to the Blog CMS')
          setStatus('succeeded')
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message)
          setStatus('failed')
        }
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [])

  return (
    <section className="home-hero p-4 p-md-5">
      <p className="text-uppercase small text-muted mb-2">Capstone boilerplate</p>
      <h1 className="display-6">Blog CMS</h1>
      <p className="lead mb-4">
        This shell is ready. Build the full CMS with Bootstrap, React Router,
        Context API for auth, and the Express API.
      </p>

      <div className="card shadow-sm">
        <div className="card-body">
          <h2 className="h5 card-title">Backend welcome message</h2>
          <p className="card-text home-status mb-0">
            {status === 'loading' && 'Loading from /api/welcome…'}
            {status === 'failed' && (
              <span className="text-danger">
                Could not reach the API. Start the backend with a valid MONGO_URI.
                {' '}
                <span className="d-block small mt-1">{error}</span>
              </span>
            )}
            {status === 'succeeded' && (
              <span className="text-success">{message}</span>
            )}
            {status === 'idle' && 'Waiting to fetch…'}
          </p>
        </div>
      </div>

      <div className="alert alert-info mt-4 mb-0" role="status">
        Next steps are in <code>PROJECT_INSTRUCTIONS.md</code> at the project root.
      </div>
    </section>
  )
}
