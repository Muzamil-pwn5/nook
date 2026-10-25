import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    allowedHosts: true,
    proxy: {
      '/agent': 'http://127.0.0.1:8000',
      '/dashboard': 'http://127.0.0.1:8000',
      '/products': 'http://127.0.0.1:8000',
      '/orders': 'http://127.0.0.1:8000',
      '/auth': 'http://127.0.0.1:8000',
    },
  },
})
