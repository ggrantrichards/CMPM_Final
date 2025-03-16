import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/generate": "http://127.0.0.1:8080",
      "/list-builds": "http://127.0.0.1:8080",
      "/load-build": "http://127.0.0.1:8080",
      "/download-schematic": "http://127.0.0.1:8080",
      "/build-status": "http://127.0.0.1:8080",
    },
  },
});
