import profile from "./qualification.json";
export const QUALIFICATION = profile;
export const EXAM_RULES = profile.exam;
export const SUBJECTS = [profile.subject] as const;
