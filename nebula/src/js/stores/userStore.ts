import { storeModuleFactory } from "@stores/factory/storeFactory";

export type User = {
	id: string;
	first_name: string;
	last_name: string;
	username: string;
	email: string;
	access_level: number;
	created_at: string;
};

export type AccessLevel = {
	value: number;
	name: string;
};

export const accessLevels: AccessLevel[] = [
	{
		value: 0,
		name: "Guest",
	},
	{
		value: 1,
		name: "Student",
	},
	{
		value: 2,
		name: "Moderator",
	},
	{
		value: 3,
		name: "Admin",
	},
	{
		value: 4,
		name: "Maintainer",
	},
];

export const userStore = storeModuleFactory<User>("users");
