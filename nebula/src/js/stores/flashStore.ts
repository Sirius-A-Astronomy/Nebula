import { ref } from "vue";

type FlashMessage = {
	id: number;
	message: string;
	type: string;
	timeout: number;
};

const flashMessages = ref<FlashMessage[]>([]);

const addFlashMessage = (
	message: string,
	type: string,
	timeout: number = 3000
) => {
	const nextId =
		flashMessages.value.reduce(
			(maxId, flashMessage) =>
				flashMessage.id > maxId ? flashMessage.id : maxId,
			-1
		) + 1;
	flashMessages.value.push({ id: nextId, message, type, timeout });
	if (timeout === 0) return;
	setTimeout(() => {
		removeFlashMessage(nextId);
	}, timeout);
};

const removeFlashMessage = (id: number) => {
	flashMessages.value = flashMessages.value.filter(
		(flashMessage) => flashMessage.id !== id
	);
};

export default () => ({
	messages: flashMessages,
	add: addFlashMessage,
	remove: removeFlashMessage,
});
