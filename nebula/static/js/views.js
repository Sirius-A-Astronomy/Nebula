// expandableText
document
	.querySelectorAll(".expandable-text")
	.forEach(function (expandableText) {
		const expandableTextContent = expandableText.innerHTML
			.trim()
			.replace(/\s+/g, " ");

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
		expandTextToggle.innerHTML = "Read more";
		const expandableTextContentTruncated =
			expandableTextContent.substring(0, displayLimit) + " (...) ";
		let isTextExpanded = false;

		expandTextToggle.addEventListener("click", function () {
			if (isTextExpanded) {
				expandableText.innerHTML = expandableTextContentTruncated;
				expandableText.blur();
				expandableText.appendChild(expandTextToggle);
				isTextExpanded = false;
				expandTextToggle.innerHTML = "Read more";
			} else {
				expandableText.innerHTML = expandableTextContent + " ";
				expandableText.appendChild(expandTextToggle);
				expandableText.blur();
				isTextExpanded = true;
				expandTextToggle.innerHTML = "Read less";
			}
		});

		expandableText.innerHTML = expandableTextContentTruncated;
		expandableText.appendChild(expandTextToggle);
	});

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
			// if the elements that need to be shown are not a sibling of the control form field, show them via the data-hidden-by attribute
			document
				.querySelectorAll(`[data-hidden-by='${formField.id}']`)
				.forEach((element) => {
					element.classList.remove("visually-hidden");
				});
		});
	});
