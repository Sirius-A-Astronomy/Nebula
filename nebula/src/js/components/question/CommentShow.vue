<script setup lang="ts">
import type { Comment } from "@stores/questionStore";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import MarkdownDisplay from "@components/MarkdownDisplay.vue";
import MarkdownEditor from "@components/MarkdownEditor.vue";
import { ref } from "vue";
import { canEditComment } from "@/lib/permissionHelpers";

import useFlashStore from "@stores/flashStore";
import useModalStore from "@stores/modalStore";
import { questionStore } from "@stores/questionStore";

const flash = useFlashStore();
const modal = useModalStore();

dayjs.extend(relativeTime);

const props = defineProps<{
    comment: Comment;
}>();

const editableComment = ref({ ...props.comment });

const editMode = ref(false);

const toggleEditMode = () => {
    editMode.value = !editMode.value;

    if (!editMode.value) {
        editableComment.value = { ...props.comment };
    }
};

const onDeleteClicked = () => {
    modal.add({
        title: "Delete Comment",
        body: `Are you sure you want to delete commment '${props.comment.content}'?`,
        actions: [
            {
                text: "Cancel",
                type: "neutral",
            },
            {
                text: "Delete",
                type: "danger",
                action: deleteComment,
            },
        ],
    });
};

const deleteComment = async () => {
    const response = await questionStore.actions.deleteComment(
        props.comment.question_id,
        props.comment.id
    );

    if (!response.ok) {
        flash.add(`Failed to delete comment: ${response.message}`, "error");
        return;
    }

    flash.add(`Comment deleted successfully`, "success");
};

const updateComment = async () => {
    const response = await questionStore.actions.updateComment(
        props.comment.question_id,
        props.comment.id,
        editableComment.value.content
    );

    if (!response.ok) {
        flash.add(`Failed to update comment: ${response.message}`, "error");
        return;
    }

    flash.add(`Comment updated successfully`, "success");
    editMode.value = false;
};
</script>

<template>
    <div
        :key="comment.id"
        class="rounded-lg bg-secondary-bg p-3"
        aria-label="comment card"
    >
        <div class="flex flex-col">
            <div class="flex flex-row justify-between">
                <div class="font-semibold text-tertiary-text">
                    {{ comment.user.first_name }}
                    {{ comment.user.last_name }} &middot;
                    {{ dayjs(comment.meta.created_at).fromNow() }}

                    <span
                        class="md:text-md text-sm"
                        v-if="comment.meta.updated_at"
                    >
                        (Last updated
                        {{ dayjs(comment.meta.updated_at).fromNow() }})
                    </span>
                </div>

                <div v-if="canEditComment(comment)" class="flex flex-row gap-1">
                    <button
                        class="text-blue-500 hover:text-blue-700"
                        @click="toggleEditMode"
                    >
                        {{ editMode ? "Cancel" : "Edit" }}
                    </button>

                    <button
                        class="text-red-500 hover:text-red-700"
                        @click="onDeleteClicked"
                    >
                        Delete
                    </button>
                </div>
            </div>
            <MarkdownDisplay v-if="!editMode" :content="comment.content" />

            <div v-if="editMode">
                <MarkdownEditor
                    v-model="editableComment.content"
                    class="rounded-lg !bg-secondary-bg"
                    placeholder="Enter comment here"
                />
                <div class="flex flex-row justify-end">
                    <button
                        @click="updateComment"
                        class="rounded-lg bg-primary-bg px-4 py-2 text-primary-text"
                    >
                        Save
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped></style>
