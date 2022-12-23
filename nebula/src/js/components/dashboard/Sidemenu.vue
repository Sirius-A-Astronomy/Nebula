<script setup lang="ts"></script>

<template>
	<div>
		<a class="flex flex-row items-center navbar-brand" href="/">
			<span class="site-name">Nebula</span>
		</a>

		<nav class="flex flex-col items-start">
			<RouterLink
				to="/dashboard"
				class="px-4 py-2 nav-link"
				active-class="active"
				>Dashboard</RouterLink
			>
			<RouterLink
				to="/dashboard/test"
				class="px-4 py-2 nav-link"
				active-class="active"
				>Test</RouterLink
			>
		</nav>
	</div>
</template>

<style lang="scss" scoped></style>
