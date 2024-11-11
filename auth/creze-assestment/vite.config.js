import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import fs from 'fs';

// https://vite.dev/config/
export default defineConfig({
  server: {
    https: {
      key: fs.readFileSync('./certificates/cert.key'),
      cert: fs.readFileSync('./certificates/cert.crt')
    }
  },
  plugins: [react()],
})
