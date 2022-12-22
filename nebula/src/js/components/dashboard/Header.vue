<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>

<template>
	<div class="w-full navbar">
		<div class="container flex flex-row justify-between items-center py-2">
			<a class="flex flex-row items-center navbar-brand" href="/">
				<span class="site-name">Nebula</span>
			</a>

			<nav class="flex flex-row items-center">
				<RouterLink
					to="/dashboard"
					class="px-2 py-2 nav-link"
					active-class="active"
					>Dashboard</RouterLink
				>
				<RouterLink
					to="/dashboard/test"
					class="px-2 py-2 nav-link"
					active-class="active"
					>Test</RouterLink
				>
			</nav>
		</div>
	</div>
</template>

<style lang="scss" scoped></style>
