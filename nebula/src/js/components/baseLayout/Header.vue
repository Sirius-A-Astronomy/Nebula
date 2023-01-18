<script setup lang="ts">
import { onMounted } from "vue";

import { courseStore } from "@stores/courseStore";
import { courseLevelStore } from "@stores/courseLevelStore";
import { computed, ref } from "@vue/reactivity";
import type { Ref } from "vue";
import Dropdown from "./Dropdown.vue";
import { useRoute } from "vue-router";
import NavDropdown, { type MenuItem } from "./NavDropdown.vue";

const courseLevels = courseLevelStore.getters.all;
const navItems: Ref<MenuItem[]> = ref([]);

const createNavItems = () => {
	const items: MenuItem[] = [];

	const courses = courseStore.getters.all.value;
	const levelTypes = [
		...new Set(courses.map((c) => c.course_level.study_type)),
	];

	const courseItems = [];
	courseItems.push({
		name: "All Courses",
		to: { name: "course.index" },
	});
	levelTypes.forEach((levelType) => {
		const courseLevels = courseLevelStore.getters.all.value.filter(
			(cl) => cl.study_type === levelType
		);

		courseItems.push({
			name: levelType,
		});

		courseLevels.forEach((courseLevel) => {
			courseItems.push({
				name: courseLevel.name,
				items: courses
					.filter(
						(course) => course.course_level.id === courseLevel.id
					)
					.map((course) => {
						return {
							name: course.name,
							to: {
								name: "course.show",
								params: { id: course.id },
							},
						};
					}),
			});
		});
	});

	items.push({
		name: "Courses",
		items: courseItems,
	});

	navItems.value = items;
};

onMounted(async () => {
	const promises = [];
	if (courseLevelStore.state.shouldLoadAll()) {
		promises.push(courseLevelStore.actions.getAll());
	}

	if (courseStore.state.shouldLoadAll()) {
		promises.push(courseStore.actions.getAll());
	}

	await Promise.all(promises);

	createNavItems();
});

const route = useRoute();
</script>

<template>
	<div class="navbar-wrapper bg-primary-bg shadow-md">
		<div
			class="nebula-nav container flex justify-between items-center py-4">
			<RouterLink
				to="/"
				class="flex py-2 gap-2 justify-center items-center">
				<div class="logo w-8 h-8"></div>
				<span class="site-name text-3xl text-primary-active"
					>Nebula</span
				>
			</RouterLink>
			<nav class="nebula-nav__links flex items-center justify-center">
				<div v-for="item in navItems">
					<Dropdown>
						<template #button-content>
							<span>{{ item.name }}</span>
						</template>
						<template #dropdown-content>
							<NavDropdown
								:items="(item.items as MenuItem[])"
								direction="left"
								v-if="item.items" />
						</template>
					</Dropdown>
				</div>
			</nav>
		</div>
	</div>
</template>

<style scoped lang="scss">
.logo {
	background-image: url("/images/mark.svg");
	background-size: cover;
	background-repeat: no-repeat;
	background-position: center;
}
</style>
