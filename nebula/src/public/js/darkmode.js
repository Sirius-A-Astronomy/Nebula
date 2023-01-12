let darkModeToggle;

const initialPrefersDarkMode = () => {
	if (window.matchMedia) {
		const darkModePreference = window.matchMedia(
			"(prefers-color-scheme: dark)"
		);
		return darkModePreference.matches ? "dark" : "light";
	}
	return "light";
};

let prefersDarkMode;
function setDarkModeDuringLoad() {
	prefersDarkMode = localStorage.getItem("prefersDarkMode");
	if (prefersDarkMode === null) {
		prefersDarkMode = initialPrefersDarkMode();
		localStorage.setItem("prefersDarkMode", prefersDarkMode);
	}
	setDarkMode(prefersDarkMode);
}
setDarkModeDuringLoad();

function setDarkMode(mode) {
	if (mode == "dark") {
		document.documentElement.classList.add("dark-mode");
	} else {
		document.documentElement.classList.remove("dark-mode");
	}
	setDarkModeToggleState(mode);
}

window.onload = () => {
	darkModeToggle = document.getElementById("dark-mode-toggler");

	if (!darkModeToggle) {
		return;
	}
	setDarkModeToggleState(prefersDarkMode);
	darkModeToggle.classList.add("animate-rotation");
	darkModeToggle.addEventListener("click", function () {
		let currentDarkModePreference =
			localStorage.getItem("prefersDarkMode") != "light"
				? "dark"
				: "light";
		let newDarkModePreference =
			currentDarkModePreference != "light" ? "light" : "dark";
		localStorage.setItem("prefersDarkMode", newDarkModePreference);
		setDarkMode(newDarkModePreference);
	});
};

function setDarkModeToggleState(state) {
	if (!darkModeToggle) return;
	darkModeToggle.checked = state == "dark";
	if (state != "light") {
		darkModeToggle.classList.add("dark-mode-enabled");
		darkModeToggle.classList.remove("light-mode-enabled");
	} else {
		darkModeToggle.classList.remove("dark-mode-enabled");
		darkModeToggle.classList.add("light-mode-enabled");
	}
}
