import type { SqlJsStatic } from "sql.js";
import type { RunInput, RunResult } from "../types";

function normalizeValue(v: unknown): unknown {
  if (v instanceof Uint8Array) return `<blob ${v.byteLength} bytes>`;
  return v;
}

/**
 * Runs SQL against a fresh in-memory SQLite database, so destructive statements
 * never leak between runs. Shared by the browser worker and the Node validator.
 */
export function executeSql(SQL: SqlJsStatic, input: RunInput): RunResult {
  const start = performance.now();
  const done = (r: Omit<RunResult, "durationMs">): RunResult => ({ ...r, durationMs: Math.round(performance.now() - start) });
  if (!input.code.trim()) return done({ ok: false, error: "Write a query first." });

  const db = new SQL.Database();
  try {
    if (input.setup) {
      try {
        db.exec(input.setup);
      } catch (e) {
        return done({ ok: false, error: `Dataset setup failed: ${(e as Error).message}` });
      }
    }
    try {
      const results = db.exec(input.code);
      const last = results.at(-1);
      if (!last) return done({ ok: true, stdout: `Statement executed. ${db.getRowsModified()} row(s) changed.` });
      return done({
        ok: true,
        table: { columns: last.columns, rows: last.values.map((row) => row.map(normalizeValue)) },
      });
    } catch (e) {
      return done({ ok: false, error: (e as Error).message });
    }
  } finally {
    db.close();
  }
}
