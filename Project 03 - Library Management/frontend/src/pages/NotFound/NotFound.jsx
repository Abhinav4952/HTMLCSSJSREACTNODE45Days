import { Link } from 'react-router-dom'
import './NotFound.css'

export default function NotFound() {
  return (
    <div className="text-center py-5">
      <h1 className="notfound-title">404</h1>
      <p className="lead">That page does not exist yet.</p>
      <Link className="btn btn-primary" to="/">
        Back to Home
      </Link>
    </div>
  )
}
