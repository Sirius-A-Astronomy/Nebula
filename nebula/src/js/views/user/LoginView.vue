<script setup lang="ts">
import LoginImage from "/images/login.svg";
import RegisterImage from "/images/register.svg";
import { watch, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import useFlashStore from "@stores/flashStore";
import { login, register } from "@stores/sessionStore";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

import "@scss/backgrounds/stars.scss";
import "@scss/components/forms.scss";

import {
    validatePassword,
    validatePasswordConfirmation,
    validateEmail,
    validateFirstName,
    validateLastName,
} from "@/components/user/userValidation";
import { debounce } from "throttle-debounce";

const props = defineProps<{
    register?: boolean;
    registration?: "success";
}>();

const flash = useFlashStore();

const showRegister = ref(props.register ?? false);

const router = useRouter();
const route = useRoute();

const animating = ref(false);

const setRegister = (val: boolean) => {
    animating.value = true;
    showRegister.value = val;

    setTimeout(() => {
        animating.value = false;
    }, 1600);

    if (val) {
        router.push({
            name: "user.register",
            query: route.query,
        });
        return;
    }
    router.push({
        name: "user.login",
        query: route.query,
    });
};

watch(
    () => props.register,
    (val) => {
        setRegister(val ?? false);
    }
);

const loginValues = ref({
    email: "",
    password: "",
});

const registerValues = ref({
    email: "",
    first_name: "",
    last_name: "",
    password: "",
    passwordConfirmation: "",
});

const registerFeedback = ref({
    email: {
        type: "unvalidated",
        message: "",
    },
    first_name: {
        type: "unvalidated",
        message: "",
    },
    last_name: {
        type: "unvalidated",
        message: "",
    },
    password: {
        type: "unvalidated",
        message: "",
    },
    password_confirmation: {
        type: "unvalidated",
        message: "",
    },
});

const onLoginSubmit = async () => {
    const response = await login(loginValues.value);

    if (!response.ok) {
        flash.add(response.message, "error");
        return;
    }

    const user = response.data.user;
    flash.add(`Welcome back to Nebula, ${user.first_name}!`, "success");

    if (route.query.next) {
        const decoded = decodeURIComponent(route.query.next as string);
        router.push(decoded);
        return;
    }

    router.push({
        name: "home",
    });
};

const onRegisterSubmit = async () => {
    const response = await register(registerValues.value);

    if (response.ok) {
        router.push({
            name: "user.login",
        });
        flash.add(
            "You have been registered, you can now login.",
            "success",
            5000
        );
        return;
    }

    flash.add(response.message, "error");

    const data = response.data as {
        errors?: Record<string, string>;
    };

    if (data.errors) {
        // @ts-ignore
        for (const [key, value] of Object.entries(data.errors)) {
            //@ts-ignore
            if (!registerFeedback.value[key]) continue;
            //@ts-ignore
            registerFeedback.value[key].message = value;
            //@ts-ignore
            registerFeedback.value[key].type = "error";
        }
    }
};

const showPassword = ref({
    login: false,
    register: false,
    registerConfirm: false,
});

const validateFirstNameDebounced = debounce(500, () => {
    registerFeedback.value.first_name.type = "validating";
    const { valid, message } = validateFirstName(
        registerValues.value.first_name
    );

    if (!valid) {
        registerFeedback.value.first_name.type = "error";
    } else {
        registerFeedback.value.first_name.type = "success";
    }
    registerFeedback.value.first_name.message = message;
});

const validateLastNameDebounced = debounce(500, () => {
    registerFeedback.value.last_name.type = "validating";
    const { valid, message } = validateLastName(registerValues.value.last_name);

    if (!valid) {
        registerFeedback.value.last_name.type = "error";
    } else {
        registerFeedback.value.last_name.type = "success";
    }
    registerFeedback.value.last_name.message = message;
});

const validateEmailDebounced = debounce(1000, async () => {
    registerFeedback.value.email.type = "validating";
    const { valid, message } = await validateEmail(registerValues.value.email);

    if (!valid) {
        registerFeedback.value.email.type = "error";
    } else {
        registerFeedback.value.email.type = "success";
    }
    registerFeedback.value.email.message = message;
});

const validatePasswordDebounced = debounce(500, () => {
    registerFeedback.value.password.type = "validating";
    const { valid, message } = validatePassword(
        registerValues.value.password,
        registerValues.value.passwordConfirmation
    );

    if (!valid) {
        registerFeedback.value.password.type = "error";
    } else {
        registerFeedback.value.password.type = "success";
    }
    registerFeedback.value.password.message = message;
});

const validatePasswordConfirmDebounced = debounce(500, () => {
    registerFeedback.value.password_confirmation.type = "validating";
    const { valid, message } = validatePasswordConfirmation(
        registerValues.value.password,
        registerValues.value.passwordConfirmation
    );

    if (!valid) {
        registerFeedback.value.password_confirmation.type = "error";
    } else {
        registerFeedback.value.password_confirmation.type = "success";
    }
    registerFeedback.value.password_confirmation.message = message;
});
</script>

<template>
    <main>
        <div
            class="login-register-container"
            :class="{
                'sign-up-mode': showRegister,
            }"
        >
            <div class="stars-container">
                <div class="stars"></div>
                <div class="twinkling"></div>
            </div>

            <div class="forms-container" id="content">
                <div class="signin-signup">
                    <form class="sign-in-form" @submit.prevent="onLoginSubmit">
                        <div
                            class="m-auto flex w-full max-w-xl flex-col items-center justify-center"
                            :class="{
                                invisible: showRegister && !animating,
                            }"
                        >
                            <h1 class="mb-2 text-4xl font-bold tracking-tight">
                                Login
                            </h1>

                            <p class="mb-2" v-if="registration === 'success'">
                                Registration was successful, you can now login.
                            </p>

                            <div class="input-field">
                                <label for="loginEmail" class="form-label"
                                    >Email</label
                                >
                                <input
                                    class="form-control"
                                    type="text"
                                    name="loginEmail"
                                    autocomplete="email"
                                    autocapitalize="off"
                                    autocorrect="off"
                                    id="loginEmail"
                                    v-model="loginValues.email"
                                />
                            </div>
                            <div class="input-field">
                                <label for="loginPassword" class="form-label"
                                    >Password</label
                                >
                                <input
                                    id="loginPassword"
                                    autocomplete="current-password"
                                    class="form-control"
                                    :class="
                                        showPassword.login ? 'font-mono' : ''
                                    "
                                    :type="
                                        showPassword.login ? 'text' : 'password'
                                    "
                                    name="password"
                                    v-model="loginValues.password"
                                />

                                <button
                                    class="password-show-button"
                                    type="button"
                                    @click="
                                        showPassword.login = !showPassword.login
                                    "
                                >
                                    <FontAwesomeIcon
                                        :icon="
                                            showPassword.login
                                                ? faEye
                                                : faEyeSlash
                                        "
                                    />
                                </button>
                            </div>

                            <button class="btn btn-primary" type="submit">
                                Login
                            </button>
                        </div>
                    </form>

                    <form
                        class="sign-up-form"
                        :class="{
                            invisible: !showRegister && !animating,
                        }"
                    >
                        <div
                            class="m-auto flex w-full max-w-xl flex-col items-center justify-center"
                        >
                            <h1 class="mb-2 text-4xl font-bold tracking-tight">
                                Register
                            </h1>
                            <form @submit.prevent="onRegisterSubmit">
                                <div class="flex flex-col md:flex-row md:gap-2">
                                    <div class="input-field">
                                        <label
                                            for="registerFirstName"
                                            class="form-label"
                                            >First Name</label
                                        >
                                        <input
                                            id="registerFirstName"
                                            autocomplete="given-name"
                                            class="form-control"
                                            type="text"
                                            name="registerFirstName"
                                            v-model="registerValues.first_name"
                                            @input="validateFirstNameDebounced"
                                        />

                                        <div
                                            class="input-feedback"
                                            :class="{
                                                'invalid-feedback':
                                                    registerFeedback.first_name
                                                        .type === 'error',
                                                'valid-feedback':
                                                    registerFeedback.first_name
                                                        .type === 'success',
                                                'validating-feedback':
                                                    registerFeedback.first_name
                                                        .type === 'validating',
                                            }"
                                        >
                                            {{
                                                registerFeedback.first_name
                                                    .message
                                            }}
                                        </div>
                                    </div>

                                    <div class="input-field">
                                        <label
                                            for="registerLastName"
                                            class="form-label"
                                            >Last Name</label
                                        >
                                        <input
                                            id="registerLastName"
                                            autocomplete="family-name"
                                            class="form-control"
                                            type="text"
                                            name="registerLastName"
                                            v-model="registerValues.last_name"
                                            @input="validateLastNameDebounced"
                                        />

                                        <div
                                            class="input-feedback"
                                            :class="{
                                                'invalid-feedback':
                                                    registerFeedback.last_name
                                                        .type === 'error',
                                                'valid-feedback':
                                                    registerFeedback.last_name
                                                        .type === 'success',
                                                'validating-feedback':
                                                    registerFeedback.last_name
                                                        .type === 'validating',
                                            }"
                                        >
                                            {{
                                                registerFeedback.last_name
                                                    .message
                                            }}
                                        </div>
                                    </div>
                                </div>
                                <div class="input-field">
                                    <label
                                        for="registerEmail"
                                        class="form-label"
                                        >Email</label
                                    >
                                    <input
                                        id="registerEmail"
                                        autocomplete="email"
                                        class="form-control"
                                        type="email"
                                        name="registerEmail"
                                        v-model="registerValues.email"
                                        @input="validateEmailDebounced"
                                    />

                                    <div
                                        class="input-feedback"
                                        :class="{
                                            'invalid-feedback':
                                                registerFeedback.email.type ===
                                                'error',
                                            'valid-feedback':
                                                registerFeedback.email.type ===
                                                'success',
                                            'validating-feedback':
                                                registerFeedback.email.type ===
                                                'validating',
                                        }"
                                    >
                                        {{ registerFeedback.email.message }}
                                    </div>
                                </div>

                                <div class="input-field mt-4">
                                    <label
                                        for="registerPassword"
                                        class="form-label"
                                        >Password</label
                                    >
                                    <input
                                        id="registerPassword"
                                        autocomplete="new-password"
                                        class="form-control"
                                        :class="
                                            showPassword.register
                                                ? 'font-mono'
                                                : ''
                                        "
                                        :type="
                                            showPassword.register
                                                ? 'text'
                                                : 'password'
                                        "
                                        name="registerPassword"
                                        v-model="registerValues.password"
                                        @input="validatePasswordDebounced"
                                    />

                                    <button
                                        class="password-show-button"
                                        @click.prevent="
                                            showPassword.register =
                                                !showPassword.register
                                        "
                                    >
                                        <FontAwesomeIcon
                                            :icon="
                                                showPassword.register
                                                    ? faEye
                                                    : faEyeSlash
                                            "
                                        />
                                    </button>

                                    <div
                                        class="input-feedback"
                                        :class="{
                                            'invalid-feedback':
                                                registerFeedback.password
                                                    .type === 'error',
                                            'valid-feedback':
                                                registerFeedback.password
                                                    .type === 'success',
                                            'validating-feedback':
                                                registerFeedback.password
                                                    .type === 'validating',
                                        }"
                                    >
                                        {{ registerFeedback.password.message }}
                                    </div>
                                </div>

                                <div class="input-field">
                                    <label
                                        for="registerPasswordConfirm"
                                        class="form-label"
                                        >Confirm Password</label
                                    >
                                    <input
                                        id="registerPasswordConfirm"
                                        autocomplete="new-password"
                                        class="form-control"
                                        :class="
                                            showPassword.registerConfirm
                                                ? 'font-mono'
                                                : ''
                                        "
                                        :type="
                                            showPassword.registerConfirm
                                                ? 'text'
                                                : 'password'
                                        "
                                        name="registerPasswordConfirm"
                                        v-model="
                                            registerValues.passwordConfirmation
                                        "
                                        @input="
                                            validatePasswordConfirmDebounced
                                        "
                                    />
                                    <button
                                        class="password-show-button"
                                        @click.prevent="
                                            showPassword.registerConfirm =
                                                !showPassword.registerConfirm
                                        "
                                    >
                                        <FontAwesomeIcon
                                            :icon="
                                                showPassword.registerConfirm
                                                    ? faEye
                                                    : faEyeSlash
                                            "
                                        />
                                    </button>

                                    <div
                                        class="input-feedback"
                                        :class="{
                                            'invalid-feedback':
                                                registerFeedback
                                                    .password_confirmation
                                                    .type === 'error',
                                            'valid-feedback':
                                                registerFeedback
                                                    .password_confirmation
                                                    .type === 'success',
                                            'validating-feedback':
                                                registerFeedback
                                                    .password_confirmation
                                                    .type === 'validating',
                                        }"
                                    >
                                        {{
                                            registerFeedback
                                                .password_confirmation.message
                                        }}
                                    </div>
                                </div>

                                <button class="btn btn-primary" type="submit">
                                    Register
                                </button>
                            </form>
                        </div>
                    </form>
                </div>
            </div>

            <div class="panels-container">
                <div
                    class="panel left-panel"
                    :class="{
                        invisible: showRegister && !animating,
                    }"
                >
                    <div class="content">
                        <h3>Not yet a part of Nebula?</h3>
                        <p>Create an account to get started!</p>
                        <button
                            class="btn transparent"
                            id="sign-up-btn"
                            @click="setRegister(true)"
                        >
                            Create an account
                        </button>
                    </div>
                    <img :src="LoginImage" class="image" alt="" />
                </div>
                <div
                    class="panel right-panel"
                    :class="{
                        invisible: !showRegister && !animating,
                    }"
                >
                    <div class="content">
                        <h3>Already have an account?</h3>
                        <button
                            @click="setRegister(false)"
                            class="btn transparent"
                            id="sign-in-btn"
                        >
                            Login
                        </button>
                    </div>
                    <img :src="RegisterImage" class="image" alt="" />
                </div>
            </div>
        </div>
    </main>
