import { storeModuleFactory, type New } from "@stores/factory/storeFactory";

export type User = {
    id: string;
    first_name: string;
    last_name: string;
    email: string;
    access_level: number;
    created_at: string;
};

export type NewUser = New<User> & {
    password_confirmation?: string;
    password?: string;
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

export const getAccessLevelName = (accessLevel: number): string => {
    const accessLevelObj = accessLevels.find(
        (accessLevelObj) => accessLevelObj.value === accessLevel
    );
    if (accessLevelObj) {
        return accessLevelObj.name;
    }
    return "Unknown";
};

export const getAccessLevelValue = (accessLevelName: string): number => {
    const accessLevelObj = accessLevels.find(
        (accessLevelObj) =>
            accessLevelObj.name.toLowerCase() === accessLevelName.toLowerCase()
    );
    if (accessLevelObj) {
        return accessLevelObj.value;
    }
    return 0;
};

export const userStore = storeModuleFactory<User>("users");
