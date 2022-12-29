import { defineConfig } from "vitepress";

const config = defineConfig({
	title: "Nebula",
	description: "Nebula Documentation",

	base: "/docs/",

	lastUpdated: true,
	cleanUrls: "without-subfolders",

	themeConfig: {
		logo: "/assets/logo.png",
		siteTitle: "Nebula Documentation",

		nav: [
			{ text: "Home", link: "/" },
			{
				text: "User Guide",
				link: "/user/",
				activeMatch: "/user/",
			},
			{
				text: "Moderator Guide",
				link: "/moderator/",
				activeMatch: "/moderator/",
			},
			{
				text: "Developer Guide",
				link: "/developer/",
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
			text: "User Guide",
			items: [
				{ text: "Introduction", link: "/user/" },
				{
					text: "Getting Started",
					link: "/user/getting-started",
				},
				{
					text: "Creating Questions",
					link: "/user/creating-questions/",
					items: [
						{
							text: "Markdown",
							link: "/user/creating-questions/markdown",
						},
						{
							text: "LaTeX",
							link: "/user/creating-questions/latex",
						},
						{
							text: "Code",
							link: "/user/creating-questions/code",
						},
					],
				},
			],
		},
	];
}

function useModeratorGuideSidebar() {
	return [
		{
			text: "Moderator Guide",
			items: [
				{ text: "Introduction", link: "/moderator/" },
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
			],
		},
	];
}

function useDeveloperGuideSidebar() {
	return [
		{
			text: "Developer Guide",
			items: [
				{ text: "Introduction", link: "/developer/" },
				{
					text: "Getting Started",
					link: "/developer/getting-started",
				},

				{
					text: "Architecture",
					link: "/developer/architecture/",
					items: [
						{
							text: "Frontend",
							link: "/developer/architecture/frontend",
						},
						{
							text: "Routes",
							link: "/developer/architecture/routes",
						},
					],
				},
				{ text: "API", link: "/developer/api" },
				{
					text: "Command Line Interfaces",
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
				{ text: "Frontend", link: "/developer/frontend" },
				{ text: "Backend", link: "/developer/backend" },
				{ text: "Testing", link: "/developer/testing" },
			],
		},
	];
}

export default config;