</template>

<style lang="scss" scoped>
/*
    Login / Register Page
*/

header {
    margin-bottom: 0;
}

footer {
    margin-top: 0;
}

.login-register-container {
    position: relative;
    width: 100%;
    overflow: hidden;
    height: calc(100vh - 5rem);
}

.forms-container {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    overflow: hidden;
}

.signin-signup {
    position: absolute;
    top: max(50%, 300px);
    transform: translate(-50%, -50%);
    left: 75%;
    width: 50%;
    transition: 0.8s 0.4s ease-in-out;
    display: grid;
    grid-template-columns: 1fr;
    z-index: 5;
    --signin-signup-height: calc(0.7 * (100vh - 5rem));
    height: var(--signin-signup-height);
    overflow: hidden;
}

form {
    display: flex;
    flex-direction: column;
    padding: 0rem 2rem;
    transition: all 0.2s 0.4s;
    overflow: auto;
    grid-column: 1 / 2;
    grid-row: 1 / 2;
    width: 100%;
}

form .form-group {
    width: 100%;
}

.form-group + .form-group {
    margin-top: 1.5rem;
}

form.sign-up-form {
    opacity: 0;
    z-index: 1;
}

form.sign-in-form {
    z-index: 2;
    opacity: 1;
}

.title {
    font-family: "Poppins", "Open Sans", "Arial", sans-serif;
    font-size: 2.2rem;
    color: var(--color-neutral-50);
    margin-bottom: 10px;
}

