<script setup lang="ts">
import { onMounted } from "vue";

import { courseStore } from "@stores/courseStore";
import { courseLevelStore } from "@/stores/courseLevelStore";
import { computed } from "@vue/reactivity";
import Dropdown from "./Dropdown.vue";
import { useRoute } from "vue-router";

const courseLevels = courseLevelStore.getters.all;

onMounted(() => {
	courseLevelStore.actions.getAll();
	courseStore.actions.getAll();
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
				<ul>
					<li class="nav-item dropdown">
						<a
							class="nav-link dropdown-toggle"
							href="#"
							id="navbarDropdown"
							role="button"
							data-bs-toggle="dropdown"
							aria-expanded="false">
							Courses
						</a>
						<ul
							class="dropdown-menu"
							aria-labelledby="navbarDropdown">
							<li>
								<RouterLink
									:to="{
										name: 'course.index',
									}"
									>All Courses</RouterLink
								>
							</li>
							<template
								v-for="levelType in ['Bachelor', 'Master']">
								<span>{{ levelType }}</span>

								<li
									class="caret-hover"
									v-for="courseLevel in courseLevels.filter(
										(level) =>
											level.study_type === levelType
									)">
									<RouterLink
										:to="{
											name: 'course.level.show',
											params: {
												id: courseLevel.id,
											},
										}"
										>{{ courseLevel.name }}</RouterLink
									>
									<ul class="dropdown-submenu">
										<li
											v-for="course in courseStore.getters.byCourseLevelId(
												courseLevel.id
											).value">
											<RouterLink
												:to="{
													name: 'course.show',
													params: { id: course.id },
												}"
												class="dropdown-item"
												>{{ course.name }}</RouterLink
											>
										</li>
									</ul>
								</li>
							</template>
						</ul>
					</li>
				</ul>

				<!-- <Dropdown direction="below" align="end">
					<template #button-content>
						<span
							class="text-secondary-text text-2xl hover:text-primary-text"
							:class="{
                            'text-primary-active': (route.name as string ?? '').startsWith('course')
                        }"
							>Courses</span
						>
					</template>

					<template #dropdown-content>
						<div class="flex flex-col gap-2">
							<RouterLink
								:to="{
									name: 'course.index',
								}"
								class="px-2 py-1"
								:class="{
									'text-primary-active':
										route.name === 'courses',
								}">
								<span class="text-secondary-text text-xl"
									>All</span
								>
							</RouterLink>
							<span class="text-tertiary-text text-base px-2 py-1"
								>Bachelor</span
							>

							<Dropdown
								direction="left"
								v-for="courseLevel in courseLevels.filter(
									(courseLevel) =>
										courseLevel.study_type === 'Bachelor'
								)"
								class="flex flex-col gap-2">
								<template #button-content>
									<span
										class="text-secondary-text text-xl px-2 py-1"
										>{{ courseLevel.name }}</span
									>
								</template>

								<template #dropdown-content>
									<div class="flex flex-col gap-2">
										<RouterLink
											v-for="course in courseStore.getters.byCourseLevelId(
												courseLevel.id
											).value"
											:key="course.id"
											:to="{
												name: 'course.show',
												params: {
													id: course.id,
												},
											}"
											class="text-secondary-text text-base px-2 py-1"
											>{{ course.name }}</RouterLink
										>
									</div>
								</template>
							</Dropdown>
						</div>
					</template>
				</Dropdown> -->
			</nav>
		</div>
	</div>
</template>

<style lang="scss" scoped>
.logo {
	background-image: url("/images/mark.svg");
	background-size: cover;
	background-repeat: no-repeat;
}

.navbar {
	display: flex;
	background-color: var(--color-background);
	box-shadow: var(--box-shadow);
	z-index: 10;
}

@media (hover: hover) and (min-width: 992px) {
	.nav-item {
		&:hover,
		&:focus {
			.dropdown-menu {
				display: block;
			}
		}
	}

	.carot-left:after,
	.dropdown-menu > li > a:hover:after,
	.dropdown-menu > li > a:focus:after {
		/* rotate caret on hover */
		transform: rotate(-90deg);
	}
	.dropdown-menu {
		display: none;
		margin-top: 0;
		position: absolute;

		.dropdown-submenu {
			display: none;
			position: absolute;
			left: 100%;
			top: 0px;
		}

		li {
			position: relative;

			&:hover,
			&:focus {
				.dropdown-submenu {
					display: block;
				}
			}

			a:hover::after,
			a:focus::after,
			.carot-left:after {
				transform: rotate(-90deg);
			}
		}
	}
}

