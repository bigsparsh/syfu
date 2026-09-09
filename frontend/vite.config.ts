import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

const BACKEND = process.env.SYFU_API ?? 'http://localhost:8000'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss()],
  server: {
    // Proxy API calls to the FastAPI backend so the SPA can use
    // same-origin /api/* requests during development.
    proxy: {
      '/api': {
        target: BACKEND,
        changeOrigin: true,
      },
    },
  },
})
