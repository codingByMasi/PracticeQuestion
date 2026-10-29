"use client";

import { useEffect, useState } from "react";
import { useRunner } from "@/lib/hooks/use-runner";
import { SCHEMA_QUERY } from "@/lib/runners/sql/schema-query";

type Column = { name: string; type: string; pk: boolean };
type Schema = { table: string; columns: Column[] }[];

export function SchemaBrowser({ setup, onInsert }: { setup: string; onInsert?: (text: string) => void }) {
  const { runner } = useRunner("sql");
  const [schema, setSchema] = useState<Schema | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    runner.run({ code: SCHEMA_QUERY, setup }).then((res) => {
      if (cancelled) return;
      if (!res.ok || !res.table) {
        setError(res.error ?? "Could not read schema");
        return;
      }
      const byTable = new Map<string, Column[]>();
      for (const [table, name, type, pk] of res.table.rows) {
        const cols = byTable.get(String(table)) ?? [];
        cols.push({ name: String(name), type: String(type), pk: Number(pk) > 0 });
        byTable.set(String(table), cols);
      }
      setError(null);
      setSchema([...byTable].map(([table, columns]) => ({ table, columns })));
    });
    return () => {
      cancelled = true;
    };
  }, [runner, setup]);

  if (error) return <p className="text-sm text-rose-600">{error}</p>;
  if (!schema) return <p className="text-sm text-zinc-500">Loading schema…</p>;
  return (
    <ul className="space-y-2 text-sm">
      {schema.map((t) => (
        <li key={t.table}>
          <details open>
            <summary className="cursor-pointer font-mono font-semibold">
              {onInsert ? (
                <button type="button" className="hover:underline" onClick={() => onInsert(t.table)} title="Insert table name">
                  {t.table}
                </button>
              ) : (
                t.table
              )}
            </summary>
            <ul className="ml-4 mt-1 space-y-0.5 font-mono text-xs">
              {t.columns.map((c) => (
                <li key={c.name} className="flex justify-between gap-2">
                  <span>
                    {c.name}
                    {c.pk && <span className="ml-1 text-amber-600" title="Primary key">🔑</span>}
                  </span>
                  <span className="text-zinc-500">{c.type.toLowerCase()}</span>
                </li>
              ))}
            </ul>
          </details>
        </li>
      ))}
    </ul>
  );
}
