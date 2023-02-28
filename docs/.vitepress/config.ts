import { defineConfig } from "vitepress";

const config = defineConfig({
    title: "Nebula",
    description: "Nebula Documentation",

    lastUpdated: true,
    cleanUrls: true,
    markdown: {
        typographer: true,
    },

    head: [["link", { rel: "icon", href: "/assets/mark.svg" }]],
    lang: "en-US",

    themeConfig: {
        logo: {
            src: "/assets/mark.svg",
            alt: "Nebula Logo",
        },

        editLink: {
            pattern:
                "https://github.com/Sirius-A-Astronomy/Nebula/edit/master/docs/:path",
        },

        siteTitle: "Nebula Documentation",

        outline: [2, 3],

        socialLinks: [
            {
                icon: "github",
                link: "https://gitlab.astro.rug.nl/sirius-a/nebula",
            },
        ],

        nav: [
            {
                text: "User",
                link: "/user/getting-started",
                activeMatch: "/user/",
            },
            {
                text: "Moderator",
                link: "/moderator/getting-started",
                activeMatch: "/moderator/",
            },
            {
                text: "Developer",
                link: "/developer/getting-started",
                activeMatch: "/developer/",
            },
        ],

        sidebar: {
            "/": [
                {
                    text: "Home",
                    items: [{ text: "Introduction", link: "/" }],
                },
            ],

            "/user/": useUserGuideSidebar(),
            "/moderator/": useModeratorGuideSidebar(),
            "/developer/": useDeveloperGuideSidebar(),
        },
    },
});

function useUserGuideSidebar() {
    return [
        {
            text: "Introduction",
            items: [
                {
                    text: "Getting Started",
                    link: "/user/getting-started",
                },
            ],
        },
        {
            text: "Writing",
            items: [
                {
                    text: "Markdown and LaTeX",
                    link: "/user/writing/markdown",
                },
            ],
        },
    ];
}

function useModeratorGuideSidebar() {
    return [
        {
            text: "Introduction",
            items: [
                {
                    text: "Getting started",
                    link: "/moderator/getting-started",
                },
            ],
        },
        {
            text: "Dashboard",
            items: [
                {
                    text: "Course Management",
                    link: "/moderator/dashboard/course-management",
                },
                {
                    text: "Question Management",
                    link: "/moderator/dashboard/question-management",
                },
                {
                    text: "User Management",
                    link: "/moderator/dashboard/user-management",
                },
            ],
        },
    ];
}

function useDeveloperGuideSidebar() {
    return [
        {
            text: "Introduction",
            items: [
                {
                    text: "Getting started",
                    link: "/developer/getting-started",
                },
            ],
        },

        {
            text: "Architecture",
            collapsible: true,
            items: [
                {
                    text: "Project Structure",
                    link: "/developer/architecture/project-structure/",
                },
            ],
        },
        {
            text: "Frontend",
            collapsible: true,

            items: [
                {
                    text: "Importing Assets",
                    link: "/developer/frontend/importing-assets",
                },
                {
                    text: "Vue",
                    link: "/developer/frontend/vue",
                },
            ],
        },
        {
            text: "Backend",
            collapsible: true,
            items: [
                {
                    text: "Routes",
                    link: "/developer/backend/routes",
                },
                {
                    text: "Models",
                    link: "/developer/backend/models",
                },
            ],
        },
        {
            text: "Command Line Interfaces",
            collapsible: true,
            collapsed: true,
            items: [
                {
                    text: "User CLI",
                    link: "/developer/cli/user-cli",
                },
                {
                    text: "Database CLI",
                    link: "/developer/cli/database-cli",
                },
            ],
        },
        {
            text: "Testing",
            collapsible: true,
            collapsed: true,
            items: [
                {
                    text: "Unit Testing",
                    link: "/developer/testing/unit-testing",
                },
                {
                    text: "Integration Testing",
                    link: "/developer/testing/integration-testing",
                },
            ],
        },
        {
            text: "Documentation",
            collapsible: true,
            collapsed: true,
            items: [
                {
                    text: "Writing Documentation",
                    link: "/developer/documentation/writing-documentation",
                },
            ],
        },
        {
            text: "Deployment",
            collapsible: true,
            collapsed: true,
            items: [
                {
                    text: "Building",
                    link: "/developer/deployment/building",
                },
            ],
        },
        {
            text: "Other",
            items: [
                {
                    text: "Contributing",
                    link: "/developer/contributing",
                },
            ],
        },
    ];
}

export default config;
