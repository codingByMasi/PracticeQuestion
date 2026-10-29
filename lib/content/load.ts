import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import type { z } from "zod";
import {
  DatasetMetaSchema,
  LessonFrontmatterSchema,
  TrackSchema,
  problemSchemaByRunner,
  type Dataset,
  type Lesson,
  type Problem,
  type ProblemSummary,
  type Track,
} from "./schema";

export class ContentError extends Error {
  constructor(public readonly issues: string[]) {
    super(`Invalid content:\n  - ${issues.join("\n  - ")}`);
  }
}

export type Content = {
  tracks: Track[];
  datasets: Dataset[];
  problems: Problem[];
  lessons: Lesson[];
};

export const DEFAULT_CONTENT_ROOT = path.join(process.cwd(), "content");

function listFiles(dir: string, ext: string): string[] {
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(ext))
    .sort()
    .map((f) => path.join(dir, f));
}

function listDirs(dir: string): string[] {
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .sort();
}

function formatZod(file: string, error: z.ZodError): string[] {
  return error.issues.map((i) => `${file}: ${i.path.join(".") || "(root)"}: ${i.message}`);
}

function readJson(file: string, issues: string[]): unknown {
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch (e) {
    issues.push(`${file}: invalid JSON (${(e as Error).message})`);
    return undefined;
  }
}

/**
 * Loads and validates every track, dataset, problem and lesson under `root`.
 * Throws ContentError listing every problem found (schema and cross-reference).
 */
export function loadContent(root: string = DEFAULT_CONTENT_ROOT): Content {
  const issues: string[] = [];
  const rel = (f: string) => path.relative(root, f);

  const tracks: Track[] = [];
  for (const file of listFiles(path.join(root, "tracks"), ".json")) {
    const parsed = TrackSchema.safeParse(readJson(file, issues));
    if (!parsed.success) {
      issues.push(...formatZod(rel(file), parsed.error));
      continue;
    }
    if (parsed.data.id !== path.basename(file, ".json")) issues.push(`${rel(file)}: id must match file name`);
    tracks.push(parsed.data);
  }
  tracks.sort((a, b) => a.order - b.order);
  const trackById = new Map(tracks.map((t) => [t.id, t]));

  const datasets: Dataset[] = [];
  for (const file of listFiles(path.join(root, "datasets"), ".json")) {
    const parsed = DatasetMetaSchema.safeParse(readJson(file, issues));
    if (!parsed.success) {
      issues.push(...formatZod(rel(file), parsed.error));
      continue;
    }
    const sqlFile = file.replace(/\.json$/, ".sql");
    if (parsed.data.id !== path.basename(file, ".json")) issues.push(`${rel(file)}: id must match file name`);
    if (!fs.existsSync(sqlFile)) {
      issues.push(`${rel(file)}: missing ${path.basename(sqlFile)}`);
      continue;
    }
    datasets.push({ ...parsed.data, sql: fs.readFileSync(sqlFile, "utf8") });
  }
  const datasetIds = new Set(datasets.map((d) => d.id));

  const problems: Problem[] = [];
  for (const trackDir of listDirs(path.join(root, "problems"))) {
    const track = trackById.get(trackDir);
    if (!track) {
      issues.push(`problems/${trackDir}: no track with id "${trackDir}"`);
      continue;
    }
    const schema = (problemSchemaByRunner as Record<string, (typeof problemSchemaByRunner)[keyof typeof problemSchemaByRunner]>)[
      track.runnerId
    ];
    if (!schema) {
      issues.push(`problems/${trackDir}: runner "${track.runnerId}" has no problem schema`);
      continue;
    }
    for (const file of listFiles(path.join(root, "problems", trackDir), ".json")) {
      const parsed = schema.safeParse(readJson(file, issues));
      if (!parsed.success) {
        issues.push(...formatZod(rel(file), parsed.error));
        continue;
      }
      const p = parsed.data;
      if (p.slug !== path.basename(file, ".json")) issues.push(`${rel(file)}: slug must match file name`);
      if (p.track !== trackDir) issues.push(`${rel(file)}: track must be "${trackDir}"`);
      if ("datasetId" in p && !datasetIds.has(p.datasetId)) issues.push(`${rel(file)}: unknown dataset "${p.datasetId}"`);
      problems.push({ kind: track.runnerId, ...p } as Problem);
    }
  }
  const seen = new Set<string>();
  for (const p of problems) {
    if (seen.has(p.slug)) issues.push(`duplicate problem slug "${p.slug}"`);
    seen.add(p.slug);
  }
  const problemBySlug = new Map(problems.map((p) => [p.slug, p]));

  const lessons: Lesson[] = [];
  for (const trackDir of listDirs(path.join(root, "lessons"))) {
    if (!trackById.has(trackDir)) {
      issues.push(`lessons/${trackDir}: no track with id "${trackDir}"`);
      continue;
    }
    const ids = new Set<string>();
    for (const file of listFiles(path.join(root, "lessons", trackDir), ".md")) {
      const { data, content } = matter(fs.readFileSync(file, "utf8"));
      const parsed = LessonFrontmatterSchema.safeParse(data);
      if (!parsed.success) {
        issues.push(...formatZod(rel(file), parsed.error));
        continue;
      }
      const l = parsed.data;
      if (ids.has(l.id)) issues.push(`${rel(file)}: duplicate lesson id "${l.id}"`);
      ids.add(l.id);
      if (l.datasetId && !datasetIds.has(l.datasetId)) issues.push(`${rel(file)}: unknown dataset "${l.datasetId}"`);
      for (const slug of l.exerciseSlugs) {
        const p = problemBySlug.get(slug);
        if (!p) issues.push(`${rel(file)}: unknown exercise "${slug}"`);
        else if (p.track !== trackDir) issues.push(`${rel(file)}: exercise "${slug}" belongs to track "${p.track}"`);
      }
      lessons.push({ ...l, track: trackDir, bodyMd: content.trim() });
    }
  }
  lessons.sort((a, b) => a.track.localeCompare(b.track) || a.order - b.order);

  if (issues.length > 0) throw new ContentError(issues);
  return { tracks, datasets, problems, lessons };
}

export function toSummary(p: Problem): ProblemSummary {
  return { slug: p.slug, track: p.track, title: p.title, difficulty: p.difficulty, tags: p.tags, order: p.order };
}
