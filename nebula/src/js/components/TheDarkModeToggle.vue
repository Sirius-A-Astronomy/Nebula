<script setup lang="ts">
import { useDark, useToggle } from "@vueuse/core";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faLightbulb as faLightbulbSolid } from "@fortawesome/free-solid-svg-icons";

import { faLightbulb as faLightbulbStroke } from "@fortawesome/free-regular-svg-icons";

const isDark = useDark();
const toggleDark = useToggle(isDark);
</script>

<template>
    <button
        class="flex flex-row items-center justify-center"
        @click="() => toggleDark()"
        :title="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
    >
        <FontAwesomeIcon
            :icon="isDark ? faLightbulbStroke : faLightbulbSolid"
            class="h-4 w-4 transition-transform duration-300 ease-in-out"
        />
    </button>
</template>

<style lang="scss" scoped></style>
