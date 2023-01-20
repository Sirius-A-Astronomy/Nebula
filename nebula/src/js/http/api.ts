const API_URL = "";

let CSRF_TOKEN = "";

export const setCSRFToken = (token: string): void => {
	CSRF_TOKEN = token;
};

type SendRequestResponse = {
	status: number;
	data?: unknown;
	message?: string;
};

const sendRequest = async (
	url: string,
	method: string,
	body: unknown,
	params: Record<string, string>
): Promise<SendRequestResponse> => {
	let full_url = "";
	if (url.startsWith("/")) {
		full_url = API_URL + "/api" + url;
	} else {
		full_url = API_URL + "/api/" + url;
	}
	const fetchUrl = `${full_url}${params ? "?" : ""}${new URLSearchParams(
		params
	)}`;

	const fetchOptions: {
		method: string;
		credentials?: RequestCredentials;
		headers: {
			Authorization?: string;
			"Content-Type": string;
			"X-CSRF-Token"?: string;
		};
		body?: string;
	} = {
		method,
		headers: {
			"Content-Type": "application/json",
			"X-CSRF-Token": CSRF_TOKEN,
		},
	};

	fetchOptions.credentials = "include";

	if (body) {
		fetchOptions.body = JSON.stringify(body);
	}

	try {
		const response = await fetch(fetchUrl, fetchOptions);

		try {
			const json = await response.json();
			return {
				status: response.status,
				message: json.message,
				data: json,
			};
		} catch (e) {
			return {
				status: response.status,
				message: response.statusText,
			};
		}
	} catch (error) {
		console.log("error", error);
		return {
			status: 500,
			message: "Couldn't connect to server",
		};
	}
};

const get = async (url: string, params: Record<string, string> = {}) => {
	return await sendRequest(url, "GET", null, params);
};

const post = async (
	url: string,
	body: unknown,
	params: Record<string, string> = {}
) => {
	return await sendRequest(url, "POST", body, params);
};

const put = async (
	url: string,
	body: unknown,
	params: Record<string, string> = {}
) => {
	return await sendRequest(url, "PUT", body, params);
};

const del = async (url: string, params: Record<string, string> = {}) => {
	return await sendRequest(url, "DELETE", null, params);
};

export default {
	get: get,
	post: post,
	put: put,
	delete: del,
};
