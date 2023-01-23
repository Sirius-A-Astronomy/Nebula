// @ts-nocheck
export const vClickOutside = {
  beforeMount: (el, binding) => {
    el.clickOutsideEvent = (event) => {
      // Check if the click was inside the element
      if (el == event.target || el.contains(event.target)) {
        return;
      }

      // if no exclude is provided, just run the handler
      if (binding.value instanceof Function) {
        binding.value();
        return;
      }

      // Check if the click was inside an excluded element
      for (const excluded of binding.value.exclude) {
        const element = document.getElementById(excluded);
        if (element == event.target || element?.contains(event.target)) {
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
