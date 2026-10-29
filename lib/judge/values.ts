export const DEFAULT_TOLERANCE = 1e-6;

export function numbersClose(a: number, b: number, tolerance = DEFAULT_TOLERANCE): boolean {
  if (Number.isNaN(a) || Number.isNaN(b)) return Number.isNaN(a) && Number.isNaN(b);
  if (a === b) return true;
  return Math.abs(a - b) <= tolerance * Math.max(1, Math.abs(a), Math.abs(b));
}

/** Compact, readable rendering of a value for diffs. */
export function formatValue(v: unknown): string {
  if (v === null || v === undefined) return "NULL";
  if (typeof v === "string") return JSON.stringify(v);
  return typeof v === "object" ? JSON.stringify(v) : String(v);
}