.nav-link {
	font-family: "Poppins", "Open Sans", "Arial", sans-serif;
	font-style: normal;
	font-weight: 400;
	font-size: 1.25rem;
	line-height: 2rem;

	color: var(--color-text-secondary) !important;

	&:hover,
	&:focus {
		color: var(--color-text-primary) !important;
	}

	&.active {
		color: var(--color-primary-active) !important;
		font-weight: 600;
	}
}

.navbar-toggler {
	border-color: var(--color-text-secondary) !important;
	border: none !important;
	padding: 0 !important;

	&:hover,
	&:focus {
		border-color: var(--color-text-primary) !important;
	}
	svg {
		color: var(--color-text-secondary) !important;
		&:hover,
		&:focus {
			color: var(--color-text-primary) !important;
		}
	}
}

.site-name {
	font-family: "Poppins", "Open Sans", "Arial", sans-serif;
	font-size: 2rem;
	// line-height: 3rem;
	-moz-osx-font-smoothing: grayscale;
	-webkit-font-smoothing: antialiased;
	font-weight: 400;
	letter-spacing: -0.04rem;
	color: var(--color-primary-active);
}

.navbar-brand {
	img {
		display: inline-block;
		max-height: 3.125rem;
	}

	.logo {
		color: var(--color-primary-active);
		height: 4rem;
		width: 4rem;
		background: url("/images/mark.svg") no-repeat center center;
	}

	div {
		display: inline-block;
		vertical-align: middle;

		p {
			margin-bottom: 0;
			font-size: 65%;
		}
	}
}

.dropdown-menu {
	border-radius: 0;
	border: 0 solid transparent;
	border-bottom: 2px solid var(--color-secondary);
	padding: 0;
	background-color: var(--color-background);
	color: var(--color-text-primary);
	overflow: visible;
	margin-top: 0 !important;

	&-right {
		right: 0;
		left: initial !important;
	}

	& .active {
		text-decoration: underline;
		color: inherit;
		background-color: var(--color-background);
		color: var(--color-text-secondary);
	}
}

.dropdown-submenu {
	border-radius: 0;
	border: 0 solid transparent;
	color: var(--color-text-primary);
	border-bottom: 2px solid var(--color-primary-active);
	padding: 0;
	background-color: var(--color-background);
}

.dropdown-submenu li {
	list-style: none;
}

.dropdown-item {
	padding-top: 10px;
	padding-bottom: 10px;
	transition: background-color 0.15s;
	color: var(--color-text-primary);
}

.dropdown-item:hover,
.dropdown-item:focus {
	background-color: var(--color-background-secondary);
	color: var(--color-text-primary);
}

.dropdown-menu .dropdown-submenu {
	display: none;
}

.nav-header {
	font-weight: 200;
	margin-left: 0.5em;
}

/* check if a device supports :hover */
@media (hover: hover) {
	:root {
		--has-hover: 1;
	}
}

