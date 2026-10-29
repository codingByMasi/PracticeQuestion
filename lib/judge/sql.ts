import type { SqlProblem } from "../content/schema";
import type { Execute } from "../runners/types";
import { compareResultSets } from "./sql-compare";
import type { JudgeMode, JudgeReport } from "./types";

export function sqlSetup(problem: Pick<SqlProblem, "setupSql">, datasetSql: string): string {
  return problem.setupSql ? `${datasetSql}\n${problem.setupSql}` : datasetSql;
}

/** Runs the user query and the reference query on identical fresh databases and compares results. */
export async function judgeSql(
  problem: SqlProblem,
  datasetSql: string,
  code: string,
  mode: JudgeMode,
  execute: Execute,
): Promise<JudgeReport> {
  const setup = sqlSetup(problem, datasetSql);
  const user = await execute({ code, setup });
  if (!user.ok) return { mode, passed: false, durationMs: user.durationMs, error: user.error };
  if (!user.table)
    return {
      mode,
      passed: false,
      durationMs: user.durationMs,
      stdout: user.stdout,
      error: "Your query did not return a result set. Make sure it ends with a SELECT statement.",
    };

  const ref = await execute({ code: problem.expected.query, setup });
  if (!ref.ok || !ref.table)
    return { mode, passed: false, durationMs: user.durationMs, error: `Reference query failed: ${ref.error ?? "no result"}` };

  const cmp = compareResultSets(user.table, ref.table, { orderMatters: problem.expected.orderMatters });
  return {
    mode,
    passed: cmp.pass,
    durationMs: user.durationMs,
    table: user.table,
    expectedTable: ref.table,
    diff: cmp.pass ? undefined : cmp.diff,
  };
}
