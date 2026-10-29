import { formatValue } from "@/lib/judge/values";
import type { Table } from "@/lib/runners/types";

const MAX_ROWS = 200;

export function ResultTable({ table, caption, highlightRow }: { table: Table; caption?: string; highlightRow?: number }) {
  const rows = table.rows.slice(0, MAX_ROWS);
  return (
    <div className="max-w-full overflow-auto rounded border border-zinc-200 dark:border-zinc-800">
      <table className="min-w-full text-left font-mono text-xs">
        {caption && <caption className="bg-zinc-50 px-2 py-1 text-left font-sans text-xs font-medium text-zinc-600 dark:bg-zinc-900 dark:text-zinc-400">{caption}</caption>}
        <thead className="bg-zinc-100 dark:bg-zinc-800">
          <tr>
            {table.columns.map((c, i) => (
              <th key={i} scope="col" className="whitespace-nowrap px-2 py-1 font-semibold">
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, r) => (
            <tr
              key={r}
              className={`border-t border-zinc-100 dark:border-zinc-800 ${r === highlightRow ? "bg-rose-50 dark:bg-rose-950/40" : ""}`}
            >
              {row.map((v, c) => (
                <td key={c} className={`whitespace-nowrap px-2 py-1 ${v === null ? "italic text-zinc-500 dark:text-zinc-400" : ""}`}>
                  {v === null ? "NULL" : typeof v === "string" ? v : formatValue(v)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <p className="border-t border-zinc-100 px-2 py-1 text-xs text-zinc-500 dark:text-zinc-400 dark:border-zinc-800">
        {table.rows.length} row{table.rows.length === 1 ? "" : "s"}
        {table.rows.length > MAX_ROWS ? ` (showing first ${MAX_ROWS})` : ""}
      </p>
    </div>
  );
}
