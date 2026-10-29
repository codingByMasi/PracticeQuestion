/**
 * Validates all content: schemas and cross references (via the loader), then runs
 * every problem's reference solution through the same judge the app uses.
 *
 *   npm run validate:content
 */
import initSqlJs from "sql.js";
import { ContentError, loadContent, type Content } from "../lib/content/load";
import type { Problem } from "../lib/content/schema";
import { judgeSql } from "../lib/judge/sql";
import type { JudgeReport } from "../lib/judge/types";
import { executeSql } from "../lib/runners/sql/engine";
import type { Execute } from "../lib/runners/types";

type Check = { label: string; ok: boolean; detail?: string };

function describeFailure(report: JudgeReport): string {
  if (report.error) return report.error;
  if (report.diff) return JSON.stringify(report.diff);
  const failed = report.cases?.filter((c) => !c.passed) ?? [];
  return failed.map((c) => `${c.label}: expected ${c.expected}, got ${c.actual ?? c.error}`).join("; ");
}

async function main() {
  let content: Content;
  try {
    content = loadContent();
  } catch (e) {
    if (e instanceof ContentError) {
      console.error(e.message);
      process.exit(1);
    }
    throw e;
  }
  console.log(
    `Loaded ${content.tracks.length} tracks, ${content.datasets.length} datasets, ${content.problems.length} problems, ${content.lessons.length} lessons.`,
  );

  const SQL = await initSqlJs();
  const executors: Record<Problem["kind"], Execute> = {
    sql: async (input) => executeSql(SQL, input),
    python: async () => ({ ok: false, error: "Python validation not available", durationMs: 0 }),
  };

  const checks: Check[] = [];
  for (const problem of content.problems) {
    const label = `${problem.track}/${problem.slug}`;
    if (problem.kind === "sql") {
      const dataset = content.datasets.find((d) => d.id === problem.datasetId);
      const sql = dataset?.sql ?? "";
      const report = await judgeSql(problem, sql, problem.expected.query, "submit", executors.sql);
      const starter = await judgeSql(problem, sql, problem.starterCode, "submit", executors.sql);
      checks.push({ label, ok: report.passed, detail: report.passed ? undefined : describeFailure(report) });
      if (starter.passed) checks.push({ label: `${label} (starter code must not pass)`, ok: false });
    }
  }

  const failed = checks.filter((c) => !c.ok);
  for (const c of checks) console.log(`${c.ok ? "✓" : "✗"} ${c.label}${c.detail ? `\n    ${c.detail}` : ""}`);
  console.log(`\n${checks.length - failed.length}/${checks.length} checks passed.`);
  if (failed.length > 0) process.exit(1);
}

main().catch((e: unknown) => {
  console.error(e);
  process.exit(1);
});
