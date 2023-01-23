<script setup lang="ts">
import { authenticatedUser, isAuthenticated } from "@stores/sessionStore";

import "@scss/backgrounds/stars.scss";

import OnlineTest from "/images/online-test.svg";
import { RouterLink } from "vue-router";
import { courseLevelStore } from "@/stores/courseLevelStore";

import "@scss/components/_buttons.scss";

const courseLevels = courseLevelStore.getters.all;
</script>

<template>
  <main id="Main">
    <div class="container-background">
      <div class="stars"></div>
      <div class="twinkling"></div>
      <div class="container-index">
        <div class="panel left-panel">
          <section class="container-introduction">
            <div class="content">
              <h2 v-if="!isAuthenticated">Welcome to Nebula!</h2>
              <h2 v-else>
                Welcome back to Nebula,
                {{ authenticatedUser.first_name }}!
              </h2>
              <p>
                This is the Nebula Database by the Kapteyn Learning Community.
              </p>
              <p>It is a repository of user-submitted practice questions.</p>
            </div>

            <div class="image">
              <img :src="OnlineTest" alt="" />
            </div>
          </section>
        </div>
        <div class="panel right-panel">
          <section class="container-index-browse" id="content">
            <h2>Browse the Nebula</h2>
            <p>
              <a
                class="button-accent on-dark"
                href="{{ url_for('web.courses.all_courses')}}"
                >All Courses</a
              >
            </p>
            <h3>Bachelor</h3>
            <RouterLink
              v-for="course_level in courseLevels.filter(
                (cl) => cl.study_type === 'Bachelor'
              )"
              :key="course_level.id"
              :to="{
                name: 'course.level.show',
                params: { id: course_level.id },
              }"
              class="button-accent on-dark"
              >{{ course_level.name }}</RouterLink
            >
            <h3>Master</h3>
            <RouterLink
              v-for="course_level in courseLevels.filter(
                (cl) => cl.study_type === 'Master'
              )"
              :key="course_level.id"
              :to="{
                name: 'course.level.show',
                params: { id: course_level.id },
              }"
              class="button-accent on-dark"
              >{{ course_level.name }}</RouterLink
            >
          </section>
        </div>
      </div>
    </div>
  </main>
</template>

<style lang="scss" scoped>
.container-index {
  grid-template-columns: 1fr 1fr;
  display: grid;
  width: 100%;
  min-height: calc(100vh - 5rem);
  position: relative;

  h2 {
    color: var(--color-text-on-primary);
    font-size: 2rem;
    font-weight: 700;
    font-family: "Poppins", "Open Sans", "Arial", sans-serif;
  }

  .button-accent {
    font-size: 1.2rem;
  }

  h3 {
    color: var(--color-text-on-primary);
    font-size: 1.5rem;
    font-weight: 700;
    font-family: "Poppins", "Open Sans", "Arial", sans-serif;
  }

  p {
    color: var(--color-text-on-primary);
    font-size: 1.125rem;
    font-weight: 400;
    font-family: "Poppins", "Open Sans", "Arial", sans-serif;
  }

  .btn {
    font-size: 1.5rem;
  }
}

.container-introduction {
  margin-bottom: 1rem;
  padding-top: 1rem;
}

.container-introduction h2 {
  color: var(--color-text-on-primary);
  font-size: 3rem;
  line-height: 1.1;
  letter-spacing: 0.04rem;
}

.container-introduction p {
  color: var(--color-text-on-primary);
  font-weight: 400;
  line-height: 1.5;
}

.container-introduction .image img {
  width: 100%;
  max-width: 650px;
  transform: translateY(60%);
}

.container-index-browse {
  /* background-color: var(--color-background-secondary); */
  padding: 0.5rem 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.5rem;
}

.container-add-question {
  margin-top: 1rem;
}

.container-add-question h2 {
  margin-bottom: 0.5rem;
}

.container-add-question .btn-primary {
  margin-top: 1rem;
}

.container-add-question .btn-primary:hover,
.container-add-question .btn-primary:focus {
  opacity: 1;
  background-position: right center;
  border: none;
  box-shadow: none;
}

