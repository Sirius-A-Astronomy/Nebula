import { authenticatedUser, isAuthenticated } from "@/stores/sessionStore";
import questionStore, { type Comment } from "@stores/questionStore";
import { getAccessLevelValue } from "@stores/userStore";

export const canEditQuestion = async (questionId: string) => {
    const user = authenticatedUser.value;
    if (!user || !isAuthenticated.value) {
        return false;
    }

    if (user.access_level >= getAccessLevelValue("admin")) {
        return true;
    }

    let question = questionStore.getters.byId(questionId).value;
    if (!question) {
        const response = await questionStore.actions.getById(questionId);
        if (!response.ok) {
            return false;
        }
        question = response.data;
    }

    if (user.id === question.user.id) {
        return true;
    }

    return false;
};

export const canCreateQuestion = () => {
    const user = authenticatedUser.value;
    if (!user || !isAuthenticated.value) {
        return false;
    }

    if (user.access_level >= getAccessLevelValue("moderator")) {
        return true;
    }

    return true;
};

export const canEditComment = (comment: Comment) => {
    const user = authenticatedUser.value;
    if (!user || !isAuthenticated.value) {
        return false;
    }

    if (user.access_level >= getAccessLevelValue("admin")) {
        return true;
    }

    if (user.id === comment.user.id) {
        return true;
    }

    return false;
};
