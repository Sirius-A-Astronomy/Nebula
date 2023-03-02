import { ref } from "vue";

export const isSideMenuOpen = ref(false);

export const toggleSideMenu = () => {
    isSideMenuOpen.value = !isSideMenuOpen.value;
};

export const closeSideMenu = () => {
    isSideMenuOpen.value = false;
};