h3 {
    font-family: "Poppins", "Open Sans", "Arial", sans-serif;
}

.input-field,
.row {
    width: 100%;
}

.row {
    --bs-gutter-x: 0;
}

.col-md-6 {
    padding: 0;
}

.col-md-6 + .col-md-6 {
    padding-left: 1rem;
}

.btn {
    padding: 0.5em 2em;
    background-image: linear-gradient(
        45deg,
        var(--color-accent-700),
        var(--color-primary-900)
    );
    background-size: 300% auto;
    border: none;
    outline: none;
    border-radius: 49px;
    color: var(--color-text-on-primary);
    text-transform: uppercase;
    font-weight: 600;
    margin: 10px 0;
    cursor: pointer;
    transition: 0.4s ease-in-out;
    transition-property: transform background-position;
    letter-spacing: 0.1em;
}

.btn:hover,
.btn:focus {
    background-position: right center;
    color: var(--color-text-on-primary);
    box-shadow: none;
}

.panels-container {
    position: absolute;
    height: 100%;
    width: 100%;
    top: 0;
    left: 0;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
}

.login-register-container:before {
    content: "";
    position: absolute;
    height: 4000px;
    width: 4000px;
    top: -10%;
    right: 48%;
    transform: translateY(-50%);
    background-image: linear-gradient(
        -45deg,
        var(--color-primary) 0%,
        var(--color-secondary) 100%
    );
    transition: 1s ease-in-out;
    border-radius: 50%;
    z-index: 6;
}

