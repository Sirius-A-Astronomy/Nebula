<script setup lang="ts">
import { ref, watch } from "vue";
import { vClickOutside } from "@/vue-services/directives/clickOutside";

const props = defineProps<{
    direction?: "below" | "above" | "left" | "right";
    align?: "start" | "end" | "center";
    openOnHover?: boolean;
    shouldClose?: boolean;
}>();
const isOpen = ref(false);

watch(
    () => props.shouldClose,
    (shouldClose) => {
        if (shouldClose) {
            close();
        }
    }
);

const toggle = () => {
    if (!isOpen.value) emit("closeSiblings");
    isOpen.value = !isOpen.value;
};

const forceCloseRef = ref(false);

const emit = defineEmits<{
    (event: "close", ...args: any[]): void;
    (event: "closeSiblings", ...args: any[]): void;
}>();

const closeParent = () => {
    isOpen.value = false;
    forceCloseRef.value = true;
    setTimeout(() => {
        forceCloseRef.value = false;
    }, 100);
    emit("close");
};

const close = () => {
    isOpen.value = false;
};

const dropdownId = ref(Math.random().toString(36).slice(8));
</script>

<template>
    <div class="dropdown" :id="`dropdown-${dropdownId}`">
        <div
            :class="{
                'dropdown__trigger--hover': !openOnHover,
                'dropdown__menu--open': isOpen,
            }"
            class="dropdown__trigger"
        >
            <slot
                name="trigger"
                :toggle="toggle"
                :close="close"
                :isOpen="isOpen"
            >
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
                    :aria-expanded="isOpen"
                >
                    <slot name="button-content"></slot>

                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        height="24"
                        fill="currentColor"
                        class="icon transition-transform"
                        :class="`icon--${direction ?? 'below'}`"
                        width="24"
                    >
                        <path
                            d="m12 15.375-6-6 1.4-1.4 4.6 4.6 4.6-4.6 1.4 1.4Z"
                        />
                    </svg>
                </button>
            </slot>
            <div
                class="dropdown__menu"
                :class="`
        dropdown__menu--${direction ?? 'below'} dropdown__menu--${
                    align ?? 'start'
                }
      ${forceCloseRef ? 'dropdown__menu--force-close' : ''}
        ${isOpen ? 'dropdown__menu--open' : ''}
        `"
            >
                <div
                    class="dropdown-menu__content z-10 rounded-md bg-secondary-bg px-2 text-secondary-text"
                >
                    <slot
                        name="dropdown-content"
                        :toggle="toggle"
                        :close="close"
                        :closeParent="closeParent"
                        :isOpen="isOpen"
                    >
                    </slot>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.dropdown {
    position: relative;
    display: inline-block;

    // trigger opening on hover
    .dropdown__menu--open,
    .dropdown__trigger--hover:hover,
    .dropdown__menu:hover {
        & > .dropdown__menu {
            opacity: 1;
            pointer-events: auto;
            visibility: visible;
            overflow: visible;

            &--below,
            &--above {
                transform: translateY(0);
            }

            &--left,
            &--right {
                transform: translateX(0);
            }
        }

        & > .dropdown__button {
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
        text-align: start;

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
    overflow: hidden;
    z-index: 10;

    &--force-close {
        opacity: 0 !important;
        pointer-events: none !important;
        visibility: hidden !important;
        overflow: hidden !important;
    }

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

        &.dropdown__menu--center {
            left: 50%;
            transform: translateX(-50%);
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

        &.dropdown__menu--center {
            top: 50%;
            transform: translateY(-50%);
        }
    }
}
</style>
