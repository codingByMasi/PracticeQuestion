"use client";

import { useState } from "react";
import { CodeEditor } from "@/components/editor/CodeEditor";
import { RunOutput } from "@/components/results/RunOutput";
import { Button } from "@/components/ui/Button";
import { useRun } from "@/lib/hooks/use-run";

type Props = { code: string; runnerId: string; language: string; setup?: string };

const LINE_HEIGHT = 19;

/** An editable code block from a lesson. The runtime loads on first Run. */
export function RunnableSnippet({ code: initial, runnerId, language, setup }: Props) {
  const [code, setCode] = useState(initial);
  const { run, result, busy, status } = useRun(runnerId);
  const lines = Math.min(24, Math.max(2, code.split("\n").length));
  const execute = () => run({ code, setup, echoLastExpression: true });

  return (
    <div className="not-prose my-4 overflow-hidden rounded-lg border border-zinc-200 dark:border-zinc-800">
      <div style={{ height: lines * LINE_HEIGHT + 16 }}>
        <CodeEditor value={code} onChange={setCode} language={language} onRun={execute} ariaLabel="Runnable example" />
      </div>
      <div className="flex items-center gap-2 border-t border-zinc-200 bg-zinc-50 px-3 py-1.5 dark:border-zinc-800 dark:bg-zinc-900">
        <Button variant="primary" onClick={execute} disabled={busy} className="py-1">
          ▶ Run
        </Button>
        {code !== initial && (
          <Button variant="ghost" onClick={() => setCode(initial)} className="py-1">
            Reset
          </Button>
        )}
        <span className="ml-auto text-xs text-zinc-500 dark:text-zinc-400">Ctrl/⌘ + Enter</span>
      </div>
      {(result || busy || status.state === "loading" || status.state === "error") && (
        <div className="border-t border-zinc-200 p-3 dark:border-zinc-800">
          <RunOutput result={result} status={status} busy={busy} />
        </div>
      )}
    </div>
  );
}
