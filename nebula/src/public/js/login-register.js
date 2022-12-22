/*
    Client-side form validation

    Client-side validation was chosen to minimise reloading of the page.
*/

async function isUsernameAvailable(username) {
	let valid_username = true;
	// await $.ajax({
	// 	url: "/api/is_username_available",
	// 	type: "POST",
	// 	data: JSON.stringify({
	// 		username: username,
	// 	}),
	// 	contentType: "application/json",
	// 	dataType: "json",
	// 	success: function (data) {
	// 		valid_username = data.available;
	// 	},
	// 	error: function (data) {
	// 		console.log(data);
	// 	},
	// });
	try {
		const response = await fetch("/api/is_username_available", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": window.CSRF_TOKEN,
			},
			body: JSON.stringify({
				username: username,
			}),
		});
		const data = await response.json();
		valid_username = data.available;
	} catch (error) {
		console.log(error);
	}

	return valid_username;
}

function debounce(callback, wait) {
	let timeout;
	return (...args) => {
		clearTimeout(timeout);
		timeout = setTimeout(function () {
			callback.apply(this, args);
		}, wait);
	};
}

async function startFormValidation() {
	// $("#username-input-field").on("input", debounce(validateUsername, 500));
	// $("#password-confirmation-input-field").on(
	// 	"input",
	// 	debounce(validatePasswordConfirmation, 500)
	// );
	// $("#password-input-field").on("input", debounce(validatePassword, 500));
	// $("#first-name-input-field").on("input", debounce(validateFirstName, 500));
	// $("#last-name-input-field").on("input", debounce(validateLastName, 500));
	// $("#email-input-field").on("input", debounce(validateEmail, 900));

	document
		.getElementById("username-input-field")
		.addEventListener("input", debounce(validateUsername, 500));
	document
		.getElementById("password-confirmation-input-field")
		.addEventListener("input", debounce(validatePasswordConfirmation, 500));
	document
		.getElementById("password-input-field")
		.addEventListener("input", debounce(validatePassword, 500));
	document
		.getElementById("first-name-input-field")
		.addEventListener("input", debounce(validateFirstName, 500));
	document
		.getElementById("last-name-input-field")
		.addEventListener("input", debounce(validateLastName, 500));
	document
		.getElementById("email-input-field")
		.addEventListener("input", debounce(validateEmail, 900));
}

