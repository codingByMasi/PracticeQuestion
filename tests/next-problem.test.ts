import { describe, expect, it } from "vitest";
import { getNextTarget } from "@/lib/content/next-problem";
import type { Lesson, ProblemSummary } from "@/lib/content/schema";

const p = (slug: string, track = "sql", order?: number): ProblemSummary => ({
  slug,
  track,
  title: slug,
  difficulty: "Easy",
  tags: ["t"],
  order,
});
const lesson = (id: string, order: number, exerciseSlugs: string[]): Lesson => ({
  id,
  title: id,
  order,
  exerciseSlugs,
  track: "sql",
  bodyMd: "",
});

const problems = [p("a", "sql", 1), p("b", "sql", 2), p("c", "sql", 3), p("d", "sql", 4), p("loose", "sql", 5), p("last", "sql", 6)];
const lessons = [lesson("l1", 1, ["a", "b"]), lesson("l2", 2, ["c", "d"])];

describe("getNextTarget", () => {
  it("goes to the next exercise in a lesson", () => {
    expect(getNextTarget(problems, lessons, "a")?.href).toBe("/problems/b");
  });

  it("goes to the next lesson after the last exercise", () => {
    expect(getNextTarget(problems, lessons, "b")?.href).toBe("/learn/sql/l2");
  });

  it("returns to the lesson list after the final lesson", () => {
    expect(getNextTarget(problems, lessons, "d")?.href).toBe("/learn/sql");
  });

  it("falls back to list order outside lessons", () => {
    expect(getNextTarget(problems, lessons, "loose")?.href).toBe("/problems/last");
    expect(getNextTarget(problems, lessons, "last")?.href).toBe("/problems");
  });

  it("returns null for an unknown problem", () => {
    expect(getNextTarget(problems, lessons, "nope")).toBeNull();
  });
});
