import { ref } from "vue";

type Modal = {
    id: number;
    name?: string;
    title: string;
    body?: string;
    actions?: ModalAction[];
    type?: ModalType;
};

type New<T> = Omit<T, "id">;

type ModalAction = {
    text: string;
    action?: () => void;
    type?: ModalActionType;
};

type ModalActionType =
    | "positive"
    | "negative"
    | "neutral"
    | "danger"
    | "warning";

type ModalType = "alert" | "confirm";

const modals = ref<Modal[]>([]);
let id = 0;

const useModalStore = () => {
    const add = (modal: New<Modal>) => {
        modals.value.push({ ...modal, id: id++ });
    };

    const remove: (modalId: { id: number } | { name: string }) => void = (
        modalId
    ) => {
        if ("id" in modalId) {
            const id = modalId.id;
            modals.value = modals.value.filter((modal) => modal.id !== id);
            return;
        }
        const name = modalId.name;
        modals.value = modals.value.filter((modal) => modal.name !== name);
    };

    return {
        modals,
        add,
        remove,
    };
};

export default useModalStore;
