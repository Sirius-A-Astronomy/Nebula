<script setup lang="ts">
export type MenuItem = {
    name: string;
    to?: RouteLocationRaw;
    items?: MenuItem[];
    active?: boolean;
    action?: () => void;
};

import { RouterView, useRouter, type RouteLocationRaw } from "vue-router";
import Header from "@/components/baseLayout/BaseHeader.vue";
import mobileNavMenu from "@components/baseLayout/mobileNavMenu.vue";

import { onMounted, computed } from "vue";

import { courseStore } from "@stores/courseStore";
import { courseLevelStore } from "@stores/courseLevelStore";
import type { ComputedRef } from "vue";
import { authenticatedUser, isAuthenticated } from "./stores/sessionStore";
import { logout } from "@stores/sessionStore";
import useFlashStore from "@stores/flashStore";
import { getAccessLevelValue } from "./stores/userStore";
import { canCreateQuestion } from "./lib/permissionHelpers";

const flash = useFlashStore();
const router = useRouter();

const primaryNavItems: ComputedRef<MenuItem[]> = computed(() => {
    const items: MenuItem[] = [];

    items.push({
        name: "Home",
        to: { name: "home" },
    });

    items.push(courseNavItem.value);

    if (canCreateQuestion()) {
        items.push({
            name: "Add a Question",
            to: { name: "question.create" },
        });
    }
    return items;
});

const secondaryNavItems: ComputedRef<MenuItem[]> = computed(() => {
    const items: MenuItem[] = [];

    items.push(userNavItem.value);

    return items;
});

const userNavItem = computed(() => {
    const items: MenuItem[] = [];

    if (isAuthenticated.value) {
        items.push({
            name: "Profile",
            to: { name: "user.profile" },
        });

        if (
            authenticatedUser.value.access_level >=
            getAccessLevelValue("moderator")
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

        const name = `${authenticatedUser.value.first_name} ${authenticatedUser.value.last_name}`;

        return {
            name,
            items,
        };
    }

    if (!isAuthenticated.value) {
        items.push({
            name: "Login",
            to: {
                name: "user.login",
                query: {
                    next: encodeURIComponent(
                        router.currentRoute.value.fullPath
                    ),
                },
            },
        });
        items.push({
            name: "Register",
            to: {
                name: "user.register",
                query: {
                    next: encodeURIComponent(
                        router.currentRoute.value.fullPath
                    ),
                },
            },
        });
    }

    return {
        name: "Account",
        items,
    };
});

const courseNavItem = computed(() => {
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
                to: {
                    name: "course.level.show",
                    params: { id: courseLevel.id },
                },
                items: courses
                    .filter(
                        (course) => course.course_level.id === courseLevel.id
                    )
                    .sort((a, b) => a.semester.localeCompare(b.semester))
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
            :primary-nav-items="primaryNavItems"
            :secondary-nav-items="secondaryNavItems"
        />
        <mobileNavMenu
            :primary-nav-items="primaryNavItems"
            :secondary-nav-items="secondaryNavItems"
        />
        <div
            class="fixed inset-0 top-20 w-screen overflow-y-auto overflow-x-hidden"
        >
            <div class="w-screen">
                <RouterView />
            </div>
        </div>
    </div>
</template>
