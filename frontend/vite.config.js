import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: ['industrace.local', 'www.industrace.local', 'localhost'],
    hmr: false
  },
  build: {
    chunkSizeWarningLimit: 1000,
    assetsDir: 'static'
  },
  optimizeDeps: {
    include: ['vis-network']
  }
})

