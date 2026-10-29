import type { PythonProblem } from "../content/schema";
import type { Execute } from "../runners/types";
import { formatPython, jsonEqual } from "./python-compare";
import type { CaseReport, JudgeMode, JudgeReport } from "./types";

function lastLine(s: string): string {
  return s.trim().split("\n").at(-1) ?? s;
}

/** Calls the user's function on each test (visible only for "run") and compares return values. */
export async function judgePython(problem: PythonProblem, code: string, mode: JudgeMode, execute: Execute): Promise<JudgeReport> {
  const tests = mode === "run" ? problem.tests.filter((t) => !t.hidden) : problem.tests;
  const result = await execute({
    code,
    harness: { functionName: problem.functionName, cases: tests.map((t) => ({ args: t.args })) },
  });
  if (!result.ok || !result.cases)
    return { mode, passed: false, durationMs: result.durationMs, error: result.error ?? "No result", stdout: result.stdout };

  let visibleIndex = 0;
  let hiddenIndex = 0;
  const cases: CaseReport[] = tests.map((t, i) => {
    const outcome = result.cases?.[i];
    const passed = !!outcome?.ok && jsonEqual(outcome.value, t.expected);
    const label = t.hidden ? `Hidden test ${++hiddenIndex}` : `Example ${++visibleIndex}`;
    if (t.hidden)
      return { label, hidden: true, passed, error: outcome?.error ? lastLine(outcome.error) : undefined };
    return {
      label,
      hidden: false,
      passed,
      input: `${problem.functionName}(${t.args.map(formatPython).join(", ")})`,
      expected: formatPython(t.expected),
      actual: outcome?.ok ? formatPython(outcome.value) : undefined,
      stdout: outcome?.stdout || undefined,
      error: outcome?.error,
    };
  });

  return {
    mode,
    passed: cases.every((c) => c.passed),
    durationMs: result.durationMs,
    stdout: result.stdout,
    cases,
  };
}
