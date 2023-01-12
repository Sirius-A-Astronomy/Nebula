import { ref } from "vue";

export const isSideMenuOpen = ref(false);

export const toggleSideMenu = () => {
	isSideMenuOpen.value = !isSideMenuOpen.value;
};

export const closeSideMenu = () => {
	isSideMenuOpen.value = false;
};

export const isProfileMenuOpen = ref(false);

export const toggleProfileMenu = () => {
	isProfileMenuOpen.value = !isProfileMenuOpen.value;
};

export const closeProfileMenu = () => {
	isProfileMenuOpen.value = false;
};
