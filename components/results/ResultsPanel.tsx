import type { JudgeReport } from "@/lib/judge/types";
import type { RunnerStatus } from "@/lib/runners/types";
import { ResultTable } from "./ResultTable";
import { SqlDiffView } from "./SqlDiffView";

function Verdict({ report }: { report: JudgeReport }) {
  const passed = report.passed;
  const total = report.cases?.length;
  const passedCount = report.cases?.filter((c) => c.passed).length;
  const label =
    report.mode === "submit"
      ? passed
        ? "Accepted"
        : report.error
          ? "Error"
          : "Wrong answer"
      : passed
        ? "Looks right. Submit when ready."
        : report.error
          ? "Error"
          : "Not matching yet";
  return (
    <div className="flex flex-wrap items-baseline gap-x-3">
      <p className={`text-base font-semibold ${passed ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400"}`}>
        {label}
      </p>
      {total !== undefined && (
        <span className="text-sm text-zinc-500">
          {passedCount}/{total} tests passed
        </span>
      )}
      <span className="text-xs text-zinc-500">{report.durationMs} ms</span>
    </div>
  );
}

export function ResultsPanel({ report, status, busy }: { report: JudgeReport | null; status: RunnerStatus; busy: boolean }) {
  return (
    <section aria-label="Results" aria-live="polite" className="h-full space-y-3 overflow-auto p-3 text-sm">
      {status.state === "loading" && (
        <p className="flex items-center gap-2 text-zinc-600 dark:text-zinc-400">
          <span className="h-3 w-3 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" aria-hidden="true" />
          {status.message ?? "Loading runtime…"}
        </p>
      )}
      {status.state === "error" && <p className="text-rose-600">Runtime failed to load: {status.message}</p>}
      {busy && status.state !== "loading" && <p className="text-zinc-500">Running…</p>}
      {!report && !busy && status.state !== "loading" && (
        <p className="text-zinc-500">
          Press <kbd className="rounded border px-1 font-mono text-xs">Ctrl/⌘ + Enter</kbd> to run,{" "}
          <kbd className="rounded border px-1 font-mono text-xs">Ctrl/⌘ + Shift + Enter</kbd> to submit.
        </p>
      )}
      {report && !busy && (
        <>
          <Verdict report={report} />
          {report.error && (
            <pre className="overflow-auto whitespace-pre-wrap rounded bg-rose-50 p-2 font-mono text-xs text-rose-800 dark:bg-rose-950/40 dark:text-rose-200">
              {report.error}
            </pre>
          )}
          {report.diff && (
            <div className="rounded border border-rose-200 bg-rose-50/50 p-2 dark:border-rose-900 dark:bg-rose-950/20">
              <SqlDiffView diff={report.diff} />
            </div>
          )}
          {report.stdout && (
            <pre className="overflow-auto whitespace-pre-wrap rounded bg-zinc-100 p-2 font-mono text-xs dark:bg-zinc-900">{report.stdout}</pre>
          )}
          {report.cases && (
            <ol className="space-y-2">
              {report.cases.map((c, i) => (
                <li key={i} className="rounded border border-zinc-200 p-2 dark:border-zinc-800">
                  <p className="font-medium">
                    <span className={c.passed ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400"}>
                      {c.passed ? "✓" : "✗"}
                    </span>{" "}
                    {c.label}
                    {c.hidden && <span className="ml-2 text-xs text-zinc-500">(hidden)</span>}
                  </p>
                  {!c.hidden && (
                    <dl className="mt-1 grid grid-cols-[max-content_1fr] gap-x-3 font-mono text-xs">
                      {c.input !== undefined && (
                        <>
                          <dt className="text-zinc-500">input</dt>
                          <dd className="break-all">{c.input}</dd>
                        </>
                      )}
                      {c.expected !== undefined && (
                        <>
                          <dt className="text-zinc-500">expected</dt>
                          <dd className="break-all">{c.expected}</dd>
                        </>
                      )}
                      {c.actual !== undefined && (
                        <>
                          <dt className="text-zinc-500">got</dt>
                          <dd className="break-all">{c.actual}</dd>
                        </>
                      )}
                      {c.stdout && (
                        <>
                          <dt className="text-zinc-500">stdout</dt>
                          <dd className="whitespace-pre-wrap">{c.stdout}</dd>
                        </>
                      )}
                    </dl>
                  )}
                  {c.error && (
                    <pre className="mt-1 overflow-auto whitespace-pre-wrap font-mono text-xs text-rose-700 dark:text-rose-300">{c.error}</pre>
                  )}
                </li>
              ))}
            </ol>
          )}
          {report.table && (
            <ResultTable
              table={report.table}
              caption="Your result"
              highlightRow={report.diff?.kind === "row" && report.diff.orderMatters ? report.diff.index : undefined}
            />
          )}
          {report.expectedTable && !report.passed && report.mode === "run" && <ResultTable table={report.expectedTable} caption="Expected result" />}
        </>
      )}
    </section>
  );
}
