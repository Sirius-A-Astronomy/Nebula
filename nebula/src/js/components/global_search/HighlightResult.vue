<script setup lang="ts">
import DOMPurify from "dompurify";
import fuzzysort from "fuzzysort";
import { computed } from "vue";

const props = defineProps<{
  result: Fuzzysort.Result;
  fallback?: string;
  highlightClass?: string;
}>();

const html = computed(() => {
  if (!props.result) {
    return props.fallback;
  }
  return DOMPurify.sanitize(
    fuzzysort.highlight(
      props.result,
      `<span class=${props.highlightClass}>`,
      "</span>"
    ) as string,
    { ALLOWED_TAGS: ["span"] }
  );
});
</script>

<template>
  <span v-html="html" />
</template>