.image {
    width: 100%;
    transition: transform 0.8s ease-in-out;
    transition-delay: 0.3s;
}

.panel {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
    text-align: center;
    z-index: 6;
}

.left-panel {
    pointer-events: all;
    padding: 3rem 17% 2rem 12%;
    opacity: 1;
}

.left-panel .image {
    transform: translateY(50px);
}

.right-panel {
    animation: fadeout 2s ease-in-out;
    pointer-events: none;
    padding: 3rem 12% 2rem 17%;
}

.panel .content {
    transition: transform 0.8s ease-in-out;
    transition-delay: 0.4s;
}

.panel h3 {
    font-weight: 500;
    line-height: 1;
    font-size: 1.5rem;
    color: var(--color-text-on-primary);
}

.panel p {
    color: var(--color-text-on-primary);
    font-size: 0.95rem;
    padding: 0.7rem 0;
}

.btn.transparent {
    margin: 0;
    background: none;
    border: 2px solid var(--color-text-on-primary);
    font-weight: 600;
    font-size: 0.8rem;
    color: var(--color-text-on-primary);
}

.btn.transparent:hover,
.btn.transparent:focus {
    box-shadow: none;
    opacity: 0.65;
}

.right-panel .image,
.right-panel .content {
    transform: translateX(1600px);
}

