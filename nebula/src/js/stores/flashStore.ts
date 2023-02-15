import { ref } from "vue";

type FlashMessage = {
    id: number;
    message: string;
    type: string;
    timeout: number;
};

const flashMessages = ref<FlashMessage[]>([]);
let id = 0;

const addFlashMessage = (
    message: string,
    type: string,
    timeout: number = 5000
) => {
    const nextId = id++;
    const flashMessage: FlashMessage = {
        id: nextId,
        message,
        type,
        timeout,
    };
    flashMessageQueue.push(flashMessage);
    processFlashMessageQueue();
};

const flashMessageQueue: FlashMessage[] = [];

const MAX_CONCURRENT_FLASH_MESSAGES = 3;

const processFlashMessageQueue = () => {
    if (flashMessages.value.length >= MAX_CONCURRENT_FLASH_MESSAGES) return;
    if (flashMessageQueue.length === 0) return;
    const flashMessage = flashMessageQueue.shift();
    if (!flashMessage) return;
    flashMessages.value.push(flashMessage);
    if (flashMessage.timeout === 0) return;
    setTimeout(() => {
        removeFlashMessage(flashMessage.id);
        processFlashMessageQueue();
    }, flashMessage.timeout);
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
