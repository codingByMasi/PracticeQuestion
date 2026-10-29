import { z } from "zod";

/** Lowercase kebab-case identifier used for slugs and ids. */
export const IdSchema = z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/, "must be lowercase kebab-case");

export const TrackSchema = z.strictObject({
  id: IdSchema,
  title: z.string().min(1),
  description: z.string().min(1),
  runnerId: z.string().min(1),
  editorLanguage: z.string().min(1),
  order: z.number().int(),
});
export type Track = z.infer<typeof TrackSchema>;

export const DatasetMetaSchema = z.strictObject({
  id: IdSchema,
  title: z.string().min(1),
  description: z.string().min(1),
});
export type DatasetMeta = z.infer<typeof DatasetMetaSchema>;
export type Dataset = DatasetMeta & { sql: string };

export const DifficultySchema = z.enum(["Easy", "Medium", "Hard"]);
export type Difficulty = z.infer<typeof DifficultySchema>;
export const DIFFICULTIES: readonly Difficulty[] = DifficultySchema.options;

const problemBase = {
  slug: IdSchema,
  track: IdSchema,
  title: z.string().min(1),
  difficulty: DifficultySchema,
  tags: z.array(z.string().min(1)).min(1),
  statementMd: z.string().min(1),
  hints: z.array(z.string().min(1)),
  solutionMd: z.string().min(1),
  starterCode: z.string(),
  /** Optional global position (beginner -> advanced) used to sort the problem list. */
  order: z.number().int().optional(),
};

export const SqlProblemSchema = z.strictObject({
  ...problemBase,
  datasetId: IdSchema,
  setupSql: z.string().optional(),
  expected: z.strictObject({ query: z.string().min(1), orderMatters: z.boolean() }),
});
export type SqlProblem = z.infer<typeof SqlProblemSchema>;

export const PythonTestSchema = z.strictObject({
  args: z.array(z.unknown()),
  expected: z.unknown(),
  hidden: z.boolean(),
});
export type PythonTest = z.infer<typeof PythonTestSchema>;

export const PythonProblemSchema = z
  .strictObject({
    ...problemBase,
    functionName: z.string().regex(/^[A-Za-z_][A-Za-z0-9_]*$/, "must be a valid Python identifier"),
    referenceSolution: z.string().min(1),
    tests: z.array(PythonTestSchema).min(1),
  })
  .refine((p) => p.tests.some((t) => !t.hidden), { message: "needs at least one visible test", path: ["tests"] })
  .refine((p) => p.tests.some((t) => t.hidden), { message: "needs at least one hidden test", path: ["tests"] });
export type PythonProblem = z.infer<typeof PythonProblemSchema>;

/**
 * Problem schema per runner. A new track that reuses an existing runner needs no
 * code; a new runner registers its problem shape here (and a judge in lib/judge).
 */
export const problemSchemaByRunner = {
  sql: SqlProblemSchema,
  python: PythonProblemSchema,
} as const;
export type RunnerWithProblems = keyof typeof problemSchemaByRunner;

export type Problem =
  | ({ kind: "sql" } & SqlProblem)
  | ({ kind: "python" } & PythonProblem);

export type ProblemSummary = Pick<Problem, "slug" | "track" | "title" | "difficulty" | "tags" | "order">;

export const LessonFrontmatterSchema = z.strictObject({
  id: IdSchema,
  title: z.string().min(1),
  order: z.number().int(),
  exerciseSlugs: z.array(IdSchema).min(2).max(5),
  /** SQL lessons: dataset used by runnable snippets. */
  datasetId: IdSchema.optional(),
});
export type LessonFrontmatter = z.infer<typeof LessonFrontmatterSchema>;
export type Lesson = LessonFrontmatter & { track: string; bodyMd: string };

/** Key used by ProgressStore for lesson completion (lesson ids are unique per track). */
export function lessonKey(track: string, id: string): string {
  return `${track}/${id}`;
}
