const API_URL = "";

let CSRF_TOKEN = "";

export const setCSRFToken = (token: string): void => {
  CSRF_TOKEN = token;
};

type SendRequestResponse<T = unknown> =
  | {
      ok: true;
      status: number;
      data: T;
      message?: string;
    }
  | {
      ok: false;
      status: number;
      message: string;
      data?: T;
    };

const sendRequest = async <T, TBody = unknown>(
  url: string,
  method: string,
  body: TBody,
  params: Record<string, string>
): Promise<SendRequestResponse<T>> => {
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
        ok: response.ok,
        message: json.message,
        data: json,
      };
    } catch (e) {
      return {
        status: response.status,
        ok: false,
        message: response.statusText,
      };
    }
  } catch (error) {
    console.log("error", error);
    return {
      status: 500,
      message: "Couldn't connect to server",
      ok: false,
    };
  }
};

const get = async <T>(url: string, params: Record<string, string> = {}) => {
  return await sendRequest<T>(url, "GET", null, params);
};

const post = async <T, TBody = unknown>(
  url: string,
  body: TBody,
  params: Record<string, string> = {}
) => {
  return await sendRequest<T, TBody>(url, "POST", body, params);
};

const put = async <T, TBody>(
  url: string,
  body: TBody,
  params: Record<string, string> = {}
) => {
  return await sendRequest<T, TBody>(url, "PUT", body, params);
};

const del = async <T>(url: string, params: Record<string, string> = {}) => {
  return await sendRequest<T>(url, "DELETE", null, params);
};

export default {
  get: get,
  post: post,
  put: put,
  delete: del,
};
