<script setup lang="ts">
defineProps<{
  width?: string;
  height?: string;
}>();
</script>

<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="currentcolor"
    :width="width ?? '24'"
    :height="height ?? '24'"
    viewBox="0 0 24 24"
  >
    <path d="m12 20-8-8 8-8 1.425 1.4-5.6 5.6H20v2H7.825l5.6 5.6Z" />
  </svg>
</template>

<style lang="scss" scoped></style>
