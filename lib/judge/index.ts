import type { Problem } from "../content/schema";
import type { Execute } from "../runners/types";
import { judgePython } from "./python";
import { judgeSql } from "./sql";
import type { JudgeMode, JudgeReport } from "./types";

export type JudgeContext = { execute: Execute; datasetSql?: string };

/** Dispatches to the judge for the problem's runner. */
export async function judgeProblem(problem: Problem, code: string, mode: JudgeMode, ctx: JudgeContext): Promise<JudgeReport> {
  switch (problem.kind) {
    case "sql":
      return judgeSql(problem, ctx.datasetSql ?? "", code, mode, ctx.execute);
    case "python":
      return judgePython(problem, code, mode, ctx.execute);
  }
}

export type { JudgeMode, JudgeReport } from "./types";
