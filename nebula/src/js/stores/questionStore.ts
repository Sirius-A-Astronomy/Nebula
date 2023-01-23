import { storeModuleFactory } from "@stores/factory/storeFactory";
import type { Course } from "@stores/courseStore";
import type { SubjectTag } from "@stores/subjectTagStore";
import type { User } from "@stores/userStore";

export type Answer = {
  id: string;
  content: string;
  title: string;
  sources: string[];
  user: User;
  question_id: string;
};

export type Comment = {
  id: string;
  content: string;
  user: User;
  question_id: string;
  is_suggestion: boolean;
};

export type Question = {
  id: string;
  title: string;
  content: string;
  course: Course;
  subject_tags?: SubjectTag[];
  answers?: Answer[];
  comments?: Comment[];
  user: User;
};

export const questionStore = storeModuleFactory<Question>("questions");
