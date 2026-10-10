import { NavLink } from 'react-router-dom'
import './Navbar.css'

/**
 * Top navigation.
 * Styling pattern: Bootstrap classes for layout + Navbar.css for custom tweaks.
 * Candidates: add more NavLink items for catalog, cart, login, admin, etc.
 */
export default function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <NavLink className="navbar-brand navbar-brand-logo" to="/">
          ShopLite
        </NavLink>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#mainNav"
          aria-controls="mainNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse" id="mainNav">
          <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <NavLink
                className={({ isActive }) =>
                  `nav-link${isActive ? ' navbar-link-active' : ''}`
                }
                to="/"
                end
              >
                Home
              </NavLink>
            </li>
            {/* Candidates: add Catalog, Cart, Login, Dashboard links here */}
          </ul>
        </div>
      </div>
    </nav>
  )
}
