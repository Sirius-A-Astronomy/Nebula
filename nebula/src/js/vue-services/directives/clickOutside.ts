// @ts-nocheck
export const vClickOutside = {
	beforeMount: (el, binding) => {
		el.clickOutsideEvent = (event) => {
			// here I check that click was outside the el and his children
			if (el == event.target || el.contains(event.target)) {
				return;
			}
			// and if it did, call method provided in attribute value
			if (binding.value instanceof Function) {
				binding.value();
				return;
			}

			for (const excluded of binding.value.exclude) {
				const element = document.getElementById(excluded);
				if (
					element == event.target ||
					element?.contains(event.target)
				) {
					return;
				}
			}
			binding.value.handler();
			return;
		};
		document.addEventListener("click", el.clickOutsideEvent);
	},
	unmounted: (el) => {
		document.removeEventListener("click", el.clickOutsideEvent);
	},
};
