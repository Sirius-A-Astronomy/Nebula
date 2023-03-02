class TagInput {
	constructor(element, options) {
		this.element = element;
		this.options = options;
		this.tags = this.options.inputStore.value
			? JSON.parse(this.options.inputStore.value)
			: [];
		this.tagContainer = document.createElement("div");
		this.tagContainer.classList.add("tag-container");
		this.element.parentNode.insertBefore(this.tagContainer, this.element);

		this.onKeyDown = this.onKeyDown.bind(this);
		this.onFocus = this.onFocus.bind(this);
		this.onBlur = this.onBlur.bind(this);
		this.onPaste = this.onPaste.bind(this);
		this.onCut = this.onCut.bind(this);
		this.options.onAddTag = this.options.onAddTag.bind(this);
		this.options.onRemoveTag = this.options.onRemoveTag.bind(this);
		this.options.addTag = this.options.addTag.bind(this);
	}

	init() {
		this.element.addEventListener("keydown", this.onKeyDown);
		this.element.addEventListener("focus", this.onFocus);
		this.element.addEventListener("blur", this.onBlur);
		this.element.addEventListener("paste", this.onPaste);
		this.element.addEventListener("cut", this.onCut);
		for (let tag of this.tags) {
			this.options.addTag(tag);
		}
	}

	onKeyDown(e) {
		if (
			e.key == ";" ||
			e.key == "," ||
			e.key == "Enter" ||
			e.key == "Tab"
		) {
			let value = this.element.value;
			if (value) {
				this.element.value = "";
				this.options.onAddTag(value);
				e.preventDefault();
			}
			return false;
		}
		if (e.key == "Backspace") {
			const value = this.element.value;
			if (!value) {
				this.options.onRemoveTag();
				e.preventDefault();
			}
			return false;
		}
	}

	onFocus(e) {
		this.element.classList.add("is-focused");
	}

	onBlur(e) {
		this.element.classList.remove("is-focused");
	}

	onPaste(e) {
		const clipboardData = e.clipboardData || window.clipboardData;
		const pastedData = clipboardData.getData("Text");
		const tags = pastedData.split(",");

		if (tags.length) {
			for (let i = 0; i < tags.length - 1; i++) {
				this.options.onAddTag(tags[i]);
			}
			this.element.value = DOMPurify.sanitize(
				tags[tags.length - 1].trim(),
				{
					ALLOWED_TAGS: [],
				}
			);
		}
		e.preventDefault();
	}

	onCut(e) {
		const clipboardData = e.clipboardData || window.clipboardData;
		const cutData = clipboardData.getData("Text");
		const tags = cutData.split(",");
		if (tags.length) {
			this.options.onRemoveTag();
		}
	}
}

class AutoComplete {
	constructor(element, options) {
		this.element = element;
		this.options = options;
		this.source = options.source;
		this.onKeyDown = this.onKeyDown.bind(this);
		this.navigate = this.navigate.bind(this);
		this.clear = this.clear.bind(this);
		this.select = this.select.bind(this);
		this.showAutocomplete = this.showAutocomplete.bind(this);

		this.init();
	}

	init() {
		this.element.addEventListener("keydown", this.onKeyDown);
		this.element.addEventListener("input", this.showAutocomplete);
	}

	onKeyDown(e) {
		if (e.key === "ArrowDown") {
			this.navigate(1);
			e.preventDefault();
		} else if (e.key === "ArrowUp") {
			this.navigate(-1);
			e.preventDefault();
		} else if (e.key === "Enter" || e.key === "Tab") {
			if (this.element.value != "") {
				e.preventDefault();
			}
			if (this.selected !== undefined) {
				this.options.onSelect(this.selected);
				this.selected = undefined;
			}
			this.showAutocomplete();
		} else if (e.key === "Escape" || e.key === "Backspace") {
			this.selected = undefined;
		}
	}

	showAutocomplete() {
		this.clear();
		if (this.element.value === "") {
			return;
		}
		this.suggestionsContainer = document.createElement("div");
		this.suggestionsContainer.classList.add("suggestions-container");
		this.element.parentNode.insertBefore(
			this.suggestionsContainer,
			this.element.nextSibling
		);
		this.suggestions = this.source.filter((suggestion) => {
			return suggestion
				.toLowerCase()
				.includes(this.element.value.toLowerCase());
		});

		let suggestionResults = fuzzysort.go(this.element.value, this.source);

		suggestionResults.forEach((suggestion) => {
			let suggestionElement = document.createElement("div");
			suggestionElement.classList.add("suggestion");
			suggestionElement.innerHTML = DOMPurify.sanitize(
				fuzzysort.highlight(suggestion, "<span>", "</span>"),
				{
					ALLOWED_TAGS: ["span"],
				}
			);
			suggestionElement.addEventListener("click", this.select);
			this.suggestionsContainer.appendChild(suggestionElement);
		});
	}

