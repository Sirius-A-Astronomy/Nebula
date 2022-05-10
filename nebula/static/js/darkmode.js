// set colorsCourse as the :root css variable
const colorsSource = getComputedStyle(document.documentElement);

// Add colors that should respond to the prefers-color-scheme media query here:
const colorScheme = [
	"--color-primary",
	"--color-secondary",
	"--color-tertiary",
	"--color-background",
	"--color-background-secondary",
	"--color-background-tertiary",
	"--color-text-primary",
	"--color-text-secondary",
	"--color-text-tertiary",
	"--color-text-on-primary",
	"--color-text-on-accent",
	"--color-accent-focus",
	"--color-accent",
	"--color-form-is-valid",
	"--color-form-is-invalid",
];

const darkModeToggle = document.getElementById("dark-mode-toggler");

const initialPrefersDarkMode = () => {
	if (window.matchMedia) {
		const darkModePreference = window.matchMedia(
			"(prefers-color-scheme: dark)"
		);
		if (darkModePreference.matches) {
			darkModeToggle.checked = true;
		}
		return darkModePreference.matches ? "dark" : "light";
	}
	return "light";
};

function setDarkModeonLoad() {
	let prefersDarkMode = localStorage.getItem("prefersDarkMode");
	if (prefersDarkMode === null) {
		prefersDarkMode = initialPrefersDarkMode();
		localStorage.setItem("prefersDarkMode", prefersDarkMode);
	}
	setDarkMode(prefersDarkMode);
}
setDarkModeonLoad();

darkModeToggle.addEventListener("click", function () {
	let currentDarkModePreference = localStorage.getItem("prefersDarkMode");
	if (currentDarkModePreference != "light") {
		localStorage.setItem("prefersDarkMode", "light");
		setDarkMode("light");
	} else {
		localStorage.setItem("prefersDarkMode", "dark");
		setDarkMode("dark");
	}
	darkModeToggle.classList.add("animate-rotation");
});

function setDarkMode(mode) {
	colorScheme.forEach(function (color) {
		document.documentElement.style.setProperty(
			color,
			colorsSource.getPropertyValue(color + "-" + mode)
		);
	});
	document.documentElement.style.setProperty("color-scheme", mode);

	darkModeToggle.checked = mode == "dark";
	if (mode == "dark") {
		darkModeToggle.classList.add("dark-mode-enabled");
		darkModeToggle.classList.remove("light-mode-enabled");
	} else {
		darkModeToggle.classList.remove("dark-mode-enabled");
		darkModeToggle.classList.add("light-mode-enabled");
	}
}
