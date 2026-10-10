import { Outlet } from 'react-router-dom'
import Navbar from '../Navbar/Navbar'
import './Layout.css'

/**
 * Shared page chrome: Navbar + main content + footer.
 * Nested routes render inside <Outlet />.
 */
export default function Layout() {
  return (
    <div className="d-flex flex-column min-vh-100">
      <Navbar />
      <main className="layout-main container py-4 flex-grow-1">
        <Outlet />
      </main>
      <footer className="layout-footer py-3 bg-light">
        <div className="container small text-muted">
          Capstone boilerplate — build features on top of this shell.
        </div>
      </footer>
    </div>
  )
}
