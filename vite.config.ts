import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "node:path";

// https://vitejs.dev/config/
export default defineConfig({
	server: {
		origin: "http://localhost:5000",
	},
	build: {
		manifest: true,
		rollupOptions: {
			input: {
				add_question: resolve(
					__dirname,
					"nebula/src/add_question/add_question.ts"
				),
			},
			output: {
				dir: "nebula/static/dist",
				entryFileNames: "[name].js",
				chunkFileNames: "[name].js",
				assetFileNames: "[name].[ext]",
			},
		},
	},
	plugins: [vue()],
	resolve: {
		alias: {
			"@": fileURLToPath(new URL("./nebula/src", import.meta.url)),
		},
	},
});
