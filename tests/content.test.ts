import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { describe, expect, it } from "vitest";
import { ContentError, loadContent } from "@/lib/content/load";

function fixture(files: Record<string, unknown>): string {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "codedrill-content-"));
  for (const [rel, body] of Object.entries(files)) {
    const file = path.join(root, rel);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, typeof body === "string" ? body : JSON.stringify(body));
  }
  return root;
}

const sqlTrack = { id: "sql", title: "SQL", description: "d", runnerId: "sql", editorLanguage: "sql", order: 1 };
const pyTrack = { id: "python", title: "Python", description: "d", runnerId: "python", editorLanguage: "python", order: 2 };
const dataset = { id: "tiny", title: "Tiny", description: "d" };
const sqlProblem = {
  slug: "all-rows",
  track: "sql",
  title: "All rows",
  difficulty: "Easy",
  tags: ["select"],
  statementMd: "Select everything.",
  hints: [],
  solutionMd: "Use SELECT *.",
  starterCode: "",
  datasetId: "tiny",
  expected: { query: "SELECT * FROM t", orderMatters: false },
};
const pyProblem = {
  slug: "add",
  track: "python",
  title: "Add",
  difficulty: "Easy",
  tags: ["basics"],
  statementMd: "Add.",
  hints: ["Use +"],
  solutionMd: "a + b",
  starterCode: "def add(a, b):\n    pass\n",
  functionName: "add",
  referenceSolution: "def add(a, b):\n    return a + b\n",
  tests: [
    { args: [1, 2], expected: 3, hidden: false },
    { args: [2, 2], expected: 4, hidden: true },
  ],
};
const lesson = (slugs: string[]) =>
  `---\nid: intro\ntitle: Intro\norder: 1\nexerciseSlugs: [${slugs.join(", ")}]\n---\n# Hello\n`;

const valid = {
  "tracks/sql.json": sqlTrack,
  "tracks/python.json": pyTrack,
  "datasets/tiny.json": dataset,
  "datasets/tiny.sql": "CREATE TABLE t(x INT); INSERT INTO t VALUES (1);",
  "problems/sql/all-rows.json": sqlProblem,
  "problems/python/add.json": pyProblem,
  "lessons/python/01-intro.md": lesson(["add", "add"]),
};

function issuesOf(root: string): string[] {
  try {
    loadContent(root);
    return [];
  } catch (e) {
    if (e instanceof ContentError) return e.issues;
    throw e;
  }
}

describe("content loader", () => {
  it("loads valid content", () => {
    const c = loadContent(fixture(valid));
    expect(c.tracks.map((t) => t.id)).toEqual(["sql", "python"]);
    expect(c.problems.map((p) => [p.slug, p.kind])).toEqual([
      ["add", "python"],
      ["all-rows", "sql"],
    ]);
    expect(c.datasets[0]?.sql).toContain("CREATE TABLE");
    expect(c.lessons[0]).toMatchObject({ id: "intro", track: "python", bodyMd: "# Hello" });
  });

  it("validates problems against their track's runner schema", () => {
    const issues = issuesOf(fixture({ ...valid, "problems/python/all-rows.json": { ...sqlProblem, track: "python" } }));
    expect(issues.some((i) => i.includes("problems/python/all-rows.json"))).toBe(true);
  });

  it("rejects bad difficulty and missing fields", () => {
    const { solutionMd: _omit, ...noSolution } = sqlProblem;
    void _omit;
    const issues = issuesOf(
      fixture({ ...valid, "problems/sql/all-rows.json": { ...noSolution, difficulty: "Trivial" } }),
    );
    expect(issues.join("\n")).toMatch(/difficulty/);
    expect(issues.join("\n")).toMatch(/solutionMd/);
  });

  it("requires visible and hidden python tests", () => {
    const issues = issuesOf(
      fixture({ ...valid, "problems/python/add.json": { ...pyProblem, tests: [{ args: [1, 1], expected: 2, hidden: false }] } }),
    );
    expect(issues.join("\n")).toMatch(/hidden test/);
  });

  it("checks cross references", () => {
    const issues = issuesOf(
      fixture({
        ...valid,
        "problems/sql/all-rows.json": { ...sqlProblem, datasetId: "missing" },
        "problems/sql/renamed.json": { ...sqlProblem, slug: "other" },
        "lessons/python/01-intro.md": lesson(["add", "nope"]),
        "lessons/sql/01-intro.md": lesson(["add", "all-rows"]),
      }),
    );
    const all = issues.join("\n");
    expect(all).toMatch(/unknown dataset "missing"/);
    expect(all).toMatch(/slug must match file name/);
    expect(all).toMatch(/unknown exercise "nope"/);
    expect(all).toMatch(/exercise "add" belongs to track "python"/);
  });

  it("rejects unknown keys (typos)", () => {
    const issues = issuesOf(fixture({ ...valid, "problems/sql/all-rows.json": { ...sqlProblem, hint: ["x"] } }));
    expect(issues.join("\n")).toMatch(/hint/);
  });

  it("loads the real /content folder", () => {
    const c = loadContent();
    expect(c.tracks.length).toBeGreaterThanOrEqual(2);
  });
});
