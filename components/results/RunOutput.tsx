import type { RunResult, RunnerStatus } from "@/lib/runners/types";
import { ResultTable } from "./ResultTable";

/** Displays a raw RunResult (playgrounds and lesson snippets). */
export function RunOutput({ result, status, busy }: { result: RunResult | null; status: RunnerStatus; busy: boolean }) {
  return (
    <div aria-live="polite" className="space-y-2 text-sm">
      {status.state === "loading" && (
        <p className="flex items-center gap-2 text-zinc-600 dark:text-zinc-400">
          <span className="h-3 w-3 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" aria-hidden="true" />
          {status.message ?? "Loading runtime…"}
        </p>
      )}
      {busy && status.state === "running" && <p className="text-zinc-500 dark:text-zinc-400">{status.message ?? "Running…"}</p>}
      {status.state === "error" && <p className="text-rose-600">Runtime failed to load: {status.message}</p>}
      {result && !busy && (
        <>
          {result.table && <ResultTable table={result.table} />}
          {result.stdout && (
            <pre className="max-h-80 overflow-auto whitespace-pre-wrap rounded bg-zinc-100 p-2 font-mono text-xs dark:bg-zinc-900">{result.stdout}</pre>
          )}
          {result.stderr && (
            <pre className="max-h-60 overflow-auto whitespace-pre-wrap rounded bg-amber-50 p-2 font-mono text-xs text-amber-900 dark:bg-amber-950/40 dark:text-amber-200">
              {result.stderr}
            </pre>
          )}
          {result.error && (
            <pre className="overflow-auto whitespace-pre-wrap rounded bg-rose-50 p-2 font-mono text-xs text-rose-800 dark:bg-rose-950/40 dark:text-rose-200">
              {result.error}
            </pre>
          )}
          {result.ok && !result.table && !result.stdout && !result.stderr && <p className="text-zinc-500 dark:text-zinc-400">(no output)</p>}
          <p className="text-xs text-zinc-500 dark:text-zinc-400">{result.durationMs} ms</p>
        </>
      )}
    </div>
  );
}
