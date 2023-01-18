<script setup lang="ts">
import { ref } from "vue";
import { vClickOutside } from "@/vue-services/directives/clickOutside";

defineProps<{
	direction?: "below" | "above" | "left" | "right";
	align?: "start" | "end";
	openOnHover?: boolean;
}>();
const isOpen = ref(false);

const toggle = () => {
	console.log("toggle", isOpen.value);
	isOpen.value = !isOpen.value;
};

const close = () => {
	isOpen.value = false;
};

const dropdownId = ref(Math.random().toString(36).slice(8));
</script>

<template>
	<div class="dropdown" :id="`dropdown-${dropdownId}`">
		<div
			:class="{ 'dropdown__trigger--hover': !openOnHover }"
			class="dropdown__trigger">
			<slot
				name="trigger"
				:toggle="toggle"
				:close="close"
				:isOpen="isOpen">
				<button
					v-if="!$slots.button"
					class="dropdown__button"
					@click.stop="toggle"
					@keydown.escape="close"
					v-click-outside="{
						handler: close,
						exclude: `dropdown-${dropdownId}`,
					}"
					aria-label="Profile Menu"
					aria-haspopup="true"
					id="dropdown-button"
					:aria-expanded="isOpen">
					<slot name="button-content"></slot>

					<svg
						xmlns="http://www.w3.org/2000/svg"
						height="24"
						fill="currentColor"
						class="icon transition-transform"
						:class="`icon--${direction ?? 'below'}`"
						width="24">
						<path
							d="m12 15.375-6-6 1.4-1.4 4.6 4.6 4.6-4.6 1.4 1.4Z" />
					</svg>
				</button>
			</slot>
		</div>

		<div
			class="dropdown__menu"
			:class="`
        dropdown__menu--${direction ?? 'below'} dropdown__menu--${
				align ?? 'start'
			}
        ${isOpen ? 'dropdown__menu--open' : ''}
        `">
			<div
				class="dropdown-menu__content px-2 text-secondary-text bg-secondary-bg rounded-md z-10">
				<slot
					name="dropdown-content"
					:toggle="toggle"
					:close="close"
					:isOpen="isOpen">
				</slot>
			</div>
		</div>
	</div>
</template>

<style lang="scss" scoped>
.dropdown {
	position: relative;
	display: inline-block;

	// trigger opening on hover
	&:has(
			.dropdown__trigger--hover:hover,
			.dropdown__menu:hover,
			.dropdown__menu--open
		) {
		& > .dropdown__menu {
			opacity: 1;
			pointer-events: auto;
			visibility: visible;

			&--below,
			&--above {
				transform: translateY(0);
			}

			&--left,
			&--right {
				transform: translateX(0);
			}
		}

		& > .dropdown__trigger > .dropdown__button {
			.icon {
				&--below {
					transform: rotate(0deg);
				}

				&--left {
					transform: rotate(90deg);
				}

				&--right {
					transform: rotate(-90deg);
				}

				&--above {
					transform: rotate(180deg);
				}
			}
		}
	}

	&__button {
		display: flex;
		align-items: center;
		justify-content: center;

		.icon {
			transition: transform 0.1s ease-in-out;

			&--below {
				transform: rotate(-180deg);
			}

			&--left {
				transform: rotate(0deg);
			}

			&--right {
				transform: rotate(0deg);
			}

			&--above {
				transform: rotate(0deg);
			}
		}
	}
}
.dropdown__menu {
	position: absolute;
	transition: opacity 0.1s ease-in-out, transform 0.1s ease-in-out;
	opacity: 0;
	pointer-events: none;
	width: max-content;
	max-width: 20rem;
	visibility: hidden;

	&--below {
		top: 100%;
		transform: translateY(-0.5rem);
	}

	&--above {
		bottom: 100%;
		transform: translateY(0.5rem);
	}

	&--left {
		right: 100%;
		transform: translateX(0.5rem);
	}

	&--right {
		left: 100%;
		transform: translateX(-0.5rem);
	}

	&--below,
	&--above {
		padding: 0.5rem 0;

		&.dropdown__menu--start {
			left: 0;
		}

		&.dropdown__menu--end {
			right: 0;
		}
	}

	&--left,
	&--right {
		padding: 0 0.5rem;

		&.dropdown__menu--start {
			top: 0;
		}

		&.dropdown__menu--end {
			bottom: 0;
		}
	}
}
</style>
