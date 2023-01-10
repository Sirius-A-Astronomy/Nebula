export const addMathJaxScrips = () => {
	// if no MathJax script is found, add it to the head
	if (document.getElementById("MathJax-script")) return;
	(window as any).MathJax = {
		startup: {
			typeset: false,
		},
		tex: {
			tags: "ams",
			inlineMath: [["$", "$"]],
			displayMath: [["$$", "$$"]],
			processEscapes: true,
			processEnvironments: true,
			processRefs: true,
		},
		menuSettings: {
			autocollape: true,
		},
	};
	const scriptPolyfill = document.createElement("script");
	scriptPolyfill.src = "https://polyfill.io/v3/polyfill.min.js?features=es6";

	const scriptMathjax = document.createElement("script");
	scriptMathjax.src =
		"https://cdn.jsdelivr.net/npm/mathjax@3.2.1/es5/tex-mml-chtml.js";
	scriptMathjax.id = "MathJax-script";
	scriptMathjax.async = true;
	document.head.appendChild(scriptMathjax);
};

let attempts = 0;
let mathjax: any;

let moduleState: "uninitialised" | "initialising" | "initialised" =
	"uninitialised";

export const initMathJax = async () => {
	if (moduleState === "initialised") {
		return;
	}
	if (moduleState === "initialising") {
		if (!(window as any).MathJax?.version) {
			await new Promise((resolve) => setTimeout(resolve, 100));
			return await initMathJax();
		}
		if ((window as any).MathJax?.version) {
			mathjax = (window as any).MathJax;
			moduleState = "initialised";
		}
		return;
	}
	moduleState = "initialising";
	addMathJaxScrips();
	await new Promise((resolve) => setTimeout(resolve, 100));
	return await initMathJax();
};

export const useMathJax = async () => {
	if (!mathjax) {
		await initMathJax();
	}
	return mathjax;
};
