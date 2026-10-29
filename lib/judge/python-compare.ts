import { DEFAULT_TOLERANCE, numbersClose } from "./values";

/** Structural equality for JSON values; numbers compare with tolerance, bools never equal numbers. */
export function jsonEqual(actual: unknown, expected: unknown, tolerance = DEFAULT_TOLERANCE): boolean {
  if (typeof actual === "number" && typeof expected === "number") return numbersClose(actual, expected, tolerance);
  if (Array.isArray(expected)) {
    return Array.isArray(actual) && actual.length === expected.length && expected.every((e, i) => jsonEqual(actual[i], e, tolerance));
  }
  if (expected !== null && typeof expected === "object") {
    if (actual === null || typeof actual !== "object" || Array.isArray(actual)) return false;
    const a = actual as Record<string, unknown>;
    const e = expected as Record<string, unknown>;
    const keys = Object.keys(e);
    return keys.length === Object.keys(a).length && keys.every((k) => k in a && jsonEqual(a[k], e[k], tolerance));
  }
  return actual === expected;
}

/** Python-flavoured rendering of a JSON value (True/False/None). */
export function formatPython(v: unknown): string {
  if (v === null || v === undefined) return "None";
  if (v === true) return "True";
  if (v === false) return "False";
  if (typeof v === "string") {
    const inner = JSON.stringify(v).slice(1, -1).replace(/\\"/g, '"');
    return inner.includes("'") && !inner.includes('"') ? `"${inner}"` : `'${inner.replace(/'/g, "\\'")}'`;
  }
  if (Array.isArray(v)) return `[${v.map(formatPython).join(", ")}]`;
  if (typeof v === "object")
    return `{${Object.entries(v as Record<string, unknown>)
      .map(([k, x]) => `${formatPython(k)}: ${formatPython(x)}`)
      .join(", ")}}`;
  return String(v);
}
