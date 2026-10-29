import { addDays, dayNumber } from "./dates";

export type HeatmapCell = { date: string; count: number; inRange: boolean };

/**
 * Builds a GitHub-style grid of `weeks` columns × 7 rows (Sunday first) ending
 * with the week containing `today`. Cells after today are marked out of range.
 */
export function buildHeatmap(counts: Record<string, number>, today: string, weeks = 53): HeatmapCell[][] {
  const weekday = (dayNumber(today) + 4) % 7; // 1970-01-01 was a Thursday (4); 0 = Sunday
  const start = addDays(today, -(weeks - 1) * 7 - weekday);
  const columns: HeatmapCell[][] = [];
  for (let w = 0; w < weeks; w++) {
    const col: HeatmapCell[] = [];
    for (let d = 0; d < 7; d++) {
      const date = addDays(start, w * 7 + d);
      col.push({ date, count: counts[date] ?? 0, inRange: date <= today });
    }
    columns.push(col);
  }
  return columns;
}

export function intensity(count: number): 0 | 1 | 2 | 3 | 4 {
  if (count <= 0) return 0;
  if (count <= 2) return 1;
  if (count <= 5) return 2;
  if (count <= 9) return 3;
  return 4;
}
