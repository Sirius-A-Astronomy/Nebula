
// set colorsCourse as the :root css variable
let colorsSource = getComputedStyle(document.documentElement);

// Add colors that should respond to the prefers-color-scheme media query here:
let colorScheme = ['--color-background', '--color-background-secondary', '--color-text-primary', '--color-text-secondary',
  '--color-text-tertiary', '--color-text-accent', '--color-text-on-accent',
  '--color-text-accent-focus', '--color-primary', '--color-secondary', '--color-accent'];

const setColorScheme = e => {
  if (e.matches) {
    // Set each color variable to it's respective color in the dark color scheme
    colorScheme.forEach(function (color) {
      document.documentElement.style.setProperty(color, colorsSource.getPropertyValue(color + "-dark"));
    });
  } else {
    // Set each color variable to it's respective color in the light color scheme
    colorScheme.forEach(function (color) {
      document.documentElement.style.setProperty(color, colorsSource.getPropertyValue(color + "-light"));
    });
  }
}


if (window.matchMedia) {

  const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)');
  setColorScheme(prefersDarkMode);
  if (prefersDarkMode?.addEventListener) {
    prefersDarkMode.addEventListener('change', setColorScheme);
  } else {
    prefersDarkMode.addListener(setColorScheme);
  }
}