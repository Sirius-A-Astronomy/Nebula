import { computed, ref } from "vue";

import api from "@http/api";

export type User = {
	id: string;
	name: string;
	username: string;
	email: string;
	access_level: number;
};

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
