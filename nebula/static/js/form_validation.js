/*
    Client-side form validation

    Client-side validation was chosen to minimise reloading of the page.
*/

async function isUsernameAvailable(username) {
	let valid_username;
	await $.ajax({
		url: "/api/is_username_available",
		type: "POST",
		data: JSON.stringify({
			username: username,
		}),
		contentType: "application/json",
		dataType: "json",
		success: function (data) {
			valid_username = data.available;
		},
		error: function (data) {
			console.log(data);
		},
	});
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
	$("#username-input-field").on("input", debounce(validateUsername, 500));
	console.log("startFormValidation");
	$("#password-confirmation-input-field").on(
		"input",
		debounce(validatePasswordConfirmation, 500)
	);
	$("#password-input-field").on("input", debounce(validatePassword, 500));
	$("#first-name-input-field").on("input", debounce(validateFirstName, 500));
	$("#last-name-input-field").on("input", debounce(validateLastName, 500));
}

async function validateUsername() {
	let usernameInputField = document.getElementById("username-input-field");
	let username = $(usernameInputField).val();

	if (username.length < 3) {
		addInvalidFeedback(
			usernameInputField,
			"Username must be at least 3 characters long"
		);
		return;
	}

	if (username.length >= 30) {
		addInvalidFeedback(
			usernameInputField,
			"Username must be at most 30 characters long"
		);
		return;
	}

	if (/\s/.test(username)) {
		addInvalidFeedback(
			usernameInputField,
			"Username cannot contain spaces"
		);
		return;
	}

	var regex = /[ @()+=\[\]{};':"\\|,.<>\/?]/g;
	if (regex.test(username)) {
		addInvalidFeedback(
			usernameInputField,
			"Username cannot contain special characters"
		);
		return;
	}

	addValidatingFeedback(
		usernameInputField,
		"Checking if username already exists..."
	);
	let usernameAvailable = await isUsernameAvailable(username);
	if (usernameAvailable) {
		addValidFeedback(usernameInputField, "Looks good!");
	} else {
		addInvalidFeedback(
			usernameInputField,
			"Uh oh, it looks like that username is already taken, please try another one"
		);
	}
}

function validatePassword() {
	let passwordInputField = document.getElementById("password-input-field");
	let password = $(passwordInputField).val();

	if (password.length < 12) {
		addInvalidFeedback(
			passwordInputField,
			"Password must be at least 12 characters long"
		);
		return false;
	}
	addValidFeedback(passwordInputField, "Looks good!");
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
			"Please enter a password first"
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

	if (firstName.length < 2) {
		addInvalidFeedback(
			firstNameInputField,
			"First name must be at least 2 characters long"
		);
		return;
	}
	addValidFeedback(firstNameInputField, "Looks good!");
}

function validateLastName() {
	let lastNameInputField = document.getElementById("last-name-input-field");
	let lastName = $(lastNameInputField).val();

	if (lastName.length < 2) {
		addInvalidFeedback(
			lastNameInputField,
			"Last name must be at least 2 characters long"
		);
		return;
	}
	addValidFeedback(lastNameInputField, "Looks good!");
}

function addInvalidFeedback(element, feedbackMessage) {
	$(element).addClass("is-invalid");
	$(element).removeClass("is-valid");
	$(element).removeClass("is-validating");
	$(`#${element.id}-feedback`).addClass("invalid-feedback");
	$(`#${element.id}-feedback`).removeClass("valid-feedback");
	$(`#${element.id}-feedback`).removeClass("validating-feedback");
	$(`#${element.id}-feedback`).text(feedbackMessage);
	console.log(`#${element.id}-feedback`);

	// Disable the submit button
	$("#register-form-submit-button").prop("disabled", true);
}

function addValidatingFeedback(element, feedbackMessage) {
	$(element).addClass("is-validating");
	$(element).removeClass("is-invalid");
	$(element).removeClass("is-valid");
	$(`#${element.id}-feedback`).addClass("validating-feedback");
	$(`#${element.id}-feedback`).removeClass("invalid-feedback");
	$(`#${element.id}-feedback`).removeClass("valid-feedback");
	$(`#${element.id}-feedback`).text(feedbackMessage);
}

function addValidFeedback(element, feedbackMessage) {
	$(element).addClass("is-valid");
	$(element).removeClass("is-invalid");
	$(element).removeClass("is-validating");
	$(`#${element.id}-feedback`).addClass("valid-feedback");
	$(`#${element.id}-feedback`).removeClass("invalid-feedback");
	$(`#${element.id}-feedback`).removeClass("validating-feedback");
	$(`#${element.id}-feedback`).text(feedbackMessage);

	// Enable the submit button
	$("#register-form-submit-button").prop("disabled", false);
}

startFormValidation();
