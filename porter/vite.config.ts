import path from "node:path";
import { fileURLToPath } from "node:url";

import { defineConfig, loadEnv, type ProxyOptions } from "vite";
import react from "@vitejs/plugin-react";

/** `vite.config.ts` 가 있는 폴더 = 프론트 루트 */
const FRONTEND_ROOT = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, FRONTEND_ROOT, "");

  /** 개발·프리뷰 UI 포트 — 항상 3000 */
  const DEV_PORT = 3000;

  /** harry_poter 백엔드 API 포트 */
  const API_PORT = Number(env.VITE_API_PORT || 8000);
  const API_ORIGIN = `http://127.0.0.1:${API_PORT}`;

  const apiProxy: ProxyOptions = {
    target: API_ORIGIN,
    changeOrigin: true,
    proxyTimeout: 120_000,
  };

  return {
    root: FRONTEND_ROOT,
    plugins: [react()],
    server: {
      port: DEV_PORT,
      strictPort: true,
      host: true,
      proxy: {
        "/harry-poter": apiProxy,
      },
    },
    preview: {
      port: DEV_PORT,
      strictPort: true,
      host: true,
      proxy: {
        "/harry-poter": apiProxy,
      },
    },
  };
});
