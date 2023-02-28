/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "nebula/templates/**/*.html",
        "./nebula/src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        fontFamily: {
            display: ["Poppins", "sans-serif"],
            body: ["Lato", "sans-serif"],
        },
        extend: {
            colors: {
                "primary-clr": "var(--color-primary)",
                "secondary-clr": "var(--color-secondary)",
                "tertiary-clr": "var(--color-tertiary)",
                "accent-clr": "var(--color-accent)",
                "accent-focus": "var(--color-accent-focus)",
                "primary-active": "var(--color-primary-active)",

                "primary-text": "var(--color-text-primary)",
                "secondary-text": "var(--color-text-secondary)",
                "tertiary-text": "var(--color-text-tertiary)",

                "on-primary-text": "var(--color-text-on-primary)",
                "on-accent-text": "var(--color-text-on-accent)",

                "primary-bg": "var(--color-background)",
                "secondary-bg": "var(--color-background-secondary)",
                "tertiary-bg": "var(--color-background-tertiary)",

                "code-bg": "var(--color-code-bg)",
                "code-text": "var(--color-code-text)",
                "code-bg-muted": "var(--color-code-bg-muted)",

                "alert-error": "var(--color-alert-error)",
                "alert-warning": "var(--color-alert-warning)",
                "alert-success": "var(--color-alert-success)",
                "alert-info": "var(--color-alert-info)",

                "alert-error-text": "var(--color-alert-error-text)",
                "alert-warning-text": "var(--color-alert-warning-text)",
                "alert-success-text": "var(--color-alert-success-text)",
                "alert-info-text": "var(--color-alert-info-text)",
            },
        },
        container: {
            center: true,
            padding: "0.75rem",
        },
    },
    plugins: [require("@tailwindcss/forms")],
};
