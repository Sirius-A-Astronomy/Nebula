/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ["./index.html", "./nebula/src/**/*.{vue,js,ts,jsx,tsx}"],
	theme: {
		extend: {},
		container: {
			center: true,
			padding: "1rem",
		},
	},
	plugins: [],
};
