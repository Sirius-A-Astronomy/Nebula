import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "node:path";

// https://vitejs.dev/config/
export default defineConfig({
  publicDir: "nebula/src/public",
  base: "/static/",
  build: {
    manifest: true,
    copyPublicDir: true,

    rollupOptions: {
      input: {
        app: resolve(__dirname, "nebula/src/js/App.ts"),
      },
      output: {
        dir: "nebula/static",
        entryFileNames: "[name].js",
        chunkFileNames: "[name].js",
        assetFileNames: "[name].[ext]",
      },
    },
  },
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./nebula/src/js", import.meta.url)),
      "@scss": fileURLToPath(new URL("./nebula/src/scss", import.meta.url)),
      "@views": fileURLToPath(
        new URL("./nebula/src/js/views", import.meta.url)
      ),
      "@components": fileURLToPath(
        new URL("./nebula/src/js/components", import.meta.url)
      ),
      "@stores": fileURLToPath(
        new URL("./nebula/src/js/stores", import.meta.url)
      ),
      "@http": fileURLToPath(new URL("./nebula/src/js/http", import.meta.url)),
    },
  },
});