	/**
	 * Navigate through the suggestions
	 * @param {int} direction how many steps to move in the direction (positive for next, negative for previous)
	 */
	navigate(direction) {
		if (this.suggestionsContainer === undefined) {
			return;
		}

		let suggestions =
			this.suggestionsContainer.querySelectorAll(".suggestion");

		if (suggestions.length === 0) {
			return;
		}
		if (this.selected === undefined) {
			this.selected =
				direction > 0
					? suggestions[0]
					: suggestions[suggestions.length - 1];
			this.selected.classList.add("selected");
			this.selectedIndex = direction > 0 ? 0 : suggestions.length - 1;
			this.element.value = DOMPurify.sanitize(this.selected.innerHTML, {
				ALLOWED_TAGS: [],
			});
			this.selected.scrollIntoView();
			return;
		}

		let newIndex = (this.selectedIndex + direction) % suggestions.length;
		if (newIndex < 0) {
			newIndex += suggestions.length;
		}

		this.selected.classList.remove("selected");
		this.selected = suggestions[newIndex];
		this.selectedIndex = newIndex;
		this.selected.classList.add("selected");
		let topOffset = this.selected.offsetTop;
		this.suggestionsContainer.scroll({
			top: topOffset - this.suggestionsContainer.offsetTop,
			behavior: "smooth",
		});

		this.element.value = DOMPurify.sanitize(this.selected.innerHTML, {
			ALLOWED_TAGS: [],
		});
	}

	select(e) {
		let target = e.target;
		if (!e.target.classList.contains("suggestion")) {
			if (!e.target.parentNode.classList.contains("suggestion")) {
				return;
			}
			target = e.target.parentNode;
		}
		this.element.value = DOMPurify.sanitize(target.innerHTML, {
			ALLOWED_TAGS: [],
		});
		this.selected = target;
		this.selectedIndex = Array.from(
			this.suggestionsContainer.querySelectorAll(".suggestion")
		).indexOf(target);
		this.options.onSelect(this.selected);
	}

	clear() {
		if (this.suggestionsContainer !== undefined) {
			this.suggestionsContainer.remove();
			this.suggestionsContainer = undefined;
		}
	}
}

let tag_input, autocomplete;

async function initTagInputs() {
	const subjectTags = await getSubjectTags();
	let tag_inputs = document.querySelectorAll(".tag-input");
	tag_inputs.forEach(async function (input) {
		let autocomplete; // Initialize later

		let inputStore = document.getElementById(
			input.getAttribute("data-store-in")
		);

		let tag_input = new TagInput(input, {
			onAddTag: function (value) {
				if (this.tags.includes(value)) {
					return;
				}
				this.options.addTag(value);
				this.element.focus();
				this.tags.push(value);
				this.options.inputStore.value = JSON.stringify(this.tags);
			},
			onRemoveTag: function () {
				const tags =
					this.element.parentNode.querySelectorAll(".subject-tag");

				if (tags.length) {
					tag_value = DOMPurify.sanitize(
						tags[tags.length - 1].innerText.trim(),
						{
							ALLOWED_TAGS: [],
						}
					);
					tags[tags.length - 1].remove();
					this.element.value = tag_value;
				}
				this.tags.pop();
				this.options.inputStore.value = JSON.stringify(this.tags);
			},
			addTag: function (value) {
				const tag = document.createElement("span");
				tag.classList.add("subject-tag");
				value = DOMPurify.sanitize(value.trim(), {
					ALLOWED_TAGS: [],
				});
				tag.innerHTML = value;
				tag.title = value;
				this.element.value = "";
				this.tagContainer.append(tag);
			},
			inputStore: inputStore,
		});

		// autocomplete

		autocomplete = new AutoComplete(input, {
			source: subjectTags.map((tag) => tag.name),
			onSelect: function (suggestion) {
				tag_input.options.onAddTag(suggestion.innerText);
			},
		});
		tag_input.init();
	});

	async function getSubjectTags() {
		const subjectTags = await fetch("/api/get_subject_tags")
			.then((response) => {
				return response.json();
			})
			.then((data) => data.subject_tags)
			.catch((error) => console.log(error));
		return subjectTags;
	}
}

initTagInputs();
