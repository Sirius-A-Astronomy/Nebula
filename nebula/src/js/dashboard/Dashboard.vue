<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";

import "@scss/views/dashboard.scss";
import "@scss/main.scss";

import Header from "@components/dashboard/Header.vue";
</script>

<template>
	<div class="w-full">
		<Header />
		<div class="container">
			<RouterView />
		</div>
	</div>
</template>

<style lang="scss" scoped></style>
