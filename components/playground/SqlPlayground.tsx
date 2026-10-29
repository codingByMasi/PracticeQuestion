"use client";

import { useEffect, useState } from "react";
import { CodeEditor } from "@/components/editor/CodeEditor";
import { RunOutput } from "@/components/results/RunOutput";
import { SchemaBrowser } from "@/components/sql/SchemaBrowser";
import { Button } from "@/components/ui/Button";
import { useAutosaveDraft } from "@/lib/hooks/use-autosave-draft";
import { useRun } from "@/lib/hooks/use-run";
import { useProgress } from "@/lib/progress/ProgressProvider";

type DatasetOption = { id: string; title: string; description: string; sql: string };

function defaultQuery(sql: string): string {
  const table = /CREATE TABLE\s+(\w+)/i.exec(sql)?.[1] ?? "sqlite_master";
  return `-- Explore the data. Ctrl/⌘ + Enter runs the query.\nSELECT * FROM ${table} LIMIT 10;\n`;
}

export function SqlPlayground({ datasets }: { datasets: DatasetOption[] }) {
  const { ready, store } = useProgress();
  const [datasetId, setDatasetId] = useState(datasets[0]?.id ?? "");
  const dataset = datasets.find((d) => d.id === datasetId);

  useEffect(() => {
    store.setLastVisited("/playground/sql", "SQL playground");
  }, [store]);

  if (!dataset) return <p className="p-6">No datasets available.</p>;
  return (
    <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-6 lg:h-[calc(100dvh-3.5rem)]">
      <div className="flex flex-wrap items-end gap-3">
        <h1 className="text-2xl font-bold tracking-tight">SQL playground</h1>
        <label className="ml-auto flex items-center gap-2 text-sm">
          Dataset
          <select
            className="rounded-md border border-zinc-300 bg-white px-2 py-1.5 dark:border-zinc-700 dark:bg-zinc-900"
            value={datasetId}
            onChange={(e) => setDatasetId(e.target.value)}
          >
            {datasets.map((d) => (
              <option key={d.id} value={d.id}>
                {d.title}
              </option>
            ))}
          </select>
        </label>
      </div>
      <p className="text-sm text-zinc-600 dark:text-zinc-400">
        {dataset.description} Every run starts from a fresh copy of the dataset, so feel free to INSERT, UPDATE or DROP.
      </p>
      {ready ? <SqlWorkbench key={dataset.id} dataset={dataset} /> : <p className="text-sm text-zinc-500">Loading…</p>}
    </div>
  );
}

function SqlWorkbench({ dataset }: { dataset: DatasetOption }) {
  const [code, setCode] = useAutosaveDraft(`playground:sql:${dataset.id}`, defaultQuery(dataset.sql));
  const { run, result, busy, status } = useRun("sql", { eager: true });
  const execute = () => run({ code, setup: dataset.sql });

  return (
    <div className="grid min-h-0 flex-1 gap-4 lg:grid-cols-[16rem_1fr]">
      <aside aria-label="Schema" className="overflow-auto rounded-lg border border-zinc-200 p-3 lg:max-h-full dark:border-zinc-800">
        <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-zinc-500">Schema</h2>
        <SchemaBrowser setup={dataset.sql} />
      </aside>
      <div className="flex min-h-0 flex-col overflow-hidden rounded-lg border border-zinc-200 dark:border-zinc-800">
        <div className="flex items-center gap-2 border-b border-zinc-200 px-3 py-2 dark:border-zinc-800">
          <Button variant="primary" onClick={execute} disabled={busy}>
            ▶ Run
          </Button>
          <Button variant="ghost" onClick={() => setCode(defaultQuery(dataset.sql))}>
            Reset
          </Button>
        </div>
        <div className="h-[40vh] shrink-0 lg:h-[45%]">
          <CodeEditor value={code} onChange={setCode} language="sql" onRun={execute} ariaLabel="SQL playground editor" />
        </div>
        <section aria-label="Output" className="min-h-0 flex-1 overflow-auto border-t border-zinc-200 p-3 dark:border-zinc-800">
          {!result && !busy ? <p className="text-sm text-zinc-500">Run a query to see results.</p> : <RunOutput result={result} status={status} busy={busy} />}
        </section>
      </div>
    </div>
  );
}
