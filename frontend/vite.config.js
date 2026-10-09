import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    allowedHosts: ['4173-itn7rcxefatfesumqbthp-7e83371a.us1.manus.computer', 'localhost'],
  },
})
