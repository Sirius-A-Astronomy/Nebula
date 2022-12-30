import { storeModuleFactory } from "./factory/storeFactory";

export type CourseLevel = {
	id: string;
	code: string;
	name: string;
	study_type: string;
};

export const courseLevelStore =
	storeModuleFactory<CourseLevel>("course_levels");
