<script setup lang="ts">
import CookieNotice from "@components/ui/CookieNotice.vue";

import "@scss/main.scss";
import { useRoute } from "vue-router";
import Dashboard from "@/DashboardLayout.vue";
import BaseLayout from "@/BaseLayout.vue";

import ModalContainer from "@components/ui/modals/ModalContainer.vue";
import FlashContainer from "@components/ui/FlashContainer.vue";

const route = useRoute();
</script>

<template>
	<div>
		<a href="#content" id="skip-link" class="skip-link sr-only"
			>Skip to content</a
		>
		<CookieNotice />
		<ModalContainer />
		<FlashContainer />

		<Dashboard v-if="route.name?.toString().startsWith('dashboard')" />
		<BaseLayout v-else />
	</div>
</template>

<style lang="scss" scoped>
.skip-link,
#skip-link {
	position: absolute;
	top: 8px;
	left: 8px;
	padding: 8px 16px;
	z-index: 999;
	border-radius: 8px;
	font-size: 12px;
	font-weight: bold;
	text-decoration: none;
	color: var(--color-primary-active);
	box-shadow: var(--box-shadow);
	background-color: var(--color-background);

	&:focus {
		height: auto;
		width: auto;
		clip: auto;
		-webkit-clip-path: none;
		clip-path: none;
	}
}
</style>
