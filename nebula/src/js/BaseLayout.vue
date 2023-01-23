<script setup lang="ts">
export type MenuItem = {
  name: string;
  to?: RouteLocationRaw;
  items?: MenuItem[];
  active?: boolean;
  action?: () => void;
};

import { RouterView, useRouter, type RouteLocationRaw } from "vue-router";
import Header from "@components/baseLayout/Header.vue";
import mobileNavMenu from "@components/baseLayout/mobileNavMenu.vue";

import { onMounted, computed } from "vue";

import { courseStore } from "@stores/courseStore";
import { courseLevelStore } from "@stores/courseLevelStore";
import type { Ref } from "vue";
import { authenticatedUser, isAuthenticated } from "./stores/sessionStore";
import { logout } from "@stores/sessionStore";
import useFlashStore from "@stores/flashStore";
import { getAccessLevelValue } from "./stores/userStore";

const flash = useFlashStore();
const router = useRouter();

const navItems: Ref<MenuItem[]> = computed(() => {
  const items: MenuItem[] = [];

  items.push(makeCourseNavItems.value);
  items.push(makeUserNavItems.value);

  return items;
});

const makeUserNavItems = computed(() => {
  const items: MenuItem[] = [];

  if (isAuthenticated.value) {
    items.push({
      name: "Profile",
      to: { name: "user.profile" },
    });

    if (
      authenticatedUser.value.access_level >= getAccessLevelValue("moderator")
    ) {
      items.push({
        name: "Dashboard",
        to: { name: "dashboard" },
      });
    }

    items.push({
      name: "Logout",
      action: () => {
        try {
          logout();
          flash.add("You have been logged out.", "success");
          router.push({ name: "home" });
        } catch (error) {
          flash.add("There was an error logging out.", "error");
        }
      },
    });

    const name =
      authenticatedUser.value.first_name && authenticatedUser.value.last_name
        ? `${authenticatedUser.value.first_name} ${authenticatedUser.value.last_name}`
        : authenticatedUser.value.username;

    return {
      name,
      items,
    };
  }

  if (!isAuthenticated.value) {
    items.push({
      name: "Login",
      to: { name: "user.login" },
    });
    items.push({
      name: "Register",
      to: { name: "user.register" },
    });
  }

  return {
    name: "Account",
    items,
  };
});

const makeCourseNavItems = computed(() => {
  const courses = courseStore.getters.all.value;
  const levelTypes = [
    ...new Set(courses.map((c) => c.course_level.study_type)),
  ];

  const courseItems = [];
  courseItems.push({
    name: "All Courses",
    to: { name: "course.index" },
  });

  levelTypes.forEach((levelType) => {
    const courseLevels = courseLevelStore.getters.all.value.filter(
      (cl) => cl.study_type === levelType
    );

    courseItems.push({
      name: levelType,
    });

    courseLevels.forEach((courseLevel) => {
      courseItems.push({
        name: courseLevel.name,
        items: courses
          .filter((course) => course.course_level.id === courseLevel.id)
          .map((course) => {
            return {
              name: course.name,
              to: {
                name: "course.show",
                params: { id: course.id },
              },
            };
          }),
      });
    });
  });

  return {
    name: "Courses",
    items: courseItems,
  };
});

onMounted(async () => {
  const promises = [];
  if (courseLevelStore.state.shouldLoadAll()) {
    promises.push(courseLevelStore.actions.getAll());
  }

  if (courseStore.state.shouldLoadAll()) {
    promises.push(courseStore.actions.getAll());
  }
  Promise.all(promises);
});
</script>

<template>
  <!-- Mobile SideMenu -->
  <!-- Backdrop -->
  <div class="relative overflow-hidden">
    <Header
      class="fixed inset-x-0 top-0 z-10 flex h-20 flex-row justify-center"
      :menu-items="navItems"
    />
    <mobileNavMenu :menu-items="navItems" />
    <div class="fixed inset-0 top-20 overflow-auto">
      <RouterView />
    </div>
  </div>
</template>

<style lang="scss" scoped></style>
