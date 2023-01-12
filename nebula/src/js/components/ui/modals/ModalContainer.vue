<script setup lang="ts">
import { computed } from "vue";
import useModalStore from "@stores/modalStore";
import CloseIcon from "@components/icons/Close.vue";

const modal = useModalStore();

const currentModal = computed(() => {
	if (modal.modals.value.length === 0) return null;
	return modal.modals.value[0];
});

const executeAction = (action: any) => {
	const actionModal = currentModal.value;
	if (!actionModal) return;
	modal.remove({ id: actionModal.id });
	action.action?.();
};
</script>

<template>
	<div
		class="fixed bg-black bg-opacity-20 w-screen h-screen z-50"
		v-if="currentModal">
		<div class="flex items-center justify-center w-full h-full">
			<div
				class="bg-primary-bg w-96 px-4 py-2 relative rounded-md shadow-lg flex flex-col gap-2"
				v-if="currentModal">
				<div class="flex flex-row justify-between items-start w-full">
					<h1 class="text-2xl">{{ currentModal.title }}</h1>
					<button
						class="bg-secondary-bg shadow-sm text-primary-text rounded-sm font-bold hover:text-primary-text flex items-center justify-center"
						@click="modal.remove({ id: currentModal!.id })">
						<CloseIcon height="20" width="20" />
					</button>
				</div>
				<p>{{ currentModal.body }}</p>
				<div class="flex flex-row justify-between gap-4">
					<div class="positive-actions">
						<button
							v-for="action in currentModal.actions?.filter(
								(action) =>
									['positive', 'danger', 'warning'].includes(
										action.type ?? ''
									)
							)"
							class="px-4 py-2 rounded-md font-bold hover:font-bold"
							:class="{
								'bg-alert-warning text-alert-warning-text':
									action.type === 'warning' ||
									action.type === 'danger',
								'bg-alert-success text-alert-success-text':
									action.type === 'positive',
							}"
							@click="executeAction(action)">
							{{ action.text }}
						</button>
					</div>

					<div>
						<button
							v-for="action in currentModal.actions?.filter(
								(action) =>
									['negative', 'neutral'].includes(
										action.type ?? 'neutral'
									)
							)"
							class="px-4 py-2 rounded-md font-bold hover:shadow-md"
							:class="{
								'bg-alert-warning text-alert-warning-text':
									action.type === 'negative',
								'bg-alert-info text-alert-info-text':
									action.type === 'neutral',
							}"
							@click="executeAction(action)">
							{{ action.text }}
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<style lang="scss" scoped></style>
