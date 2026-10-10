/**
 * Shared fetch wrapper for talking to the Express API.
 * - During `npm run dev`, Vite proxies `/api` to the backend (see vite.config.js).
 * - Later: attach JWT with `setAuthToken(token)` after login.
 */

let authToken = null;

export function setAuthToken(token) {
  authToken = token || null;
}

export async function apiRequest(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  if (authToken) {
    headers.Authorization = `Bearer ${authToken}`;
  }

  const res = await fetch(path.startsWith('/api') ? path : `/api${path}`, {
    ...options,
    headers,
  });

  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = { message: text };
  }

  if (!res.ok) {
    const err = new Error(data?.message || `Request failed (${res.status})`);
    err.status = res.status;
    err.data = data;
    throw err;
  }

  return data;
}
