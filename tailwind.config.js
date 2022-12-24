/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ["./index.html", "./nebula/src/**/*.{vue,js,ts,jsx,tsx}"],
	theme: {
		extend: {
			colors: {
				"primary-clr": "var(--color-primary)",
				"secondary-clr": "var(--color-secondary)",
				"tertiary-clr": "var(--color-tertiary)",
				"accent-clr": "var(--color-accent)",
				"primary-active": "var(--color-primary-active)",

				"primary-text": "var(--color-primary-text)",
				"secondary-text": "var(--color-secondary-text)",
				"tertiary-text": "var(--color-tertiary-text)",

				"on-primary-text": "var(--color-text-on-primary)",

				"primary-bg": "var(--color-background)",
				"secondary-bg": "var(--color-background-secondary)",
				"tertiary-bg": "var(--color-background-tertiary)",
			},
		},
		container: {
			center: true,
			padding: "1rem",
		},
	},
	plugins: [],
};
