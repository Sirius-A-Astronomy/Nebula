import type { RouteRecordRaw } from "vue-router";

export const baseRoutes: RouteRecordRaw[] = [
    {
        path: "/",
        name: "home",
        component: () => import("@/views/main/IndexView.vue"),
        meta: {
            title: "Nebula | Home",
            description: "Home page of nebula",
        },
    },
];

export default baseRoutes;
