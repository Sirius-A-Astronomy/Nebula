import { storeModuleFactory } from "@stores/factory/storeFactory";

export type SubjectTag = {
    id: string;
    name: string;
};

export const subjectTagStore = storeModuleFactory<SubjectTag>("subject_tags");

export default subjectTagStore;
