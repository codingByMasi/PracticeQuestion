import type { PyodideAPI } from "pyodide";
import type { CaseOutcome, RunInput, RunResult } from "../types";
import { HARNESS_PY } from "./harness";

type HarnessOutput = { ok: boolean; error?: string; stdout?: string; stderr?: string; cases?: CaseOutcome[] };

/** Defines the harness in a loaded Pyodide instance. Call once after loading. */
export function installHarness(pyodide: PyodideAPI): void {
  pyodide.runPython(HARNESS_PY);
}

/** Runs user code (and optional test cases) through the harness. Shared by worker and validator. */
export function executePython(pyodide: PyodideAPI, input: RunInput): RunResult {
  const start = performance.now();
  const fn = pyodide.globals.get("_codedrill_run") as ((...args: unknown[]) => string) & { destroy(): void };
  try {
    const raw = fn(
      input.code,
      input.harness?.functionName ?? null,
      JSON.stringify(input.harness?.cases ?? []),
      input.echoLastExpression ?? false,
    );
    const out = JSON.parse(raw) as HarnessOutput;
    return {
      ok: out.ok,
      error: out.error,
      stdout: out.stdout || undefined,
      stderr: out.stderr || undefined,
      cases: out.cases,
      durationMs: Math.round(performance.now() - start),
    };
  } catch (e) {
    return { ok: false, error: (e as Error).message, durationMs: Math.round(performance.now() - start) };
  } finally {
    fn.destroy();
  }
}
