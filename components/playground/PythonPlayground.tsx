"use client";

import { useEffect } from "react";
import { CodeEditor } from "@/components/editor/CodeEditor";
import { RunOutput } from "@/components/results/RunOutput";
import { Button } from "@/components/ui/Button";
import { SplitPane } from "@/components/ui/SplitPane";
import { useAutosaveDraft } from "@/lib/hooks/use-autosave-draft";
import { useRun } from "@/lib/hooks/use-run";
import { useProgress } from "@/lib/progress/ProgressProvider";

const DEFAULT_CODE = `# Python runs in your browser (Pyodide). Ctrl/⌘ + Enter runs the code.
# The value of the last line is shown, like a REPL.
# numpy and pandas load on demand when you import them (first time takes a few seconds).

def greet(name):
    return f"Hello, {name}!"

print(greet("CodeDrill"))
[n * n for n in range(10)]
`;

export function PythonPlayground() {
  const { ready, store } = useProgress();
  useEffect(() => {
    store.setLastVisited("/playground/python", "Python playground");
  }, [store]);
  return (
    <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-6 lg:h-[calc(100dvh-3.5rem)]">
      <h1 className="text-2xl font-bold tracking-tight">Python playground</h1>
      {ready ? <PythonWorkbench /> : <p className="text-sm text-zinc-500 dark:text-zinc-400">Loading…</p>}
    </div>
  );
}

function PythonWorkbench() {
  const [code, setCode] = useAutosaveDraft("playground:python", DEFAULT_CODE);
  const { run, result, busy, status } = useRun("python", { eager: true });
  const execute = () => run({ code, echoLastExpression: true });

  const editor = (
    <div className="flex h-full flex-col">
      <div className="flex items-center gap-2 border-b border-zinc-200 px-3 py-2 dark:border-zinc-800">
        <Button variant="primary" onClick={execute} disabled={busy || status.state === "loading"}>
          ▶ Run
        </Button>
        <Button variant="ghost" onClick={() => setCode(DEFAULT_CODE)}>
          Reset
        </Button>
        <span className="ml-auto text-xs text-zinc-500 dark:text-zinc-400">
          {status.state === "ready" ? "Python ready" : status.state === "loading" ? "Loading Python…" : ""}
        </span>
      </div>
      <div className="h-[50vh] lg:h-auto lg:flex-1">
        <CodeEditor value={code} onChange={setCode} language="python" onRun={execute} ariaLabel="Python playground editor" />
      </div>
    </div>
  );

  const output = (
    <section aria-label="Output" className="h-full overflow-auto p-3">
      <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">Output</h2>
      {!result && !busy && status.state !== "loading" ? (
        <p className="text-sm text-zinc-500 dark:text-zinc-400">Run your code to see stdout, stderr and errors here.</p>
      ) : (
        <RunOutput result={result} status={status} busy={busy} />
      )}
    </section>
  );

  return (
    <div className="min-h-0 flex-1 overflow-hidden rounded-lg border border-zinc-200 dark:border-zinc-800">
      <SplitPane label="Resize editor and output" initial={60} className="h-full" first={editor} second={output} />
    </div>
  );
}
