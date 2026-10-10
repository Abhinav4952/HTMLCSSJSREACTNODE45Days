import { createContext, useContext, useMemo, useState } from 'react'

/**
 * Placeholder Auth Context for the Blog CMS (no Redux in this project).
 * Candidates: expand with login/register/logout that call /api/auth and store JWT.
 */
const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(() => localStorage.getItem('blog_token'))

  const value = useMemo(
    () => ({
      user,
      token,
      setUser,
      setToken: (next) => {
        setToken(next)
        if (next) localStorage.setItem('blog_token', next)
        else localStorage.removeItem('blog_token')
      },
      logout: () => {
        setUser(null)
        setToken(null)
        localStorage.removeItem('blog_token')
      },
    }),
    [user, token],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}
