import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Proxy /api/* to the Express backend during local development.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5003',
        changeOrigin: true,
      },
    },
  },
})
