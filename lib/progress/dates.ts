/** Local calendar date as YYYY-MM-DD. */
export function toLocalDateKey(d: Date): string {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

const DAY_MS = 86_400_000;

/** Days since epoch for a YYYY-MM-DD key (calendar arithmetic, DST-safe). */
export function dayNumber(key: string): number {
  const [y, m, d] = key.split("-").map(Number);
  return Math.round(Date.UTC(y ?? 1970, (m ?? 1) - 1, d ?? 1) / DAY_MS);
}

export function addDays(key: string, delta: number): string {
  const d = new Date((dayNumber(key) + delta) * DAY_MS);
  return d.toISOString().slice(0, 10);
}

export function isDateKey(s: string): boolean {
  return /^\d{4}-\d{2}-\d{2}$/.test(s) && addDays(s, 0) === s;
}
