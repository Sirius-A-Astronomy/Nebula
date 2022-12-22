<script setup lang="ts">
import { ref } from "vue";

const count = ref(0);

function increment() {
	count.value++;
}
</script>

<template>
	<div>
		<p>Count is: {{ count }}</p>
		<button @click="increment">Increment</button>
	</div>
</template>

<style lang="scss" scoped></style>