@media (max-width: 991px) {
	/* .navbar-nav>li>a:after, */
	.dropdown-menu > li > a:after {
		transform: rotate(-90deg);
	}

	/* .navbar-nav>li>a:focus:after, */
	.dropdown-menu > li > a:focus:after {
		transform: rotate(0);
	}

	.dropdown-menu .dropdown-submenu {
		margin-left: 0.5em;
		border: 0;
	}

	.dropdown-submenu,
	.dropdown-item {
		max-width: #{"calc(100vw - 2rem)"};
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
}

@media (hover: none) and (min-width: 992px) {
	:root {
		--has-hover: 0;
	}

	.dropdown-menu .dropdown-submenu {
		display: none;
		position: absolute;
		left: 100%;
		top: 0px;
	}

	.dropdown-menu li {
		position: relative;

		/* rotate caret on hover */
		a:focus:after {
			transform: rotate(-90deg);
		}
	}
}

.persistent-nav-container {
	color: var(--color-text-primary);
	margin-inline-start: auto;
	display: flex;
	.dark-mode-toggle-container {
		vertical-align: middle;
		margin-left: auto;
		display: grid;
		place-items: center;
		padding: 0.5rem;
	}

	.account-management-dropdown {
		padding: 0.5rem;
		display: flex;
		align-items: center;
		justify-content: center;

		span {
			display: none;

			@media (min-width: 992px) {
				display: inline;
			}
		}
	}
}
.main-title {
	/* font-size: 3rem; */
	margin-bottom: 1rem;
}

@media all and (min-width: 992px) {
	.persistent-nav-container {
		order: 2;
		margin-right: 0;
	}
	.account-management-dropdown {
		order: 2;
	}
}

.dark-mode-icon,
.light-mode-icon {
	display: none;
	color: var(--color-text-secondary);
}

.dark-mode-icon:hover,
.light-mode-icon:hover {
	color: var(--color-text-primary);
}

.animate-rotation .dark-mode-icon,
.animate-rotation .light-mode-icon {
	animation: rotation 0.2s ease-out;
}
.dark-mode-toggle-container .dark-mode-enabled .dark-mode-icon {
	display: none;
}

.dark-mode-toggle-container .dark-mode-enabled .light-mode-icon {
	display: block;
}

.dark-mode-toggle-container .light-mode-enabled .dark-mode-icon {
	display: block;
}

.dark-mode-toggle-container .light-mode-enabled .light-mode-icon {
	display: none;
}

@keyframes rotation {
	from {
		transform: rotate(0deg);
	}
	to {
		transform: rotate(360deg);
	}
}
.notifications {
	position: relative;

	&__toggle {
		padding: 0.5rem;
		display: grid;
		place-items: center;
		height: 100%;
		color: var(--color-text-secondary);

		&:hover,
		&:focus {
			color: var(--color-text-primary);
		}

		&.unread {
			color: var(--color-primary-active);

			&::after {
				content: attr(data-unread-count);
				position: absolute;
				display: flex;
				font-family: "Lato", "Roboto", "Arial", sans-serif;
				justify-content: center;
				align-items: center;
				text-align: center;
				top: 10%;
				right: 0;
				width: 1.2rem;
				height: 1.2rem;
				font-size: 0.875rem;
				border-radius: 50%;
				background-color: var(--color-primary-active);
				color: var(--color-background);
			}
		}
	}

	&__list {
		display: none;
		position: absolute;
		z-index: 900;
		top: 4rem;
		left: 50%;
		transform: translateX(-50%);
		width: min(80vw, 500px);
		margin-left: auto;
		margin-right: auto;

		background-color: var(--color-background-secondary);
		border-radius: 0.5rem;
		box-shadow: var(--box-shadow);

		&--active {
			display: block;
		}

		&__header {
			padding: 0.5rem;
			&__title {
				font-size: 1.3rem;
				font-weight: 200;
			}
		}

		&__no-notifications {
			padding: 0.5rem;
			text-align: center;
			font-size: 1.2rem;
			font-weight: 200;
		}

		&__item {
			padding: 0.5rem;
			font-weight: 300;
			display: grid;
			align-items: flex-start;

			&__category {
				grid-row: 1 / span 1;
				grid-column: 1 / span 1;
				width: 1.2rem;
				height: 1.2rem;
				border-radius: 50%;
				align-self: center;
				border: 4px solid var(--color-text-primary);

				&.success {
					border-color: var(--color-alert-success);
				}

				&.warning {
					border-color: var(--color-alert-warning);
				}

				&.error {
					border-color: var(--color-alert-error);
				}

				&.info {
					border-color: var(--color-alert-info);
				}
			}
			&.unread {
				font-weight: 400;

				& .notifications__list__item__category {
					background-color: var(--color-accent);
				}
			}

			&:last-of-type {
				border-radius: 0 0.5rem 0.5rem 0;
			}

			&__content {
				grid-row: 1 / span 1;
				grid-column: 2 / span 1;
				padding-left: 0.5rem;
			}

			&__actions {
				grid-row: 2 / span 1;
				grid-column: 2 / span 1;
				text-align: right;
				padding-right: 0.5rem;

				font-weight: 500;
			}
		}
	}
}
</style>
