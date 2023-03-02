import { defineConfig } from "vite";
import { fileURLToPath, URL } from "node:url";

export default defineConfig({
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("../nebula/src/js", import.meta.url)),
      "@scss": fileURLToPath(new URL("../nebula/src/scss", import.meta.url)),
      "@views": fileURLToPath(
        new URL("../nebula/src/js/views", import.meta.url)
      ),
      "@components": fileURLToPath(
        new URL("../nebula/src/js/components", import.meta.url)
      ),
      "@stores": fileURLToPath(
        new URL("../nebula/src/js/stores", import.meta.url)
      ),
      "@http": fileURLToPath(new URL("../nebula/src/js/http", import.meta.url)),
    },
  },
});
