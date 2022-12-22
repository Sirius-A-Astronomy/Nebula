import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "node:path";

// https://vitejs.dev/config/
export default defineConfig({
	server: {
		origin: "http://localhost:5000",
	},
	publicDir: "nebula/src/public",
	build: {
		manifest: true,
		copyPublicDir: true,
		rollupOptions: {
			input: {
				add_question: resolve(
					__dirname,
					"nebula/src/js/add_question/add_question.ts"
				),
				main_scss: resolve(__dirname, "nebula/src/scss/main.scss"),

				// SCSS VIEWS
				course_scss: resolve(
					__dirname,
					"nebula/src/scss/views/course.scss"
				),
				login_register_scss: resolve(
					__dirname,
					"nebula/src/scss/views/login_register.scss"
				),
				question_scss: resolve(
					__dirname,
					"nebula/src/scss/views/question.scss"
				),
				profile_scss: resolve(
					__dirname,
					"nebula/src/scss/views/profile.scss"
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