/* ANIMATION */

.login-register-container.sign-up-mode:before {
    transform: translate(100%, -50%);
    right: 52%;
}

.login-register-container.sign-up-mode .left-panel .content {
    transform: translateX(-1600px);
}

.login-register-container.sign-up-mode .left-panel .image {
    transform: translate(-1600px, 50px);
}

.login-register-container.sign-up-mode .signin-signup {
    left: 25%;
}

.login-register-container.sign-up-mode form.sign-up-form {
    opacity: 1;
    z-index: 2;
}

.login-register-container.sign-up-mode form.sign-in-form {
    opacity: 0;
    z-index: 1;
}

.login-register-container.sign-up-mode .right-panel .image,
.login-register-container.sign-up-mode .right-panel .content {
    transform: translateX(0%);
}

.login-register-container.sign-up-mode .left-panel {
    pointer-events: none;
    animation: fadeOut 2s ease-in-out;
}

.login-register-container.sign-up-mode .right-panel {
    pointer-events: all;
    opacity: 1;
}

@media (max-width: 870px) {
    form {
        top: 0%;
        padding-bottom: 1em;
    }

    .signin-signup {
        transform-origin: top;
        width: 100%;
        top: 5%;
        transform: translate(-50%, 0);
        transition: 0.6s 0.2s ease-in-out;
    }

    .signin-signup,
    .login-register-container.sign-up-mode .signin-signup {
        left: 50%;
    }

    .login-register-container.sign-up-mode .signin-signup {
        margin-top: 200px;
        top: 100%;
        transform: translate(-50%, calc(-200px - var(--signin-signup-height)));
    }

    .panels-container {
        grid-template-columns: 1fr;
        grid-template-rows: 1fr 2fr 1fr;
    }

    .panel {
        flex-direction: row;
        justify-content: space-around;
        align-items: center;
        padding: 2.5rem 8%;
        grid-column: 1 / 2;
        overflow: hidden;
    }

    .right-panel {
        grid-row: 1 / 2;
    }

    .left-panel {
        grid-row: 3 / 4;
    }

    .image {
        width: 200px;
        transition: transform 0.8s ease-in-out;
        transition-delay: 0.3s;
    }

    .panel .content {
        padding-right: 15%;
        transition: transform 0.8s ease-in-out;
        transition-delay: 0.4s;
    }

    .panel h3 {
        font-size: 1.2rem;
    }

    .panel p {
        font-size: 0.7rem;
        padding: 0.5rem 0;
    }

    .btn.transparent {
        font-size: 0.7rem;
    }

    .login-register-container:before {
        position: absolute;
        width: 1500px;
        height: 1500px;
        transform: translate(-50%, 102%);
        left: 30%;
        bottom: 32%;
        right: initial;
        top: initial;
        overflow: hidden;
    }

    .login-register-container.sign-up-mode:before {
        bottom: 72%;
        transform: translateX(-50%);
        right: initial;
        overflow: hidden;
    }

    .login-register-container.sign-up-mode .left-panel .image,
    .login-register-container.sign-up-mode .left-panel .content {
        transform: translateY(1000px);
    }

    .right-panel .image,
    .right-panel .content {
        transform: translateY(-1000px);
    }

    .login-register-container.sign-up-mode .right-panel .image,
    .login-register-container.sign-up-mode .right-panel .content {
        transform: translateY(0px);
    }
}

@media (max-width: 767px) {
    .col-md-6 + .col-md-6 {
        padding-left: 0;
    }
}

@media (max-width: 570px) {
    form {
        padding: 0 0.5rem;
    }

    .image {
        display: none;
    }
    .panel .content {
        padding: 0.5rem 1rem;
    }
    .login-register-container {
        padding: 1.5rem;
    }

    .login-register-container:before {
        bottom: 28%;
        left: 50%;
    }

    .login-register-container.sign-up-mode:before {
        bottom: 72%;
        left: 50%;
    }
}

@keyframes fadeOut {
    0% {
        opacity: 1;
    }

    99% {
        opacity: 1;
    }

    100% {
        opacity: 0;
    }
}

@keyframes fadeIn {
    0% {
        opacity: 0;
    }

    1% {
        opacity: 1;
    }

    100% {
        opacity: 1;
    }
}
</style>
