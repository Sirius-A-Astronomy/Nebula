<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";

import "@scss/views/dashboard.scss";
import "@scss/main.scss";

import Header from "@components/dashboard/Header.vue";
import Sidemenu from "@components/dashboard/Sidemenu.vue";
</script>

<template>
	<div class="w-full min-h-screen">
		<aside
			class="z-20 hidden w-64 overflow-y-auto bg-secondary md:block flex-shrink-0 h-screen fixed">
			<Sidemenu />
		</aside>
		<Header />
		<div class="md:ml-64 container">
			<RouterView />
		</div>
	</div>
</template>

<style lang="scss" scoped></style>
