import { storeModuleFactory } from "./factory/storeFactory";
import type { Course } from "@stores/courseStore";

export type CourseLevel = {
  id: string;
  code: string;
  name: string;
  study_type: StudyType;
};

export type CourseLevelWithCourses = CourseLevel & {
  courses?: Course[];
};

export type StudyType = "Bachelor" | "Master";

export const studyTypes: StudyType[] = ["Bachelor", "Master"];

export const courseLevelStore =
  storeModuleFactory<CourseLevel>("course_levels");
