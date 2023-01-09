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

export const useMathJax = async () => {
	if ((window as any).MathJax?.version) {
		return (window as any).MathJax;
	}

	if (attempts > 10) {
		console.error("MathJax failed to load");
		return;
	}
	addMathJaxScrips();

	attempts++;
	await new Promise((resolve) => setTimeout(resolve, 100));
	return await useMathJax();
};
