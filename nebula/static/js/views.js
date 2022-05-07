window.MathJax = {
	tex: {
		tags: "ams",
	},
	tex2jax: {
		processEscapes: true,
	},
};

(function () {
	var script = document.createElement("script");
	script.src =
		// "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js";
		"https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML";
	script.async = true;
	document.head.appendChild(script);
})();

/*
    SECTION Expendable-Text
*/

document
	.querySelectorAll(".expandable-text")
	.forEach(function (expandableText) {
		const expandableTextContent = expandableText.textContent
			.trim()
			.replace(/\s+/g, " ")
			.replace(/</g, "&lt;")
			.replace(/>/g, "&gt;");

		let displayLimit;
		if (expandableText?.getAttribute("displaylimit") !== null) {
			displayLimit = expandableText.getAttribute("displaylimit");
		} else {
			displayLimit = 220;
		}

		if (expandableTextContent.length < displayLimit) {
			return;
		}

		let punctIndexes = [
			...expandableTextContent.matchAll(new RegExp("[.!?,]", "gi")),
		].map((a) => a.index);

		// @TODO stupidly large number, should probably find a more elegant way to do this
		let punctIndex = 1_000_000_000;
		if (punctIndexes.length > 0) {
			punctIndex =
				punctIndexes.reduce(function (prev, curr) {
					return Math.abs(curr - displayLimit) <
						Math.abs(prev - displayLimit)
						? curr
						: prev;
				}) + 1;
		}
		let spaceIndexes = [
			...expandableTextContent.matchAll(new RegExp(" ", "gi")),
		].map((a) => Math.abs(a.index));
		let spaceIndex = spaceIndexes.reduce(function (prev, curr) {
			return Math.abs(curr - displayLimit) < Math.abs(prev - displayLimit)
				? curr
				: prev;
		});

		// If the distance between the displayLimit and punctuation is more than 25% of the displayLimit, break at the nearest space.
		if (Math.abs(punctIndex - displayLimit) > displayLimit / 4) {
			punctIndex = spaceIndex;
		}

		// Only change the displayLimit if a suitable breakpoint is found.
		if (
			punctIndex < 1.25 * displayLimit ||
			spaceIndex < 1.25 * displayLimit
		) {
			displayLimit = punctIndex;
		}

		const expandTextToggle = document.createElement("a");
		expandTextToggle.setAttribute("style", "font-size: 0.8125");
		expandTextToggle.setAttribute("href", "#!");
		expandTextToggle.classList.add("inline-link");
		expandTextToggle.textContent = "Read more";
		const expandableTextContentTruncated =
			expandableTextContent.substring(0, displayLimit) + " (...) ";
		let isTextExpanded = false;

		expandTextToggle.addEventListener("click", function () {
			if (isTextExpanded) {
				expandableText.textContent = expandableTextContentTruncated;
				expandableText.blur();
				expandableText.appendChild(expandTextToggle);
				isTextExpanded = false;
				expandTextToggle.textContent = "Read more";
			} else {
				expandableText.textContent = expandableTextContent + " ";
				expandableText.appendChild(expandTextToggle);
				expandableText.blur();
				isTextExpanded = true;
				expandTextToggle.textContent = "Read less";
			}
		});

		expandableText.textContent = expandableTextContentTruncated;
		expandableText.appendChild(expandTextToggle);
	});
// END !SECTION Expendable-Text

/*
    SECTION Hidden-Form-Field
*/

// hide all hidden-form-field-elements
document
	.querySelectorAll(".hidden-form-field-element")
	.forEach(function (element) {
		element.classList.add("visually-hidden");
	});
// Show submit button on form focus
document
	.querySelectorAll(".hidden-form-field-control")
	.forEach(function (formField) {
		formField.addEventListener("focus", function () {
			formField.parentElement
				.querySelectorAll(".hidden-form-field-element")
				.forEach((element) => {
					element.classList.remove("visually-hidden");
				});
			// if the elements that need to be shown are not a sibling
			//   of the control form field, show them via the data-hidden-by attribute
			document
				.querySelectorAll(`[data-hidden-by='${formField.id}']`)
				.forEach((element) => {
					element.classList.remove("visually-hidden");
				});
		});
	});

// !SECTION Hidden-Form-Field

/*
    SECTION Toggle latex instructions
*/
// first hide all latex instructions
instructionContainers = document.querySelectorAll(
	".latex-instructions-container"
);

instructionContainers.forEach((element) => {
	element.style.display = "none";
});

document
	.querySelectorAll("#toggle-latex-instructions-button")
	.forEach((button) => {
		button.addEventListener("click", function (e) {
			instructionContainers.forEach((element) => {
				if (element.style.display === "none") {
					element.style.display = "block";
				} else {
					element.style.display = "none";
				}
			});
			button.blur();
		});
	});

// !SECTION Toggle latex instructions

/*
    SECTION Preview-Form-Input
*/

document
	.querySelectorAll(".show-preview-button")
	.forEach((showPreviewButton) => {
		showPreviewButton.addEventListener("click", function (e) {
			const previewContent = e.target.parentElement.querySelector(
				".preview-form-container"
			);
			previewContent.style.display = "block";
			document
				.querySelectorAll(
					`[data-preview-toggled-by=${showPreviewButton.id}]`
				)
				.forEach((element) => {
					let inputForm = document.querySelector(
						`#${element.attributes["data-preview-value-from"].value}`
					);
					element.textContent = inputForm.value;
					showPreviewButton.disabled = true;
					MathJax.Hub.Queue(["Typeset", MathJax.Hub, element]);
					showPreviewButton.disabled = false;
				});
			e.target.blur();
		});
	});

// !SECTION Preview-Form-Input

/*
    SECTION focus-form-input-field 
*/

document.querySelectorAll(".input-field").forEach((inputField) => {
	inputField.addEventListener("click", function (e) {
		// only focus the input field if the user is not trying to select text
		if (window.getSelection().toString() === "") {
			inputField
				.querySelectorAll("input, textarea, select")
				.forEach((input) => {
					input.focus();
				});
		} else {
			e.stopPropagation();
		}
	});
});
