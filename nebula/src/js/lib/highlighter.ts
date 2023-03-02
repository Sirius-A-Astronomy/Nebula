import {
    setCDN,
    getHighlighter,
    BUNDLED_LANGUAGES,
    BUNDLED_THEMES,
    type Highlighter,
} from "shiki";
import type { Lang, Theme } from "shiki/dist/index";

setCDN("https://cdn.jsdelivr.net/npm/shiki/");

const preloadLanguages: Lang[] = ["python", "markdown"];
const preloadThemes: Theme[] = ["material-palenight"];

let highlighter: Highlighter;
let moduleState: "uninitialised" | "initialising" | "initialised" =
    "uninitialised";

// ensure shiki is only loaded once
const init = async (): Promise<void> => {
    if (moduleState === "initialised") {
        return;
    }
    if (moduleState === "initialising") {
        if (!highlighter) {
            await new Promise((resolve) => setTimeout(resolve, 100));
            return await init();
        }
        return;
    }
    moduleState = "initialising";
    highlighter = await getHighlighter({
        themes: preloadThemes,
        langs: preloadLanguages,
    });
    moduleState = "initialised";
};

export const getShikiHighlighter = async () => {
    if (!highlighter) {
        await init();
    }
    const loadedLanguages = highlighter.getLoadedLanguages();
    for (const lang of preloadLanguages) {
        if (!loadedLanguages.includes(lang)) {
            const bundles = BUNDLED_LANGUAGES.filter((bundle) => {
                // Languages are specified by their id, they can also have aliases (i. e. "js" and "javascript")
                return bundle.id === lang || bundle.aliases?.includes(lang);
            });
            if (bundles.length > 0) {
                await highlighter.loadLanguage(lang);
            }
        }
    }

    const loadedThemes = highlighter.getLoadedThemes();
    for (const theme of preloadThemes) {
        // Check for the loaded themes, and load the theme if it's not loaded yet.
        if (!loadedThemes.includes(theme)) {
            // Check if the theme is supported by Shiki
            if (BUNDLED_THEMES.includes(theme)) {
                await highlighter.loadTheme(theme);
            }
        }
    }
    return highlighter;
};
