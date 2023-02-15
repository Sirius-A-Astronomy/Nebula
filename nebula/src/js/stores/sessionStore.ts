import { computed, ref } from "vue";

import api from "@http/api";

import type { User } from "@stores/userStore";

export const authenticatedUser = ref({} as User);

export const isAuthenticated = computed(() => {
    return authenticatedUser.value.id !== undefined;
});

type FetchUserResponse = {
    status: number;
    data?: User;
    message?: string;
};

export const fetchUser = async (): Promise<FetchUserResponse> => {
    const response = await api.get("/me");
    if (response.status === 200) {
        authenticatedUser.value = response.data as User;
    } else {
        authenticatedUser.value = {} as User;
    }
    return response as FetchUserResponse;
};

export class FetchUserFailedError extends Error {
    constructor() {
        super("Failed to fetch user");
    }
}

export const logout = async () => {
    const response = await api.post("/logout", {});
    authenticatedUser.value = {} as User;
    return response;
};

export const login = async (values: { email: string; password: string }) => {
    const response = await api.post<{ user: User }>("/login", {
        email: values.email,
        password: values.password,
    });
    if (response.ok) {
        authenticatedUser.value = response.data.user;
    }
    return response;
};

export const register = async (values: {
    email: string;
    password: string;
    passwordConfirmation: string;
    first_name: string;
    last_name: string;
}) => {
    const response = await api.post<User>("/users", {
        email: values.email,
        password: values.password,
        password_confirmation: values.passwordConfirmation,
        first_name: values.first_name,
        last_name: values.last_name,
    });
    return response;
};
