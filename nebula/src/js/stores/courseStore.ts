import { storeModuleFactory } from "./factory/storeFactory";

export type Course = {
	id: string;
	name: string;
	code: string;
	description: string;
	semester: string;
	course_level: {
		id: string;
		code: string;
		name: string;
		study_type: string;
	};
};

export const courseStore = storeModuleFactory<Course>("courses");
