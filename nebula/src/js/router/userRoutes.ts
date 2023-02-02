export const userRoutes = [
    {
        path: "/login",
        name: "user.login",
        component: () => import("@/views/user/LoginView.vue"),
        props: { register: false },
    },
    {
        path: "/register",
        name: "user.register",
        component: () => import("@/views/user/LoginView.vue"),
        props: { register: true },
    },
    {
        path: "/profile",
        name: "user.profile",
        component: () => import("@/views/user/ProfileView.vue"),
    },
];

export default userRoutes;
