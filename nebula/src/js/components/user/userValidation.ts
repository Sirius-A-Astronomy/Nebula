import api from "@http/api";

export const isUsernameAvailable = async (username: string) => {
	let valid_username = true;

	const response = await api.post("/api/is_username_available", {
		username: username,
	});

	if (response.status === 200) {
		const data = response.data as { available: boolean };
		valid_username = data.available;
	}

	return valid_username;
};

export const validateUsername = async (
	username: string
): Promise<{ valid: boolean; message: string }> => {
	if (username.length < 3) {
		return {
			valid: false,
			message: "Please enter a username with at least 3 characters",
		};
	}

	if (username.length >= 30) {
		return {
			valid: false,
			message: "Please enter a username with at most 30 characters",
		};
	}

	if (/\s/.test(username)) {
		return {
			valid: false,
			message: "Please enter a username without any spaces",
		};
	}

	var regex = /[ @()+=\[\]{};':"\\|,.<>\/?]/g;
	if (regex.test(username)) {
		return {
			valid: false,
			message: "Please enter a username without any special characters",
		};
	}

	let usernameAvailable = await isUsernameAvailable(username);
	if (!usernameAvailable) {
		return {
			valid: false,
			message:
				"It looks like we already know someone with that username, do you want to try another one?",
		};
	}

	return {
		valid: true,
		message: "",
	};
};

export const validatePassword = (
	password: string,
	passwordConfirmation: string
): {
	valid: boolean;
	message: string;
} => {
	if (password.length < 12) {
		return {
			valid: false,
			message: "Please enter a password with at least 12 characters",
		};
	}

	// validate password confirmation on input of password
	if (
		passwordConfirmation.length >= 12 &&
		password !== passwordConfirmation
	) {
		return {
			valid: false,
			message: "Please double check that your passwords match",
		};
	}
	return {
		valid: true,
		message: "",
	};
};

export const validatePasswordConfirmation = (
	password: string,
	passwordConfirmation: string
): {
	valid: boolean;
	message: string;
} => {
	if (!validatePassword(password, passwordConfirmation).valid) {
		return {
			valid: false,
			message: "Please enter a valid password first",
		};
	}
	if (password !== passwordConfirmation) {
		return {
			valid: false,
			message: "Please double check that your passwords match",
		};
	}
	return {
		valid: true,
		message: "",
	};
};

export const validateEmail = (
	email: string
): {
	valid: boolean;
	message: string;
} => {
	// rfc2822 regex for emails
	const emailRegex =
		/(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/;
	if (!emailRegex.test(email)) {
		return {
			valid: false,
			message:
				"We can't recognize that as an email address quite yet, please double check it",
		};
	}
	return {
		valid: true,
		message: "",
	};
};
