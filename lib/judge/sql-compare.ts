import type { Table } from "../runners/types";
import { DEFAULT_TOLERANCE, numbersClose } from "./values";

export type SqlDiff =
  | { kind: "columns"; expected: string[]; actual: string[] }
  | { kind: "rowCount"; expected: number; actual: number }
  | { kind: "row"; index: number; expected: unknown[]; actual: unknown[]; orderMatters: boolean };

export type CompareResult = { pass: true } | { pass: false; diff: SqlDiff };

export type CompareOptions = { orderMatters: boolean; tolerance?: number };

function valuesEqual(a: unknown, b: unknown, tolerance: number): boolean {
  if (typeof a === "number" && typeof b === "number") return numbersClose(a, b, tolerance);
  if (a === null || a === undefined) return b === null || b === undefined;
  return a === b;
}

function typeRank(v: unknown): number {
  if (v === null || v === undefined) return 0;
  if (typeof v === "number") return 1;
  if (typeof v === "string") return 2;
  return 3;
}

function compareValues(a: unknown, b: unknown): number {
  const ra = typeRank(a);
  const rb = typeRank(b);
  if (ra !== rb) return ra - rb;
  if (typeof a === "number" && typeof b === "number") return a - b;
  const sa = String(a);
  const sb = String(b);
  return sa < sb ? -1 : sa > sb ? 1 : 0;
}

function compareRows(a: unknown[], b: unknown[]): number {
  for (let i = 0; i < Math.max(a.length, b.length); i++) {
    const c = compareValues(a[i], b[i]);
    if (c !== 0) return c;
  }
  return 0;
}

/**
 * Aligns `actual` columns to `expected` by case-insensitive name. Same names in a
 * different order are accepted and reordered; anything else is a column mismatch.
 */
function alignColumns(actual: Table, expected: Table): Table | null {
  const exp = expected.columns.map((c) => c.toLowerCase());
  const act = actual.columns.map((c) => c.toLowerCase());
  if (exp.length !== act.length) return null;
  if (exp.every((c, i) => c === act[i])) return actual;
  const used = new Set<number>();
  const order: number[] = [];
  for (const c of exp) {
    const idx = act.findIndex((a, i) => a === c && !used.has(i));
    if (idx === -1) return null;
    used.add(idx);
    order.push(idx);
  }
  return { columns: order.map((i) => actual.columns[i] ?? ""), rows: actual.rows.map((r) => order.map((i) => r[i])) };
}

export function compareResultSets(actual: Table, expected: Table, options: CompareOptions): CompareResult {
  const tolerance = options.tolerance ?? DEFAULT_TOLERANCE;
  const aligned = alignColumns(actual, expected);
  if (!aligned) return { pass: false, diff: { kind: "columns", expected: expected.columns, actual: actual.columns } };
  if (aligned.rows.length !== expected.rows.length)
    return { pass: false, diff: { kind: "rowCount", expected: expected.rows.length, actual: aligned.rows.length } };

  const exp = options.orderMatters ? expected.rows : [...expected.rows].sort(compareRows);
  const act = options.orderMatters ? aligned.rows : [...aligned.rows].sort(compareRows);
  for (let i = 0; i < exp.length; i++) {
    const e = exp[i] ?? [];
    const a = act[i] ?? [];
    if (e.length !== a.length || e.some((v, j) => !valuesEqual(a[j], v, tolerance)))
      return { pass: false, diff: { kind: "row", index: i, expected: e, actual: a, orderMatters: options.orderMatters } };
  }
  return { pass: true };
}
