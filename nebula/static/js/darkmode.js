const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)');

// set colorsCourse as the :root css variable
let colorsSource = getComputedStyle(document.documentElement);

let colorScheme = ['--color-background', '--color-background-secondary', '--color-text-primary', '--color-text-secondary', 
    '--color-text-tertiary', '--color-text-accent', '--color-primary', '--color-secondary','--color-accent']

const setColorScheme = e => {
  if (e.matches) {
    // Dark
    console.log('Dark mode')
    colorScheme.forEach(function (color) {
        document.documentElement.style.setProperty(color, colorsSource.getPropertyValue(color + "-dark"));
    });
  } else {
    // Light
    console.log('Light mode')
    colorScheme.forEach(function (color) {
        document.documentElement.style.setProperty(color, colorsSource.getPropertyValue(color + "-light"));
    });
  }
}
  
setColorScheme(prefersDarkMode);
prefersDarkMode.addEventListener('change', setColorScheme);