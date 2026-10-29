"use client";

import { useCallback, useEffect, useState } from "react";
import { CodeEditor } from "@/components/editor/CodeEditor";
import { ResultsPanel } from "@/components/results/ResultsPanel";
import { SchemaBrowser } from "@/components/sql/SchemaBrowser";
import { Button } from "@/components/ui/Button";
import { SplitPane } from "@/components/ui/SplitPane";
import type { Problem } from "@/lib/content/schema";
import { useAutosaveDraft } from "@/lib/hooks/use-autosave-draft";
import { useRunner } from "@/lib/hooks/use-runner";
import { judgeProblem, type JudgeMode, type JudgeReport } from "@/lib/judge";
import { sqlSetup } from "@/lib/judge/sql";
import { useProgress } from "@/lib/progress/ProgressProvider";
import { ProblemDescription } from "./ProblemDescription";

type Props = {
  problem: Problem;
  runnerId: string;
  editorLanguage: string;
  datasetSql?: string;
};

export function ProblemWorkspace(props: Props) {
  const { ready } = useProgress();
  if (!ready) return <p className="p-6 text-sm text-zinc-500 dark:text-zinc-400">Loading…</p>;
  return <Workspace {...props} />;
}

function Workspace({ problem, runnerId, editorLanguage, datasetSql }: Props) {
  const { store } = useProgress();
  const { runner, status } = useRunner(runnerId);
  const [code, setCode] = useAutosaveDraft(problem.slug, problem.starterCode);
  const [report, setReport] = useState<JudgeReport | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    store.setLastVisited(`/problems/${problem.slug}`, problem.title);
  }, [store, problem.slug, problem.title]);

  const execute = useCallback(
    async (mode: JudgeMode) => {
      if (busy) return;
      setBusy(true);
      try {
        const r = await judgeProblem(problem, code, mode, { execute: (input) => runner.run(input), datasetSql });
        setReport(r);
        if (mode === "submit") store.saveAttempt(problem.slug, code, r.passed);
      } finally {
        setBusy(false);
      }
    },
    [busy, problem, code, runner, datasetSql, store],
  );

  const status_ = store.getProblemStatus(problem.slug);
  const failed = store.getFailedAttempts(problem.slug);
  const schema = problem.kind === "sql" && datasetSql !== undefined ? <SchemaBrowser setup={sqlSetup(problem, datasetSql)} /> : undefined;

  const editorPane = (
    <div className="flex h-full min-h-0 flex-col">
      <div className="flex flex-wrap items-center gap-2 border-b border-zinc-200 px-3 py-2 dark:border-zinc-800">
        <Button variant="secondary" onClick={() => execute("run")} disabled={busy} title="Run (Ctrl/⌘+Enter)">
          ▶ Run
        </Button>
        <Button variant="primary" onClick={() => execute("submit")} disabled={busy} title="Submit (Ctrl/⌘+Shift+Enter)">
          Submit
        </Button>
        <Button
          variant="ghost"
          className="ml-auto"
          onClick={() => {
            if (window.confirm("Reset your code to the starter template?")) setCode(problem.starterCode);
          }}
        >
          Reset
        </Button>
      </div>
      <div className="h-[50vh] min-h-0 lg:h-auto lg:flex-1">
        <CodeEditor
          value={code}
          onChange={setCode}
          language={editorLanguage}
          onRun={() => execute("run")}
          onSubmit={() => execute("submit")}
          ariaLabel={`${problem.title} code editor`}
        />
      </div>
    </div>
  );

  return (
    <div className="lg:h-[calc(100dvh-3.5rem)]">
      <SplitPane
        label="Resize description and editor"
        initial={42}
        className="h-full"
        first={<ProblemDescription problem={problem} status={status_} failedAttempts={failed} schema={schema} />}
        second={
          <SplitPane
            orientation="vertical"
            label="Resize editor and results"
            initial={60}
            className="h-full"
            first={editorPane}
            second={<ResultsPanel report={report} status={status} busy={busy} />}
          />
        }
      />
    </div>
  );
}
