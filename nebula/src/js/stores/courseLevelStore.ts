import { storeModuleFactory } from "./factory/storeFactory";
import type { Course } from "@stores/courseStore";

export type CourseLevel = {
	id: string;
	code: string;
	name: string;
	study_type: string;
};

export type CourseLevelWithCourses = CourseLevel & {
	courses?: Course[];
};

export const courseLevelStore =
	storeModuleFactory<CourseLevel>("course_levels");
