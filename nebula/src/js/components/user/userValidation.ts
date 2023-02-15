import api from "@http/api";

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
        message: "Looks good!",
    };
};

export const validatePasswordConfirmation = (
    password: string,
    passwordConfirmation: string
): {
    valid: boolean;
    message: string;
} => {
    if (passwordConfirmation.length < 12) {
        return {
            valid: false,
            message: "",
        };
    }

    const { valid, message } = validatePassword(password, passwordConfirmation);
    if (!valid) {
        return {
            valid: false,
            message: message,
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
        message: "Looks good!",
    };
};

export const validateEmail = async (
    email: string
): Promise<{
    valid: boolean;
    message: string;
}> => {
    // rfc2822 regex for emails
    const emailRegex =
        // eslint-disable-next-line no-control-regex -- this is a regex for emails from rfc2822, it contains valid control characters
        /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/;
    if (!emailRegex.test(email)) {
        return {
            valid: false,
            message:
                "We can't recognize that as an email address quite yet, please double check it",
        };
    }

    const response = await api.post<{
        valid: boolean;
        message: string;
    }>("/users/validate/email", {
        email: email,
    });

    if (response.ok && response.data.valid === false) {
        return {
            valid: false,
            message: response.data.message,
        };
    }

    return {
        valid: true,
        message: "Looks good!",
    };
};

export const validateFirstName = (
    firstName: string
): {
    valid: boolean;
    message: string;
} => {
    if (firstName.length < 1) {
        return {
            valid: false,
            message: "Please enter your first name",
        };
    }
    return {
        valid: true,
        message: "Looks good!",
    };
};

export const validateLastName = (
    lastName: string
): {
    valid: boolean;
    message: string;
} => {
    if (lastName.length < 1) {
        return {
            valid: false,
            message: "Please enter your last name",
        };
    }
    return {
        valid: true,
        message: "Looks good!",
    };
};
