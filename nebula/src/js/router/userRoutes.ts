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
    {
        path: "/profile/edit",
        name: "user.profile.edit",
        component: () => import("@/views/user/ProfileEdit.vue"),
    },
];

export default userRoutes;
