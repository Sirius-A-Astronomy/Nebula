import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "node:path";

// https://vitejs.dev/config/
export default defineConfig({
	server: {
		origin: "http://localhost:5000",
	},
	root: "nebula/src",
	build: {
		manifest: true,
		rollupOptions: {
			input: {
				add_question: resolve(
					__dirname,
					"nebula/src/js/add_question/add_question.ts"
				),
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
		},
	},
});
