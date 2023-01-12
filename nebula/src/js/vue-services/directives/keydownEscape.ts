// @ts-nocheck
export const vKeydownEscape = {
	beforeMount: (el, binding) => {
		el.clickOutsideEvent = (event) => {
			// here I check that click was outside the el and his children
			if (event.key !== "Escape") {
				return;
			}
			// and if it did, call method provided in attribute value
			if (binding.value instanceof Function) {
				binding.value();
				return;
			}
		};
		document.addEventListener("keydown", el.clickOutsideEvent);
	},
	unmounted: (el) => {
		document.removeEventListener("keydown", el.clickOutsideEvent);
	},
};
