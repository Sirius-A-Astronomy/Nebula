<script setup lang="ts">
import LoginImage from "/images/login.svg";
import RegisterImage from "/images/register.svg";
import { watch, ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/http/api";
import useFlashStore from "@stores/flashStore";
import { login } from "@stores/sessionStore";

import "@scss/backgrounds/stars.scss";
import "@scss/components/forms.scss";

const props = defineProps<{
  register?: boolean;
}>();

const flash = useFlashStore();

const showRegister = ref(props.register ?? false);

const router = useRouter();

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
    });
    return;
  }
  router.push({
    name: "user.login",
  });
};

watch(
  () => props.register,
  (val) => {
    setRegister(val ?? false);
  }
);

const loginValues = ref({
  username: "",
  password: "",
});

const loginErrors = ref({
  username: "",
  password: "",
});

const registerValues = ref({
  username: "",
  password: "",
  passwordConfirm: "",
});

const onLoginSubmit = async () => {
  const response = await login(loginValues.value);
  if (response.ok) {
    router.push({
      name: "home",
    });
    flash.add("You have been logged in.", "success");
  }
};
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
              <h1 class="mb-2 text-4xl font-bold tracking-tight">Login</h1>
              <div class="input-field">
                <label for="loginUsername" class="form-label">Username</label>
                <input
                  class="form-control"
                  type="text"
                  name="username"
                  autocomplete="username"
                  autocapitalize="off"
                  autocorrect="off"
                  id="loginUsername"
                  v-model="loginValues.username"
                />
              </div>
              <div class="input-field">
                <label for="loginPassword" class="form-label">Password</label>
                <input
                  id="loginPassword"
                  autocomplete="current-password"
                  class="form-control"
                  type="password"
                  name="password"
                  v-model="loginValues.password"
                />
              </div>

              <button class="btn btn-primary" type="submit">Login</button>
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
              <div v-for="i in 50" class="my-2 box-border h-4 w-4 bg-pink-500">
                {{ i }} aaaaaaaaaa
              </div>
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
  --signin-signup-height: calc(0.6 * (100vh - 5rem));
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

.social-text {
  padding: 0.7rem 0;
  font-size: 1rem;
}

.social-media {
  display: flex;
  justify-content: center;
}

.social-icon {
  height: 46px;
  width: 46px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 0.45rem;
  color: #333;
  border-radius: 50%;
  border: 1px solid #333;
  text-decoration: none;
  font-size: 1.1rem;
  transition: 0.3s;
}

.social-icon:hover {
  color: #4481eb;
  border-color: #4481eb;
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