.tag-container {
  * + * {
    margin-left: 0.5rem;
  }
}

.container-index .panel {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  text-align: center;
}

.container-index .left-panel {
  grid-column: 1 / 2;
  grid-row: 1 / 3;
  padding: 3rem 17% 2rem 12%;
}

.container-index .right-panel {
  grid-column: 2 / 3;
  grid-row: 1 / 3;
  justify-content: center;
  padding: 3rem 12% 3rem 17%;
}

.container-background {
  position: relative;
  top: 0;
  left: 0;
  width: 100%;
  /* min-height: 1050px; */
  min-height: calc(100vh - 5rem);
  /* height: 100%; */
  overflow: hidden;
  /* pointer-events: none; */
}

.container-background:before {
  position: absolute;
  content: "";
  top: -10%;
  right: 48%;
  width: 4000px;
  height: 4000px;
  transform: translateY(-50%);
  border-radius: 50%;
  background-image: linear-gradient(
    -45deg,
    var(--color-primary),
    var(--color-tertiary)
  );
  z-index: -1;
  transition: 1s ease-in-out;
  overflow: hidden;
  box-shadow: var(--box-shadow);
}

.container-question-page.edit-mode .container-question-edit {
  display: block;
}

.container-question-page .container-question {
  display: block;
}

@media (max-width: 768px) {
  .container-index {
    grid-template-columns: 1fr;
  }

  .container-index h2 {
    font-size: 1.9rem;
  }
  .container-introduction h2 {
    font-size: 2.3rem;
  }
  .container-index p {
    font-size: 1rem;
  }
  .container-index .button-accent {
    font-size: 1rem;
  }
  .container-index h3 {
    font-size: 1.2rem;
  }
  .container-index .left-panel {
    padding: 2rem 0.5rem;
    grid-column: 1 / 2;
    grid-row: 1 / 2;
    min-height: 220px;
    margin-top: 30px;
  }
  .container-index .right-panel {
    padding: 2rem 0.5rem;
    grid-column: 1 / 2;
    grid-row: 2 / 3;
    justify-content: start;
  }

  .container-introduction .image img {
    max-width: 40%;
    position: absolute;
    top: 50%;
    right: 0%;
    bottom: initial;
    transform: #{"translateY(min(-42vh, -210px))"};
  }
  .container-introduction .content {
    max-width: 60%;
    position: absolute;
    left: 0;
    top: 50%;
    bottom: initial;
    transform: #{"translateY(min(-42vh, -210px))"};
  }

  .container-background:before {
    left: -20%;
    bottom: initial;
    top: calc(-4000px + max(calc(100px + 20%), 300px));
    transform: translateX(-50%);
    /* top: -100%; */
    right: initial;
  }
}

@media (max-width: 592px) {
  .container-index .image {
    display: none;
  }

  .container-introduction .content {
    width: 100%;
    max-width: 100%;
    position: relative;
    top: initial;
    left: initial;
    transform: initial;
    bottom: initial;
    right: initial;
  }

  .container-background::before {
    left: 0%;
    top: calc(-4000px + max(calc(200px + 18%), 300px));
    transform: translateX(-50%);
  }
}

@keyframes move-background {
  from {
    -webkit-transform: translate3d(0px, 0px, 0px);
  }
  to {
    -webkit-transform: translate3d(1000px, 0px, 0px);
  }
}
@-webkit-keyframes move-background {
  from {
    -webkit-transform: translate3d(0px, 0px, 0px);
  }
  to {
    -webkit-transform: translate3d(1000px, 0px, 0px);
  }
}

@-moz-keyframes move-background {
  from {
    -webkit-transform: translate3d(0px, 0px, 0px);
  }
  to {
    -webkit-transform: translate3d(1000px, 0px, 0px);
  }
}

@-webkit-keyframes move-background {
  from {
    -webkit-transform: translate3d(0px, 0px, 0px);
  }
  to {
    -webkit-transform: translate3d(1000px, 0px, 0px);
  }
}
</style>