async function validateUsername() {
	let usernameInputField = document.getElementById("username-input-field");
	let username = $(usernameInputField).val();

	if (username.length < 3) {
		addInvalidFeedback(
			usernameInputField,
			"Please enter a username with at least 3 characters"
		);
		return;
	}

	if (username.length >= 30) {
		addInvalidFeedback(
			usernameInputField,
			"Please enter a username with at most 30 characters"
		);
		return;
	}

	if (/\s/.test(username)) {
		addInvalidFeedback(
			usernameInputField,
			"Please enter a username without any spaces"
		);
		return;
	}

	var regex = /[ @()+=\[\]{};':"\\|,.<>\/?]/g;
	if (regex.test(username)) {
		addInvalidFeedback(
			usernameInputField,
			"Please enter a username without any special characters"
		);
		return;
	}

	addValidatingFeedback(
		usernameInputField,
		`Checking if we know someone with username ${username}...`
	);
	let usernameAvailable = await isUsernameAvailable(username);
	if (usernameAvailable) {
		addValidFeedback(usernameInputField, "Looks good!");
	} else {
		addInvalidFeedback(
			usernameInputField,
			"It looks like we already know someone with that username, do you want to try another one?"
		);
	}
}

function validatePassword() {
	let passwordInputField = document.getElementById("password-input-field");
	let password = $(passwordInputField).val();
	let passwordConfirmationInputField = document.getElementById(
		"password-confirmation-input-field"
	);
	let passwordConfirmation = $(passwordConfirmationInputField).val();

	if (password.length < 12) {
		addInvalidFeedback(
			passwordInputField,
			"Please enter a password with at least 12 characters"
		);
		return false;
	}
	addValidFeedback(passwordInputField, "Looks good!");

	// validate password confirmation on input of password
	if (password == passwordConfirmation) {
		addValidFeedback(passwordConfirmationInputField, "Looks good!");
	} else {
		// only give invalid feedback if the password confirmation is long enough to be a match
		if (passwordConfirmation.length >= 12) {
			addInvalidFeedback(
				passwordConfirmationInputField,
				"Please double check that your passwords match"
			);
		}
	}
	return true;
}

function validatePasswordConfirmation() {
	let passwordConfirmationInputField = document.getElementById(
		"password-confirmation-input-field"
	);
	let passwordInputField = document.getElementById("password-input-field");
	let password = $(passwordInputField).val();
	let passwordConfirmation = $(passwordConfirmationInputField).val();

	if (!validatePassword()) {
		addInvalidFeedback(
			passwordConfirmationInputField,
			"Please enter a valid password first"
		);
		return;
	}
	if (password !== passwordConfirmation) {
		addInvalidFeedback(
			passwordConfirmationInputField,
			"Please double check that your passwords match"
		);
	} else {
		addValidFeedback(passwordConfirmationInputField, "Looks good!");
	}
}

function validateFirstName() {
	let firstNameInputField = document.getElementById("first-name-input-field");
	let firstName = $(firstNameInputField).val();

	if (firstName.length < 1) {
		addInvalidFeedback(firstNameInputField, "Please enter your first name");
		return;
	}

	if (firstName.length >= 120) {
		addInvalidFeedback(
			firstNameInputField,
			"Our system only supports names up to 120 characters long"
		);
		return;
	}
	addValidFeedback(firstNameInputField, "Looks good!");
}

function validateLastName() {
	let lastNameInputField = document.getElementById("last-name-input-field");
	let lastName = $(lastNameInputField).val();

	if (lastName.length < 1) {
		addInvalidFeedback(lastNameInputField, "Please enter your last name");
		return;
	}
	addValidFeedback(lastNameInputField, "Looks good!");
}

function validateEmail() {
	let emailInputField = document.getElementById("email-input-field");
	let email = $(emailInputField).val();

	// rfc2822 regex for emails
	const emailRegex =
		/(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/;
	if (!emailRegex.test(email)) {
		addInvalidFeedback(
			emailInputField,
			"We can't recognize that as an email address quite yet, please double check it"
		);
		return;
	}
	addValidFeedback(emailInputField, "Looks good!");
}

function addInvalidFeedback(element, feedbackMessage) {
	// $(element).addClass("is-invalid");
	// $(element).removeClass("is-valid");
	// $(element).removeClass("is-validating");
	// $(element).parent().addClass("is-invalid");
	// $(element).parent().removeClass("is-valid");
	// $(element).parent().removeClass("is-validating");

	// $(`#${element.id}-feedback`).addClass("invalid-feedback");
	// $(`#${element.id}-feedback`).removeClass("valid-feedback");
	// $(`#${element.id}-feedback`).removeClass("validating-feedback");
	// $(`#${element.id}-feedback`).text(feedbackMessage);

	// // Disable the submit button
	// $("#register-form-submit-button").prop("disabled", true);

	element.classList.add("is-invalid");
	element.classList.remove("is-valid");
	element.classList.remove("is-validating");

	element.parentElement.classList.add("is-invalid");
	element.parentElement.classList.remove("is-valid");
	element.parentElement.classList.remove("is-validating");

	document
		.getElementById(`${element.id}-feedback`)
		.classList.add("invalid-feedback");
	document
		.getElementById(`${element.id}-feedback`)
		.classList.remove("valid-feedback");
	document
		.getElementById(`${element.id}-feedback`)
		.classList.remove("validating-feedback");
	document.getElementById(`${element.id}-feedback`).textContent =
		feedbackMessage;

	// Disable the submit button
	document.getElementById("register-form-submit-button").disabled = true;
}

function addValidatingFeedback(element, feedbackMessage) {

	element.classList.add("is-validating");
	element.classList.remove("is-invalid");
	element.classList.remove("is-valid");
	element.parentElement.classList.add("is-validating");
	element.parentElement.classList.remove("is-invalid");
	element.parentElement.classList.remove("is-valid");

	document
		.getElementById(`${element.id}-feedback`)
		.classList.add("validating-feedback");
	document
		.getElementById(`${element.id}-feedback`)
		.classList.remove("invalid-feedback");
	document
		.getElementById(`${element.id}-feedback`)
		.classList.remove("valid-feedback");
	document.getElementById(`${element.id}-feedback`).textContent =
		feedbackMessage;
}

function addValidFeedback(element, feedbackMessage) {
	element.classList.add("is-valid");
	element.classList.remove("is-invalid");
	element.classList.remove("is-validating");
	element.parentElement.classList.add("is-valid");
	element.parentElement.classList.remove("is-invalid");
	element.parentElement.classList.remove("is-validating");

	document
		.getElementById(`${element.id}-feedback`)
		.classList.add("valid-feedback");
	document
		.getElementById(`${element.id}-feedback`)
		.classList.remove("invalid-feedback");
	document
		.getElementById(`${element.id}-feedback`)
		.classList.remove("validating-feedback");
	document.getElementById(`${element.id}-feedback`).textContent =
		feedbackMessage;

	// Enable the submit button
	document.getElementById("register-form-submit-button").disabled = false;
}

const signInBtn = document.querySelector("#sign-in-btn");
const signUpBtn = document.querySelector("#sign-up-btn");
const loginRegisterContainer = document.querySelector(
	".login-register-container"
);

signUpBtn.addEventListener("click", () => {
	loginRegisterContainer.classList.add("sign-up-mode");

	// Maybe replace the url to reflect the change to the register "page"?

	// let url = new URL(window.location.href);
	// let paramaters = url.searchParams;
	// paramaters.delete("register");
	// let title = "Register - Nebula";
	// window.history.pushState(
	// 	"Register",
	// 	title,
	// 	"/register" + paramaters.toString() ? `?${paramaters.toString()}` : ""
	// );
	// document.title = title;
	// console.log("register", paramaters.toString());
});

signInBtn.addEventListener("click", () => {
	loginRegisterContainer.classList.remove("sign-up-mode");

	// Maybe replace the url to reflect the change to the login "page"?

	// let url = new URL(window.location.href);
	// let paramaters = url.searchParams;
	// paramaters.delete("register");
	// let title = "Login - Nebula";
	// window.history.pushState(
	// 	"Login",
	// 	title,
	// 	"/login" + paramaters.toString() ? `?${paramaters.toString()}` : ""
	// );
	// document.title = title;
	// console.log("login", paramaters.toString());
});

// doesn't work quite yet

// window.onpopstate = function (e) {
// 	if (e.state) {
// 		console.log(e);
// 		switch (e.state) {
// 			case "Register":
// 				loginRegisterContainer.classList.add("sign-up-mode");
// 				break;
// 			case "Login":
// 				loginRegisterContainer.classList.remove("sign-up-mode");
// 				break;
// 		}
// 	}
// };

// if (loginRegisterContainer.classList.contains("sign-up-mode")) {
// 	let url = new URL(window.location.href);
// 	let paramaters = url.searchParams;
// 	paramaters.delete("register");
// 	window.history.replaceState(
// 		"Register",
// 		"Register - Nebula test",
// 		"/register" + paramaters.toString() ? `?${paramaters.toString()}` : ""
// 	);
// 	console.log("Register");
// } else {
// 	let url = new URL(window.location.href);
// 	let paramaters = url.searchParams;
// 	paramaters.delete("register");
// 	window.history.replaceState(
// 		"Login",
// 		"Login - Nebula test",
// 		"/login" + paramaters.toString() ? `?${paramaters.toString()}` : ""
// 	);
// 	console.log("Login");
// }

startFormValidation();
