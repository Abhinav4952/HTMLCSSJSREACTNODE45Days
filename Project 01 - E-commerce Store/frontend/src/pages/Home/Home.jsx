import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { fetchWelcome } from '../../features/welcome/welcomeSlice'
import './Home.css'

/**
 * Home page demonstrates FE ↔ BE integration via Redux Toolkit.
 * 1) On mount, dispatch fetchWelcome
 * 2) Show loading / error / success from the welcome slice
 *
 * Prerequisites for a live message:
 * - backend/.env has a valid MONGO_URI
 * - backend is running (`npm run dev` in backend/)
 * - frontend proxy points at the backend port (vite.config.js)
 */
export default function Home() {
  const dispatch = useDispatch()
  const { message, status, error } = useSelector((state) => state.welcome)

  useEffect(() => {
    dispatch(fetchWelcome())
  }, [dispatch])

  return (
    <section className="home-hero p-4 p-md-5">
      <p className="text-uppercase small text-muted mb-2">Capstone boilerplate</p>
      <h1 className="display-6">E-commerce Store</h1>
      <p className="lead mb-4">
        This shell is ready. Build the full product on top of Bootstrap layout,
        React Router, Redux Toolkit, and the Express API.
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
